# -*- coding: utf-8 -*-
"""Shared test case."""

import os
import shutil
import tempfile
import unittest


# The path to top of the winevt-kb source tree.
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# The paths below are all derived from the project path directory.
# They are enumerated explicitly here so that they can be overwritten for
# compatibility with different build systems.
TEST_DATA_PATH = os.path.join(PROJECT_PATH, 'test_data')


class BaseTestCase(unittest.TestCase):
  """The base test case."""

  # Show full diff results, part of TestCase so does not follow our naming
  # conventions.
  maxDiff = None

  def _GetTestFilePath(self, path_segments):
    """Retrieves the path of a test file in the test data directory.

    Args:
      path_segments (list[str]): path segments inside the test data directory.

    Returns:
      str: path of the test file.
    """
    # Note that we need to pass the individual path segments to os.path.join
    # and not a list.
    return os.path.join(TEST_DATA_PATH, *path_segments)

  def _SkipIfPathNotExists(self, path):
    """Skips the test if the path does not exist.

    Args:
      path (str): path of a test file.

    Raises:
      SkipTest: if the path does not exist and the test should be skipped.
    """
    if not os.path.exists(path):
      filename = os.path.basename(path)
      raise unittest.SkipTest(f'missing test file: {filename:s}')


class TempDirectory(object):
  """Class that implements a temporary directory."""

  def __init__(self):
    """Initializes a temporary directory."""
    super(TempDirectory, self).__init__()
    self.name = ''

  def __enter__(self):
    """Make this work with the 'with' statement."""
    self.name = tempfile.mkdtemp()
    return self.name

  def __exit__(self, unused_type, unused_value, unused_traceback):
    """Make this work with the 'with' statement."""
    shutil.rmtree(self.name, True)
