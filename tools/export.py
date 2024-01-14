#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script to export Digital Forensics artifact definitions as documentation."""

import argparse
import logging
import os
import sys

import artifacts

from artifacts import reader as artifacts_reader
from artifacts import registry as artifacts_registry


class StdoutOutputWriter(object):
  """Stdout output writer."""

  def Close(self):
    """Closes the output writer."""
    return

  def Open(self):
    """Opens the output writer.

    Returns:
      bool: True if successful or False if not.
    """
    return True

  def WriteDefinition(self, artifact_definition):
    """Writes an artifact definition.

    Args:
      artifact_definition (ArtifactDefinition): artifact definition.
    """
    print(artifact_definition.name)


def Main():
  """The main program function.

  Returns:
    bool: True if successful or False if not.
  """
  argument_parser = argparse.ArgumentParser(description=(
      'Export Digital Forensics artifact definitions as documentation.'))

  argument_parser.add_argument(
      '--artifact_definitions', '--artifact-definitions',
      dest='artifact_definitions', type=str, metavar='PATH', action='store',
      help=('Path to a directory or file containing the artifact definition '
            '.yaml files.'))

  argument_parser.add_argument(
      '--output', dest='output', action='store', metavar='./artifacts-kb/',
      default=None, help='Directory to write the output to.')

  options = argument_parser.parse_args()

  artifact_definitions = options.artifact_definitions
  if not artifact_definitions:
    artifact_definitions = os.path.join(
        os.path.dirname(artifacts.__file__), 'data')
    if not os.path.exists(artifact_definitions):
      artifact_definitions = os.path.join('/', 'usr', 'share', 'artifacts')
    if not os.path.exists(artifact_definitions):
      artifact_definitions = None

  if not artifact_definitions:
    print('Path to artifact definitions is missing.')
    print('')
    argument_parser.print_help()
    print('')
    return False

  if options.output:
    if not os.path.exists(options.output):
      os.mkdir(options.output)

    if not os.path.isdir(options.output):
      print(f'{options.output:s} must be a directory')
      print('')
      return False

  logging.basicConfig(
      level=logging.INFO, format='[%(levelname)s] %(message)s')

  registry = artifacts_registry.ArtifactDefinitionsRegistry()
  reader = artifacts_reader.YamlArtifactsReader()

  if os.path.isdir(artifact_definitions):
    registry.ReadFromDirectory(reader, artifact_definitions)
  elif os.path.isfile(artifact_definitions):
    registry.ReadFromFile(reader, artifact_definitions)

  # TODO: add document output writer.

  output_writer = StdoutOutputWriter()

  if not output_writer.Open():
    print('Unable to open output writer.')
    print('')
    return False

  try:
    for artifact_definition in sorted(
        registry.GetDefinitions(),
        key=lambda definition: definition.name.lower()):
      output_writer.WriteDefinition(artifact_definition)

      # TODO: output artifact definition details.

  finally:
    output_writer.Close()

  return True


if __name__ == '__main__':
  if not Main():
    sys.exit(1)
  else:
    sys.exit(0)
