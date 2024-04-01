#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script to generate artifact definition documentation."""

import argparse
import logging
import os
import sys

import artifacts

from artifacts import definitions as artifacts_definitions
from artifacts import reader as artifacts_reader
from artifacts import registry as artifacts_registry


class IndexRstOutputWriter(object):
  """Index.rst output writer."""

  def __init__(self, path):
    """Initializes an index.rst output writer."""
    super(IndexRstOutputWriter, self).__init__()
    self._file_object = None
    self._path = path

  def __enter__(self):
    """Make this work with the 'with' statement."""
    self._file_object = open(self._path, 'w', encoding='utf-8')

    text = '\n'.join([
        '#####################################',
        'Digital Forensics Artifact definition',
        '#####################################',
        '',
        '.. toctree::',
        '   :maxdepth: 1',
        '',
        ''])
    self._file_object.write(text)

    return self

  def __exit__(self, exception_type, value, traceback):
    """Make this work with the 'with' statement."""
    self._file_object.close()
    self._file_object = None

  def WriteArtifactDefinition(self, artifact_name):
    """Writes an artifact definition to the index.rst file.

    Args:
      artifact_name (str): artifact name.
    """
    self._file_object.write(
        f'   {artifact_name:s} <{artifact_name:s}>\n')


class MarkdownOutputWriter(object):
  """Markdown output writer."""

  _URL_PREFIX = 'https://artifacts-kb.readthedocs.io/en/latest/sources/'

  def __init__(self, path):
    """Initializes a Markdown output writer."""
    super(MarkdownOutputWriter, self).__init__()
    self._file_object = None
    self._path = path

  def __enter__(self):
    """Make this work with the 'with' statement."""
    self._file_object = open(self._path, 'w', encoding='utf-8')
    return self

  def __exit__(self, exception_type, value, traceback):
    """Make this work with the 'with' statement."""
    self._file_object.close()
    self._file_object = None

  def WriteArtifactDefinition(self, artifact_definition):
    """Writes an artifact definition to a Markdown file.

    Args:
      artifact_definition (list[artifacs.ArtifactDefinition]): artifact
          definition.
    """
    lines = [
        f'## {artifact_definition.name:s}',
        '',
        artifact_definition.description,
        '']

    for source in sorted(
        artifact_definition.sources, key=lambda source: source.supported_os):
      if source.type_indicator in (
          artifacts_definitions.TYPE_INDICATOR_FILE,
          artifacts_definitions.TYPE_INDICATOR_PATH):

        supported_os = ', '.join(
            source.supported_os or artifact_definition.supported_os)

        lines.extend([
            f'Paths on: {supported_os:s}',
            '',
            '```'])

        for path in sorted(source.paths):
          lines.append(path)

        lines.extend([
            '```',
            ''])

      if source.type_indicator == (
              artifacts_definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_KEY):
        lines.append('```')
        for key_path in sorted(source.keys):
          lines.append(key_path)

        lines.extend([
            '```',
            ''])

    if artifact_definition.urls:
      lines.extend([
          '### References',
          ''])

      for url in artifact_definition.urls:
        if url.startswith(self._URL_PREFIX) and url.endswith('.html'):
          url = url[len(self._URL_PREFIX):-5]
          url = f'../{url:s}.md'

        lines.append(f'* {url:s}')

    lines.extend([
        '',
        ''])

    text = '\n'.join(lines)
    self._file_object.write(text)


def Main():
  """Entry point of console script to generate documentation.

  Returns:
    int: exit code that is provided to sys.exit().
  """
  argument_parser = argparse.ArgumentParser(description=(
      'Generated artifact definition documentation.'))

  argument_parser.add_argument(
      '--artifact_definitions', '--artifact-definitions',
      dest='artifact_definitions', type=str, metavar='PATH', action='store',
      help=('Path to a directory or file containing the artifact definition '
            '.yaml files.'))

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
    print('Missing artifact definitions.')
    print('')
    argument_parser.print_help()
    print('')
    return 1

  logging.basicConfig(
      level=logging.INFO, format='[%(levelname)s] %(message)s')

  registry = artifacts_registry.ArtifactDefinitionsRegistry()
  reader = artifacts_reader.YamlArtifactsReader()

  if os.path.isdir(artifact_definitions):
    registry.ReadFromDirectory(reader, artifact_definitions)
  elif os.path.isfile(artifact_definitions):
    registry.ReadFromFile(reader, artifact_definitions)

  output_directory = os.path.join('docs', 'sources', 'definitions')
  os.makedirs(output_directory, exist_ok=True)

  index_rst_file_path = os.path.join(output_directory, 'index.rst')
  with IndexRstOutputWriter(index_rst_file_path) as index_rst_writer:
    for artifact_definition in sorted(
        registry.GetDefinitions(), key=lambda definition: definition.name):
      markdown_file_path = os.path.join(
          output_directory, f'{artifact_definition.name:s}.md')
      with MarkdownOutputWriter(markdown_file_path) as markdown_writer:
        markdown_writer.WriteArtifactDefinition(artifact_definition)

      index_rst_writer.WriteArtifactDefinition(artifact_definition.name)

  return 0


if __name__ == '__main__':
  sys.exit(Main())
