#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script to check artifact definitions on a storage media image."""

import argparse
import logging
import os
import sys

from artifacts import reader as artifacts_reader
from artifacts import registry as artifacts_registry

from dfimagetools import helpers

from dfvfs.helpers import command_line
from dfvfs.helpers import volume_scanner as dfvfs_volume_scanner
from dfvfs.lib import errors

from artifactsrc import volume_scanner


def Main():
  """The main program function.

  Returns:
    bool: True if successful or False if not.
  """
  argument_parser = argparse.ArgumentParser(description=(
      'Checks artifact definitions on a storage media image.'))

  argument_parser.add_argument(
      '--artifact_definitions', '--artifact-definitions',
      dest='artifact_definitions', type=str, metavar='PATH', action='store',
      help=('Path to a directory or file containing the artifact definition '
            '.yaml files.'))

  argument_parser.add_argument(
      '--back_end', '--back-end', dest='back_end', action='store',
      metavar='NTFS', default=None, help='preferred dfVFS back-end.')

  argument_parser.add_argument(
      '--partitions', '--partition', dest='partitions', action='store',
      type=str, default=None, help=(
          'Define partitions to be processed. A range of partitions can be '
          'defined as: "3..5". Multiple partitions can be defined as: "1,3,5" '
          '(a list of comma separated values). Ranges and lists can also be '
          'combined as: "1,3..5". The first partition is 1. All partitions '
          'can be specified with: "all".'))

  argument_parser.add_argument(
      '--snapshots', '--snapshot', dest='snapshots', action='store', type=str,
      default=None, help=(
          'Define snapshots to be processed. A range of snapshots can be '
          'defined as: "3..5". Multiple snapshots can be defined as: "1,3,5" '
          '(a list of comma separated values). Ranges and lists can also be '
          'combined as: "1,3..5". The first snapshot is 1. All snapshots can '
          'be specified with: "all".'))

  argument_parser.add_argument(
      '--volumes', '--volume', dest='volumes', action='store', type=str,
      default=None, help=(
          'Define volumes to be processed. A range of volumes can be defined '
          'as: "3..5". Multiple volumes can be defined as: "1,3,5" (a list '
          'of comma separated values). Ranges and lists can also be combined '
          'as: "1,3..5". The first volume is 1. All volumes can be specified '
          'with: "all".'))

  argument_parser.add_argument(
      'source', nargs='?', action='store', metavar='image.raw',
      default=None, help='path of the storage media image.')

  options = argument_parser.parse_args()

  if not options.source:
    print('Path to source storage media image is missing.')
    print('')
    argument_parser.print_help()
    print('')
    return False

  if not options.artifact_definitions:
    print('Path to artifact definitions is missing.')
    print('')
    argument_parser.print_help()
    print('')
    return False

  helpers.SetDFVFSBackEnd(options.back_end)

  logging.basicConfig(
      level=logging.INFO, format='[%(levelname)s] %(message)s')

  registry = artifacts_registry.ArtifactDefinitionsRegistry()
  reader = artifacts_reader.YamlArtifactsReader()

  if os.path.isdir(options.artifact_definitions):
    registry.ReadFromDirectory(reader, options.artifact_definitions)
  elif os.path.isfile(options.artifact_definitions):
    registry.ReadFromFile(reader, options.artifact_definitions)

  mediator = command_line.CLIVolumeScannerMediator()
  scanner = volume_scanner.ArtifactDefinitionsVolumeScanner(
      registry, mediator=mediator)

  volume_scanner_options = dfvfs_volume_scanner.VolumeScannerOptions()
  volume_scanner_options.partitions = mediator.ParseVolumeIdentifiersString(
      options.partitions)

  if options.snapshots == 'none':
    volume_scanner_options.snapshots = ['none']
  else:
    volume_scanner_options.snapshots = mediator.ParseVolumeIdentifiersString(
        options.snapshots)

  volume_scanner_options.volumes = mediator.ParseVolumeIdentifiersString(
      options.volumes)

  try:
    if not scanner.ScanForOperatingSystemVolumes(
        options.source, options=volume_scanner_options):
      print('Unable to retrieve an operating system volume from: {0:s}.'.format(
          options.source))
      print('')
      return False

    definitions_found = set([])
    for artifact_definition in registry.GetDefinitions():
      if scanner.CheckArtifactDefinition(artifact_definition):
        definitions_found.add(artifact_definition.name)

  except errors.ScannerError as exception:
    print('[ERROR] {0!s}'.format(exception), file=sys.stderr)
    print('')
    return False

  except KeyboardInterrupt:
    print('Aborted by user.', file=sys.stderr)
    print('')
    return False

  print('Aritfact definitions found:')
  for name in sorted(definitions_found):
    print('* {0:s}'.format(name))
  print('')

  return True


if __name__ == '__main__':
  if not Main():
    sys.exit(1)
  else:
    sys.exit(0)