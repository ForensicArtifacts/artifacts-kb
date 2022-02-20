# -*- coding: utf-8 -*-
"""Volume scanner for artifact definitions."""

import logging
import os
import yaml

from dfimagetools import artifact_filters
from dfimagetools import environment_variables
from dfimagetools import windows_registry

from dfvfs.helpers import file_system_searcher as dfvfs_file_system_searcher
from dfvfs.helpers import volume_scanner as dfvfs_volume_scanner
from dfvfs.helpers import windows_path_resolver as dfvfs_windows_path_resolver
from dfvfs.lib import definitions as dfvfs_definitions
from dfvfs.resolver import resolver as dfvfs_resolver

from dfwinreg import registry as dfwinreg_registry

from dtfabric import errors as dtfabric_errors
from dtfabric.runtime import fabric as dtfabric_fabric

from artifactsrc import resource_file


class CheckResults(object):
  """Check results.

  Attributes:
    data_formats (set[str]): data formats that were found.
    number_of_file_entries (int): number of file entries that were found.
  """

  def __init__(self):
    """Initializes check results."""
    super(CheckResults, self).__init__()
    self.data_formats = set()
    self.number_of_file_entries = 0


class ArtifactDefinitionsVolumeScanner(dfvfs_volume_scanner.VolumeScanner):
  """Artifact definitions volume scanner."""

  # Preserve the absolute path value of __file__ in case it is changed
  # at run-time.
  _DEFINITION_FILES_PATH = os.path.dirname(__file__)

  _WINDOWS_DIRECTORIES = frozenset([
      'C:\\Windows',
      'C:\\WINNT',
      'C:\\WTSRV',
      'C:\\WINNT35',
  ])

  _FORMAT_VERSION_STRING = {
      'esedb': 'esedb 0x{format_version:x}',
      'evt': 'evt {major_format_version:d}.{minor_format_version:d}',
      'evtx': 'evtx {major_format_version:d}.{minor_format_version:d}',
      'job': 'job {format_version:d}',
      'regf': 'regf {major_format_version:d}.{minor_format_version:d}',
      'scca': 'scca {format_version:d}',
  }

  def __init__(self, artifacts_registry, mediator=None):
    """Initializes a Windows Registry collector.

    Args:
      artifacts_registry (artifacts.ArtifactDefinitionsRegistry): artifact
          definitions registry.
      mediator (Optional[dfvfs.VolumeScannerMediator]): a volume scanner
          mediator.
    """
    super(ArtifactDefinitionsVolumeScanner, self).__init__(mediator=mediator)
    self._ascii_codepage = 'cp1252'
    self._artifacts_registry = artifacts_registry
    self._checks_definitions = None
    self._data_location = os.path.join('data')
    self._data_type_fabric = self._ReadDataTypeFabricDefinitionFile(
        'formats.yaml')
    self._data_type_maps = {}
    self._environment_variables = []
    self._file_system = None
    self._file_system_searcher = None
    self._filter_generator = None
    self._mount_point = None
    self._path_resolver = None
    self._preferred_language_identifier = 'en-US'
    self._windows_directory = None
    self._windows_registry = None

  def _DetermineDataFormat(self, names, file_object):
    """Determines the data format.

    Args:
      names (list[str]): names of data formats to check.
      file_object (file): file-like object.

    Returns:
      str: data format identifier or None if the data format coudld not
          be determined.
    """
    for name in names:
      format_data_type_map = self._GetDataTypeMap(name)

      layout = getattr(format_data_type_map, 'layout', None)
      if not layout:
        continue

      layout_element_definition = layout[0]
      if layout_element_definition.offset is None:
        continue

      data_type_map = self._GetDataTypeMap(
          layout_element_definition.data_type)

      structure_values = self._ReadStructureFromFileObject(
          file_object, layout_element_definition.offset, data_type_map)
      if structure_values:
        format_string = self._FORMAT_VERSION_STRING.get(name, name)
        return format_string.format(**structure_values.__dict__)

    return None

  def _GetDataTypeMap(self, name):
    """Retrieves a data type map defined by the definition file.

    The data type maps are cached for reuse.

    Args:
      name (str): name of the data type as defined by the definition file.

    Returns:
      dtfabric.DataTypeMap: data type map which contains a data type definition,
          such as a structure, that can be mapped onto binary data.
    """
    data_type_map = self._data_type_maps.get(name, None)
    if not data_type_map:
      data_type_map = self._data_type_fabric.CreateDataTypeMap(name)
      self._data_type_maps[name] = data_type_map

    return data_type_map

  def _OpenMessageResourceFile(self, windows_path):
    """Opens the message resource file specified by the Windows path.

    Args:
      windows_path (str): Windows path containing the message resource
          filename.

    Returns:
      MessageResourceFile: message resource file or None.
    """
    path_spec = self._path_resolver.ResolvePath(windows_path)
    if path_spec is None:
      return None

    return self._OpenMessageResourceFileByPathSpec(path_spec)

  def _OpenMessageResourceFileByPathSpec(self, path_spec):
    """Opens the message resource file specified by the path specification.

    Args:
      path_spec (dfvfs.PathSpec): path specification.

    Returns:
      MessageResourceFile: message resource file or None.
    """
    windows_path = self._path_resolver.GetWindowsPath(path_spec)
    if windows_path is None:
      logging.warning('Unable to retrieve Windows path.')

    try:
      file_object = dfvfs_resolver.Resolver.OpenFileObject(path_spec)
    except IOError as exception:
      logging.warning('Unable to open: {0:s} with error: {1!s}'.format(
          path_spec.comparable, exception))
      file_object = None

    if file_object is None:
      return None

    message_file = resource_file.MessageResourceFile(
        windows_path, ascii_codepage=self._ascii_codepage,
        preferred_language_identifier=self._preferred_language_identifier)
    message_file.OpenFileObject(file_object)

    return message_file

  def _ReadChecksDefinitions(self):
    """Reads the checks definitions from checks.yaml.

    Returns:
      list[dict[str, object]]: checks definitions.
    """
    check_definitions = {}

    path = os.path.join(self._data_location, 'checks.yaml')
    with open(path, 'r', encoding='utf-8') as file_object:
      for check_definition in yaml.safe_load_all(file_object):
        name = check_definition.get('name', None)
        if name:
          check_definitions[name.lower()] = check_definition

    return check_definitions

  def _ReadDataTypeFabricDefinitionFile(self, filename):
    """Reads a dtFabric definition file.

    Args:
      filename (str): name of the dtFabric definition file.

    Returns:
      dtfabric.DataTypeFabric: data type fabric which contains the data format
          data type maps of the data type definition, such as a structure, that
          can be mapped onto binary data or None if no filename is provided.
    """
    if not filename:
      return None

    path = os.path.join(self._DEFINITION_FILES_PATH, filename)
    with open(path, 'rb') as file_object:
      definition = file_object.read()

    return dtfabric_fabric.DataTypeFabric(yaml_definition=definition)

  def _ReadStructureFromFileObject(
      self, file_object, file_offset, data_type_map):
    """Reads a structure from a file-like object.

    This method currently only supports fixed-size structures.

    Args:
      file_object (file): a file-like object to parse.
      file_offset (int): offset of the structure data relative to the start
          of the file-like object.
      data_type_map (dtfabric.DataTypeMap): data type map of the structure.

    Returns:
      object: structure values object or None if the structure cannot be read.
    """
    structure_values = None

    data_size = data_type_map.GetSizeHint()
    if data_size:
      file_object.seek(file_offset, os.SEEK_SET)
      try:
        data = file_object.read(data_size)
        structure_values = data_type_map.MapByteStream(data)
      except (dtfabric_errors.ByteStreamTooSmallError,
              dtfabric_errors.MappingError):
        pass

    return structure_values

  def CheckArtifactDefinition(self, artifact_definition):
    """Checks if an artifact definition on a storage media image.

    Args:
      artifact_definition (artifacts.ArtifactDefinition): artifact definition.

    Returns:
      CheckResults: check results.
    """
    check_result = CheckResults()

    if self._checks_definitions is None:
      self._checks_definitions = self._ReadChecksDefinitions()

    find_specs = list(self._filter_generator.GetFindSpecs(
        [artifact_definition.name]))
    if find_specs:
      path_specs = list(self._file_system_searcher.Find(find_specs=find_specs))
      check_result.number_of_file_entries = len(path_specs)

      check_definition = self._checks_definitions.get(
          artifact_definition.name.lower(), None)
      if check_definition:
        for path_spec in path_specs:
          file_entry = self._file_system.GetFileEntryByPathSpec(path_spec)
          if file_entry.size > 0:
            file_object = file_entry.GetFileObject()
            if file_object:
              formats = check_definition.get('formats', [])
              data_format = self._DetermineDataFormat(formats, file_object)
              check_result.data_formats.add(data_format or 'unknown')

    return check_result

  def GetWindowsVersion(self):
    """Determines the Windows version from kernel executable file.

    Returns:
      str: Windows version or None otherwise.
    """
    # Window NT variants.
    kernel_executable_path = '\\'.join([
        self._windows_directory, 'System32', 'ntoskrnl.exe'])
    message_file = self._OpenMessageResourceFile(kernel_executable_path)

    if not message_file:
      # Window 9x variants.
      kernel_executable_path = '\\'.join([
          self._windows_directory, 'System32', '\\kernel32.dll'])
      message_file = self._OpenMessageResourceFile(kernel_executable_path)

    if not message_file:
      return None

    return message_file.file_version

  def ScanForOperatingSystemVolumes(self, source_path, options=None):
    """Scans for volumes containing an operating system.

    Args:
      source_path (str): source path.
      options (Optional[dfvfs.VolumeScannerOptions]): volume scanner options.
          If None the default volume scanner options are used, which are defined
          in the VolumeScannerOptions class.

    Returns:
      bool: True if a volume with an operating system was found.

    Raises:
      ScannerError: if the source path does not exists, or if the source path
          is not a file or directory, or if the format of or within the source
          file is not supported.
    """
    if not options:
      options = dfvfs_volume_scanner.VolumeScannerOptions()

    scan_context = self._ScanSource(source_path)

    self._source_path = source_path
    self._source_type = scan_context.source_type

    base_path_specs = self._GetBasePathSpecs(scan_context, options)

    if (not base_path_specs or
        scan_context.source_type == dfvfs_definitions.SOURCE_TYPE_FILE):
      return False

    for path_spec in base_path_specs:
      file_system = dfvfs_resolver.Resolver.OpenFileSystem(path_spec)

      if path_spec.type_indicator == dfvfs_definitions.TYPE_INDICATOR_OS:
        mount_point = path_spec
      else:
        mount_point = path_spec.parent

      path_resolver = dfvfs_windows_path_resolver.WindowsPathResolver(
          file_system, mount_point)

      windows_directory = None
      for windows_path in self._WINDOWS_DIRECTORIES:
        windows_path_spec = path_resolver.ResolvePath(windows_path)
        if windows_path_spec is not None:
          windows_directory = windows_path
          break

      if windows_directory:
        path_resolver.SetEnvironmentVariable('SystemRoot', windows_directory)
        path_resolver.SetEnvironmentVariable('WinDir', windows_directory)

        registry_file_reader = (
            windows_registry.StorageMediaImageWindowsRegistryFileReader(
                file_system, path_resolver))
        winregistry = dfwinreg_registry.WinRegistry(
            registry_file_reader=registry_file_reader)

        collector = environment_variables.WindowsEnvironmentVariablesCollector()

        self._environment_variables = list(collector.Collect(winregistry))
        self._file_system = file_system
        self._mount_point = mount_point
        self._path_resolver = path_resolver
        self._windows_directory = windows_directory
        self._windows_registry = winregistry

    self._filter_generator = (
        artifact_filters.ArtifactDefinitionFiltersGenerator(
            self._artifacts_registry, self._environment_variables, []))

    self._file_system_searcher = dfvfs_file_system_searcher.FileSystemSearcher(
        self._file_system, self._mount_point)

    return True
