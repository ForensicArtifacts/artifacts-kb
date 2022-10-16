# -*- coding: utf-8 -*-
"""Windows Message Resource file."""

import logging

import pyexe
import pywrc


# pylint: disable=logging-format-interpolation

class MessageResourceFile(object):
  """Windows Message Resource file.

  Attributes:
    windows_path (str): Windows path of the message resource file.
  """

  _STRING_TABLE_RESOURCE_IDENTIFIER = 0x06
  _MESSAGE_TABLE_RESOURCE_IDENTIFIER = 0x0b
  _VERSION_INFORMATION_RESOURCE_IDENTIFIER = 0x10

  def __init__(
      self, windows_path, ascii_codepage='cp1252',
      preferred_language_identifier=0x0409):
    """Initializes the Windows Message Resource file.

    Args:
      windows_path (str): normalized version of the Windows path.
      ascii_codepage (Optional[str]): ASCII string codepage.
      preferred_language_identifier (Optional[int]): preferred language
          identifier (LCID).
    """
    super(MessageResourceFile, self).__init__()
    self._ascii_codepage = ascii_codepage
    self._exe_file = pyexe.file()
    self._exe_file.set_ascii_codepage(self._ascii_codepage)
    self._exe_section = None
    self._file_object = None
    self._file_version = None
    self._is_open = False
    self._preferred_language_identifier = preferred_language_identifier
    self._product_version = None
    # TODO: wrc stream set codepage?
    self._wrc_stream = pywrc.stream()

    self.windows_path = windows_path

  def _GetVersionInformation(self):
    """Determines the file and product version."""
    version_information_resource = self._GetVersionInformationResource()
    if not version_information_resource:
      return

    file_version = version_information_resource.file_version
    major_version = (file_version >> 48) & 0xffff
    minor_version = (file_version >> 32) & 0xffff
    build_number = (file_version >> 16) & 0xffff
    revision_number = file_version & 0xffff

    self._file_version = (
        f'{major_version:d}.{minor_version:d}.{build_number:d}.'
        f'{revision_number:d}')

    product_version = version_information_resource.product_version
    major_version = (product_version >> 48) & 0xffff
    minor_version = (product_version >> 32) & 0xffff
    build_number = (product_version >> 16) & 0xffff
    revision_number = product_version & 0xffff

    self._product_version = (
        f'{major_version:d}.{minor_version:d}.{build_number:d}.'
        f'{revision_number:d}')

    if file_version != product_version:
      logging.warning((
          f'Mismatch between file version: {self._file_version:s} and product '
          f'version: {self._product_version:s} in message file: '
          f'{self.windows_path:s}.'))

  def _GetVersionInformationResource(self):
    """Retrieves the version information resource.

    Returns:
      pywrc.version_information_resource: version information resource or None
          if not available.
    """
    preferred_wrc_resource_sub_item = None

    wrc_resource = self._wrc_stream.get_resource_by_identifier(
        self._VERSION_INFORMATION_RESOURCE_IDENTIFIER)
    if wrc_resource:
      first_wrc_resource_sub_item = None
      for wrc_resource_item in wrc_resource.items:
        for wrc_resource_sub_item in wrc_resource_item.sub_items:
          if not first_wrc_resource_sub_item:
            first_wrc_resource_sub_item = wrc_resource_sub_item

          language_identifier = wrc_resource_sub_item.identifier
          if language_identifier == self._preferred_language_identifier:
            if not preferred_wrc_resource_sub_item:
              preferred_wrc_resource_sub_item = wrc_resource_sub_item

      if not preferred_wrc_resource_sub_item:
        preferred_wrc_resource_sub_item = first_wrc_resource_sub_item

    if not preferred_wrc_resource_sub_item:
      return None

    resource_data = preferred_wrc_resource_sub_item.read()

    version_information_resource = pywrc.version_information_resource()
    version_information_resource.copy_from_byte_stream(resource_data)

    return version_information_resource

  @property
  def file_version(self):
    """str: the file version."""
    if self._file_version is None:
      self._GetVersionInformation()
    return self._file_version

  @property
  def product_version(self):
    """str: the product version."""
    if self._product_version is None:
      self._GetVersionInformation()
    return self._product_version

  def Close(self):
    """Closes the Windows Message Resource file.

    Raises:
      IOError: if not open.
      OSError: if not open.
    """
    if not self._is_open:
      raise IOError('Not opened.')

    if self._exe_section:
      self._wrc_stream.close()

    self._exe_file.close()
    self._file_object = None
    self._is_open = False

  def GetMessageTableResource(self):
    """Retrieves the message table resource.

    Returns:
      pywrc.resource: resource containing the message table resource or None
          if not available.
    """
    return self._wrc_stream.get_resource_by_identifier(
        self._MESSAGE_TABLE_RESOURCE_IDENTIFIER)

  def GetMUILanguage(self):
    """Retrieves the MUI language.

    Returns:
      str: MUI language or None if not available.
    """
    mui_resource = self.GetMUIResource()
    if not mui_resource:
      return None

    return mui_resource.language

  def GetMUIResource(self):
    """Retrieves the MUI resource.

    Returns:
      pywrc.mui_resource: MUI resource or None if not available.
    """
    preferred_wrc_resource_sub_item = None

    wrc_resource = self._wrc_stream.get_resource_by_name('MUI')
    if wrc_resource:
      first_wrc_resource_sub_item = None
      for wrc_resource_item in wrc_resource.items:
        for wrc_resource_sub_item in wrc_resource_item.sub_items:
          if not first_wrc_resource_sub_item:
            first_wrc_resource_sub_item = wrc_resource_sub_item

          language_identifier = wrc_resource_sub_item.identifier
          if language_identifier == self._preferred_language_identifier:
            if not preferred_wrc_resource_sub_item:
              preferred_wrc_resource_sub_item = wrc_resource_sub_item

      if not preferred_wrc_resource_sub_item:
        preferred_wrc_resource_sub_item = first_wrc_resource_sub_item

    if not preferred_wrc_resource_sub_item:
      return None

    resource_data = preferred_wrc_resource_sub_item.read()

    mui_resource = pywrc.mui_resource()
    mui_resource.copy_from_byte_stream(resource_data)

    return mui_resource

  def GetStringTableResource(self):
    """Retrieves the string table resource.

    Returns:
      pywrc.resource: resource containing the string table resource or None
          if not available.
    """
    return self._wrc_stream.get_resource_by_identifier(
        self._STRING_TABLE_RESOURCE_IDENTIFIER)

  def HasMessageTableResource(self):
    """Determines if the resource file as a message table resource.

    Returns:
      bool: True if the resource file as a message table resource.
    """
    wrc_resource = None
    if self._wrc_stream:
      try:
        wrc_resource = self._wrc_stream.get_resource_by_identifier(
            self._MESSAGE_TABLE_RESOURCE_IDENTIFIER)
      except IOError:
        pass

    return bool(wrc_resource)

  def HasStringTableResource(self):
    """Determines if the resource file as a string table resource.

    Returns:
      bool: True if the resource file as a string table resource.
    """
    wrc_resource = None
    if self._wrc_stream:
      try:
        wrc_resource = self._wrc_stream.get_resource_by_identifier(
            self._STRING_TABLE_RESOURCE_IDENTIFIER)
      except IOError:
        pass

    return bool(wrc_resource)

  def OpenFileObject(self, file_object):
    """Opens the Windows Message Resource file using a file-like object.

    Args:
      file_object (file): file-like object.

    Raises:
      IOError: if already open.
      OSError: if already open.
    """
    if self._is_open:
      raise IOError('Already open.')

    self._exe_file.open_file_object(file_object)
    self._exe_section = self._exe_file.get_section_by_name('.rsrc')

    if self._exe_section:
      self._wrc_stream.set_virtual_address(self._exe_section.virtual_address)
      self._wrc_stream.open_file_object(self._exe_section)

    self._file_object = file_object
    self._is_open = True
