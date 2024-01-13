#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the Windows Message Resource (WRC) file class."""

import unittest

from artifactsrc import resource_file

from tests import test_lib


class TestWrcResource(object):
  """Windows Resource Compiler (WRC) resource for testing.

  Attributes:
    items (list[TestWrcResourceItem]): resources items.
  """

  def __init__(self):
    """Initializes a resource."""
    super(TestWrcResource, self).__init__()
    self.items = []

  # pylint: disable=invalid-name

  def get_number_of_items(self):
    """Retrieves the number of resource items.

    Returns:
      int: number of resource items.
    """
    return len(self.items)

  def get_item_by_index(self, index):
    """Retrieves a specific resource item.

    Args:
      index (int): index.

    Returns:
      TestWrcResourceItem: resource item.
    """
    return self.items[index]


class TestWrcResourceItem(object):
  """Windows Resource Compiler (WRC) resource item for testing.

  Attributes:
    identifier (int]): identifier.
    sub_items (list[TestWrcResourceItem]): resources sub items.
  """

  def __init__(self, identifier):
    """Initializes a resource item.

    Args:
      identifier (int]): identifier.
    """
    super(TestWrcResourceItem, self).__init__()
    self.identifier = identifier
    self.resource_data = None
    self.sub_items = []

  # pylint: disable=invalid-name

  def get_number_of_sub_items(self):
    """Retrieves the number of resource sub items.

    Returns:
      int: number of resource sub items.
    """
    return len(self.sub_items)

  def get_sub_item_by_index(self, index):
    """Retrieves a specific resource sub item.

    Args:
      index (int): index.

    Returns:
      TestWrcResourceItem: resource item.
    """
    return self.sub_items[index]

  def read(self):
    """Reads the resource data.

    Returns:
      bytes: resource data.
    """
    return self.resource_data


class TestWrcStream(object):
  """Windows Resource Compiler (WRC) stream for testing.

  Attributes:
    resources (dict[int|str, object]): resources per identifier.
  """

  def __init__(self):
    """Initializes a stream."""
    super(TestWrcStream, self).__init__()
    self.resources = {}

  # pylint: disable=invalid-name

  def get_resource_by_identifier(self, identifier):
    """Retrieves a specific resource by identifier.

    Args:
      identifier (int): identifier.

    Returns:
      object: resource or None.
    """
    return self.resources.get(identifier, None)

  def get_resource_by_name(self, name):
    """Retrieves a specific resource by name.

    Args:
      name (str): name.

    Returns:
      object: resource or None.
    """
    return self.resources.get(name, None)


class MessageResourceFileTest(test_lib.BaseTestCase):
  """Tests for the Windows Message Resource file object."""

  # pylint: disable=protected-access

  _VERSION_INFORMATION_RESOURCE_DATA = bytes(bytearray([
      0xfc, 0x02, 0x34, 0x00, 0x00, 0x00, 0x56, 0x00, 0x53, 0x00, 0x5f, 0x00,
      0x56, 0x00, 0x45, 0x00, 0x52, 0x00, 0x53, 0x00, 0x49, 0x00, 0x4f, 0x00,
      0x4e, 0x00, 0x5f, 0x00, 0x49, 0x00, 0x4e, 0x00, 0x46, 0x00, 0x4f, 0x00,
      0x00, 0x00, 0x00, 0x00, 0xbd, 0x04, 0xef, 0xfe, 0x00, 0x00, 0x01, 0x00,
      0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00,
      0x00, 0x00, 0x00, 0x00, 0x3f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
      0x04, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
      0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5c, 0x02, 0x00, 0x00,
      0x01, 0x00, 0x53, 0x00, 0x74, 0x00, 0x72, 0x00, 0x69, 0x00, 0x6e, 0x00,
      0x67, 0x00, 0x46, 0x00, 0x69, 0x00, 0x6c, 0x00, 0x65, 0x00, 0x49, 0x00,
      0x6e, 0x00, 0x66, 0x00, 0x6f, 0x00, 0x00, 0x00, 0x38, 0x02, 0x00, 0x00,
      0x01, 0x00, 0x30, 0x00, 0x34, 0x00, 0x30, 0x00, 0x39, 0x00, 0x30, 0x00,
      0x34, 0x00, 0x65, 0x00, 0x34, 0x00, 0x00, 0x00, 0x2a, 0x00, 0x09, 0x00,
      0x01, 0x00, 0x43, 0x00, 0x6f, 0x00, 0x6d, 0x00, 0x6d, 0x00, 0x65, 0x00,
      0x6e, 0x00, 0x74, 0x00, 0x73, 0x00, 0x00, 0x00, 0x43, 0x00, 0x6f, 0x00,
      0x6d, 0x00, 0x6d, 0x00, 0x65, 0x00, 0x6e, 0x00, 0x74, 0x00, 0x73, 0x00,
      0x00, 0x00, 0x00, 0x00, 0x5e, 0x00, 0x1b, 0x00, 0x01, 0x00, 0x46, 0x00,
      0x69, 0x00, 0x6c, 0x00, 0x65, 0x00, 0x44, 0x00, 0x65, 0x00, 0x73, 0x00,
      0x63, 0x00, 0x72, 0x00, 0x69, 0x00, 0x70, 0x00, 0x74, 0x00, 0x69, 0x00,
      0x6f, 0x00, 0x6e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x57, 0x00, 0x69, 0x00,
      0x6e, 0x00, 0x64, 0x00, 0x6f, 0x00, 0x77, 0x00, 0x73, 0x00, 0x20, 0x00,
      0x52, 0x00, 0x65, 0x00, 0x73, 0x00, 0x6f, 0x00, 0x75, 0x00, 0x72, 0x00,
      0x63, 0x00, 0x65, 0x00, 0x20, 0x00, 0x74, 0x00, 0x65, 0x00, 0x73, 0x00,
      0x74, 0x00, 0x20, 0x00, 0x66, 0x00, 0x69, 0x00, 0x6c, 0x00, 0x65, 0x00,
      0x00, 0x00, 0x00, 0x00, 0x2c, 0x00, 0x06, 0x00, 0x01, 0x00, 0x46, 0x00,
      0x69, 0x00, 0x6c, 0x00, 0x65, 0x00, 0x56, 0x00, 0x65, 0x00, 0x72, 0x00,
      0x73, 0x00, 0x69, 0x00, 0x6f, 0x00, 0x6e, 0x00, 0x00, 0x00, 0x00, 0x00,
      0x31, 0x00, 0x2e, 0x00, 0x30, 0x00, 0x2e, 0x00, 0x30, 0x00, 0x00, 0x00,
      0x3a, 0x00, 0x0d, 0x00, 0x01, 0x00, 0x49, 0x00, 0x6e, 0x00, 0x74, 0x00,
      0x65, 0x00, 0x72, 0x00, 0x6e, 0x00, 0x61, 0x00, 0x6c, 0x00, 0x4e, 0x00,
      0x61, 0x00, 0x6d, 0x00, 0x65, 0x00, 0x00, 0x00, 0x77, 0x00, 0x72, 0x00,
      0x63, 0x00, 0x5f, 0x00, 0x74, 0x00, 0x65, 0x00, 0x73, 0x00, 0x74, 0x00,
      0x2e, 0x00, 0x64, 0x00, 0x6c, 0x00, 0x6c, 0x00, 0x00, 0x00, 0x00, 0x00,
      0x84, 0x00, 0x30, 0x00, 0x01, 0x00, 0x4c, 0x00, 0x65, 0x00, 0x67, 0x00,
      0x61, 0x00, 0x6c, 0x00, 0x43, 0x00, 0x6f, 0x00, 0x70, 0x00, 0x79, 0x00,
      0x72, 0x00, 0x69, 0x00, 0x67, 0x00, 0x68, 0x00, 0x74, 0x00, 0x00, 0x00,
      0x28, 0x00, 0x43, 0x00, 0x29, 0x00, 0x20, 0x00, 0x32, 0x00, 0x30, 0x00,
      0x31, 0x00, 0x37, 0x00, 0x2c, 0x00, 0x20, 0x00, 0x4a, 0x00, 0x6f, 0x00,
      0x61, 0x00, 0x63, 0x00, 0x68, 0x00, 0x69, 0x00, 0x6d, 0x00, 0x20, 0x00,
      0x4d, 0x00, 0x65, 0x00, 0x74, 0x00, 0x7a, 0x00, 0x20, 0x00, 0x3c, 0x00,
      0x6a, 0x00, 0x6f, 0x00, 0x61, 0x00, 0x63, 0x00, 0x68, 0x00, 0x69, 0x00,
      0x6d, 0x00, 0x2e, 0x00, 0x6d, 0x00, 0x65, 0x00, 0x74, 0x00, 0x7a, 0x00,
      0x40, 0x00, 0x67, 0x00, 0x6d, 0x00, 0x61, 0x00, 0x69, 0x00, 0x6c, 0x00,
      0x2e, 0x00, 0x63, 0x00, 0x6f, 0x00, 0x6d, 0x00, 0x3e, 0x00, 0x00, 0x00,
      0x42, 0x00, 0x0d, 0x00, 0x01, 0x00, 0x4f, 0x00, 0x72, 0x00, 0x69, 0x00,
      0x67, 0x00, 0x69, 0x00, 0x6e, 0x00, 0x61, 0x00, 0x6c, 0x00, 0x46, 0x00,
      0x69, 0x00, 0x6c, 0x00, 0x65, 0x00, 0x6e, 0x00, 0x61, 0x00, 0x6d, 0x00,
      0x65, 0x00, 0x00, 0x00, 0x77, 0x00, 0x72, 0x00, 0x63, 0x00, 0x5f, 0x00,
      0x74, 0x00, 0x65, 0x00, 0x73, 0x00, 0x74, 0x00, 0x2e, 0x00, 0x64, 0x00,
      0x6c, 0x00, 0x6c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x32, 0x00, 0x09, 0x00,
      0x01, 0x00, 0x50, 0x00, 0x72, 0x00, 0x6f, 0x00, 0x64, 0x00, 0x75, 0x00,
      0x63, 0x00, 0x74, 0x00, 0x4e, 0x00, 0x61, 0x00, 0x6d, 0x00, 0x65, 0x00,
      0x00, 0x00, 0x00, 0x00, 0x77, 0x00, 0x72, 0x00, 0x63, 0x00, 0x5f, 0x00,
      0x74, 0x00, 0x65, 0x00, 0x73, 0x00, 0x74, 0x00, 0x00, 0x00, 0x00, 0x00,
      0x30, 0x00, 0x06, 0x00, 0x01, 0x00, 0x50, 0x00, 0x72, 0x00, 0x6f, 0x00,
      0x64, 0x00, 0x75, 0x00, 0x63, 0x00, 0x74, 0x00, 0x56, 0x00, 0x65, 0x00,
      0x72, 0x00, 0x73, 0x00, 0x69, 0x00, 0x6f, 0x00, 0x6e, 0x00, 0x00, 0x00,
      0x31, 0x00, 0x2e, 0x00, 0x30, 0x00, 0x2e, 0x00, 0x30, 0x00, 0x00, 0x00,
      0x44, 0x00, 0x00, 0x00, 0x01, 0x00, 0x56, 0x00, 0x61, 0x00, 0x72, 0x00,
      0x46, 0x00, 0x69, 0x00, 0x6c, 0x00, 0x65, 0x00, 0x49, 0x00, 0x6e, 0x00,
      0x66, 0x00, 0x6f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x24, 0x00, 0x04, 0x00,
      0x00, 0x00, 0x54, 0x00, 0x72, 0x00, 0x61, 0x00, 0x6e, 0x00, 0x73, 0x00,
      0x6c, 0x00, 0x61, 0x00, 0x74, 0x00, 0x69, 0x00, 0x6f, 0x00, 0x6e, 0x00,
      0x00, 0x00, 0x00, 0x00, 0x09, 0x04, 0xe4, 0x04]))

  def testGetVersionInformationNoWrc(self):
    """Tests the _GetVersionInformation function."""
    test_file_path = self._GetTestFilePath(['nowrc_test.dll'])
    self._SkipIfPathNotExists(test_file_path)

    message_resource_file = resource_file.MessageResourceFile(
        'C:\\Windows\\System32\\nowrc_test.dll')

    with open(test_file_path, 'rb') as file_object:
      message_resource_file.OpenFileObject(file_object)

      try:
        resource = message_resource_file._GetVersionInformation()
        self.assertIsNone(resource)

      finally:
        message_resource_file.Close()

  def testGetVersionInformationWrc(self):
    """Tests the _GetVersionInformation function."""
    test_file_path = self._GetTestFilePath(['wrc_test.dll'])
    self._SkipIfPathNotExists(test_file_path)

    message_resource_file = resource_file.MessageResourceFile(
        'C:\\Windows\\System32\\wrc_test.dll')

    with open(test_file_path, 'rb') as file_object:
      message_resource_file.OpenFileObject(file_object)

      message_resource_file._GetVersionInformation()

      self.assertEqual(message_resource_file.file_version, '1.0.0.0')
      self.assertEqual(message_resource_file.product_version, '1.0.0.0')

      message_resource_file.Close()

    message_resource_file = resource_file.MessageResourceFile(
        'C:\\Windows\\System32\\test.dll')

    # Test with an empty WRC stream.
    wrc_stream = TestWrcStream()
    message_resource_file._wrc_stream = wrc_stream

    message_resource_file._GetVersionInformation()
    self.assertIsNone(message_resource_file.file_version)
    self.assertIsNone(message_resource_file.product_version)

    # Test with empty version information.
    wrc_resource = TestWrcResource()
    wrc_stream.resources[0x10] = wrc_resource

    wrc_resource_item = TestWrcResourceItem(1)
    wrc_resource.items.append(wrc_resource_item)

    wrc_resource_sub_item = TestWrcResourceItem(0x409)
    wrc_resource_item.sub_items.append(wrc_resource_sub_item)

    wrc_resource_sub_item.resource_data = (
        self._VERSION_INFORMATION_RESOURCE_DATA)

    message_resource_file._GetVersionInformation()
    self.assertEqual(message_resource_file.file_version, '0.0.0.0')
    self.assertEqual(message_resource_file.product_version, '2.0.0.0')

  def testGetVersionInformationResourceNoWrc(self):
    """Tests the _GetVersionInformationResource function."""
    test_file_path = self._GetTestFilePath(['nowrc_test.dll'])
    self._SkipIfPathNotExists(test_file_path)

    message_resource_file = resource_file.MessageResourceFile(
        'C:\\Windows\\System32\\nowrc_test.dll')

    with open(test_file_path, 'rb') as file_object:
      message_resource_file.OpenFileObject(file_object)

      version_information_resource = (
          message_resource_file._GetVersionInformationResource())

      self.assertIsNone(version_information_resource)

      message_resource_file.Close()

  def testGetVersionInformationResourceWrc(self):
    """Tests the _GetVersionInformationResource function."""
    test_file_path = self._GetTestFilePath(['wrc_test.dll'])
    self._SkipIfPathNotExists(test_file_path)

    message_resource_file = resource_file.MessageResourceFile(
        'C:\\Windows\\System32\\wrc_test.dll')

    with open(test_file_path, 'rb') as file_object:
      message_resource_file.OpenFileObject(file_object)

      version_information_resource = (
          message_resource_file._GetVersionInformationResource())

      self.assertIsNotNone(version_information_resource)

      message_resource_file.Close()

  def testFileVersionProperty(self):
    """Tests the file_version property."""
    test_file_path = self._GetTestFilePath(['wrc_test.dll'])
    self._SkipIfPathNotExists(test_file_path)

    message_resource_file = resource_file.MessageResourceFile(
        'C:\\Windows\\System32\\wrc_test.dll')

    with open(test_file_path, 'rb') as file_object:
      message_resource_file.OpenFileObject(file_object)

      self.assertEqual(message_resource_file.file_version, '1.0.0.0')

      message_resource_file.Close()

  def testProductVersionProperty(self):
    """Tests the product_version property."""
    test_file_path = self._GetTestFilePath(['wrc_test.dll'])
    self._SkipIfPathNotExists(test_file_path)

    message_resource_file = resource_file.MessageResourceFile(
        'C:\\Windows\\System32\\wrc_test.dll')

    with open(test_file_path, 'rb') as file_object:
      message_resource_file.OpenFileObject(file_object)

      self.assertEqual(message_resource_file.product_version, '1.0.0.0')

      message_resource_file.Close()

  # TODO: add open/close test on non PE/COFF file.

  def testOpenFileObjectAndCloseNoWrc(self):
    """Tests the OpenFileObject and Close functions."""
    test_file_path = self._GetTestFilePath(['nowrc_test.dll'])
    self._SkipIfPathNotExists(test_file_path)

    message_resource_file = resource_file.MessageResourceFile(
        'C:\\Windows\\System32\\nowrc_test.dll')

    with open(test_file_path, 'rb') as file_object:
      message_resource_file.OpenFileObject(file_object)

      with self.assertRaises(IOError):
        message_resource_file.OpenFileObject(file_object)

      message_resource_file.Close()

  def testOpenFileObjectAndCloseWrc(self):
    """Tests the OpenFileObject and Close functions."""
    test_file_path = self._GetTestFilePath(['wrc_test.dll'])
    self._SkipIfPathNotExists(test_file_path)

    message_resource_file = resource_file.MessageResourceFile(
        'C:\\Windows\\System32\\wrc_test.dll')

    with open(test_file_path, 'rb') as file_object:
      message_resource_file.OpenFileObject(file_object)

      with self.assertRaises(IOError):
        message_resource_file.OpenFileObject(file_object)

      message_resource_file.Close()

  def testGetMessageTableResourceNoWrc(self):
    """Tests the GetMessageTableResource function."""
    test_file_path = self._GetTestFilePath(['nowrc_test.dll'])
    self._SkipIfPathNotExists(test_file_path)

    message_resource_file = resource_file.MessageResourceFile(
        'C:\\Windows\\System32\\nowrc_test.dll')

    with open(test_file_path, 'rb') as file_object:
      message_resource_file.OpenFileObject(file_object)

      try:
        resource = message_resource_file.GetMessageTableResource()
        self.assertIsNone(resource)

      finally:
        message_resource_file.Close()

  def testGetMessageTableResourceWrc(self):
    """Tests the GetMessageTableResource function."""
    test_file_path = self._GetTestFilePath(['wrc_test.dll'])
    self._SkipIfPathNotExists(test_file_path)

    message_resource_file = resource_file.MessageResourceFile(
        'C:\\Windows\\System32\\wrc_test.dll')

    with open(test_file_path, 'rb') as file_object:
      message_resource_file.OpenFileObject(file_object)

      try:
        message_table_resource = message_resource_file.GetMessageTableResource()
        self.assertIsNotNone(message_table_resource)

      finally:
        message_resource_file.Close()

  def testGetMUILanguage(self):
    """Tests the GetMUILanguage function."""
    test_file_path = self._GetTestFilePath(['wrc_test.mui.dll'])
    self._SkipIfPathNotExists(test_file_path)

    message_resource_file = resource_file.MessageResourceFile(
        'C:\\Windows\\System32\\test.dll')

    with open(test_file_path, 'rb') as file_object:
      message_resource_file.OpenFileObject(file_object)

      mui_language = message_resource_file.GetMUILanguage()
      self.assertEqual(mui_language, 'en-US')

      message_resource_file.Close()

    # Test with an empty WRC stream.
    wrc_stream = TestWrcStream()

    message_resource_file._wrc_stream = wrc_stream

    mui_language = message_resource_file.GetMUILanguage()
    self.assertIsNone(mui_language)

  def testHasMessageTableResourceNoWrc(self):
    """Tests the HasMessageTableResource function."""
    test_file_path = self._GetTestFilePath(['nowrc_test.dll'])
    self._SkipIfPathNotExists(test_file_path)

    message_resource_file = resource_file.MessageResourceFile(
        'C:\\Windows\\System32\\nowrc_test.dll')

    with open(test_file_path, 'rb') as file_object:
      message_resource_file.OpenFileObject(file_object)

      try:
        result = message_resource_file.HasMessageTableResource()
        self.assertFalse(result)

      finally:
        message_resource_file.Close()

  def testHasMessageTableResourceWrc(self):
    """Tests the HasMessageTableResource function."""
    test_file_path = self._GetTestFilePath(['wrc_test.dll'])
    self._SkipIfPathNotExists(test_file_path)

    message_resource_file = resource_file.MessageResourceFile(
        'C:\\Windows\\System32\\wrc_test.dll')

    with open(test_file_path, 'rb') as file_object:
      message_resource_file.OpenFileObject(file_object)

      try:
        result = message_resource_file.HasMessageTableResource()
        self.assertTrue(result)

      finally:
        message_resource_file.Close()


if __name__ == '__main__':
  unittest.main()
