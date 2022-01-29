# -*- coding: utf-8 -*-
"""Volume scanner for artifact definitions."""

from dfimagetools import artifact_filters
from dfimagetools import environment_variables
from dfimagetools import windows_registry

from dfvfs.helpers import file_system_searcher as dfvfs_file_system_searcher
from dfvfs.helpers import volume_scanner as dfvfs_volume_scanner
from dfvfs.helpers import windows_path_resolver as dfvfs_windows_path_resolver
from dfvfs.lib import definitions as dfvfs_definitions
from dfvfs.resolver import resolver as dfvfs_resolver

from dfwinreg import registry as dfwinreg_registry


class ArtifactDefinitionsVolumeScanner(dfvfs_volume_scanner.VolumeScanner):
  """Artifact definitions volume scanner."""

  _WINDOWS_DIRECTORIES = frozenset([
      'C:\\Windows',
      'C:\\WINNT',
      'C:\\WTSRV',
      'C:\\WINNT35',
  ])

  def __init__(self, artifacts_registry, mediator=None):
    """Initializes a Windows Registry collector.

    Args:
      artifacts_registry (artifacts.ArtifactDefinitionsRegistry): artifact
          definitions registry.
      mediator (Optional[dfvfs.VolumeScannerMediator]): a volume scanner
          mediator.
    """
    super(ArtifactDefinitionsVolumeScanner, self).__init__(mediator=mediator)
    self._artifacts_registry = artifacts_registry
    self._environment_variables = []
    self._file_system = None
    self._file_system_searcher = None
    self._filter_generator = None
    self._mount_point = None
    self._path_resolver = None
    self._windows_registry = None

  def CheckArtifactDefinition(self, artifact_definition):
    """Checks if an artifact definition on a storage media image.

    Args:
      artifact_definition (artifacts.ArtifactDefinition): artifact definition.

    Returns:
      bool: True if artifact definition was found on storage media image.
    """
    find_specs = list(self._filter_generator.GetFindSpecs(
        [artifact_definition.name]))
    if not find_specs:
      return False

    for path_spec in self._file_system_searcher.Find(find_specs=find_specs):
      # TODO: do something with path_spec.
      _ = path_spec
      return True

    return False

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
        self._windows_registry = winregistry

    self._filter_generator = (
        artifact_filters.ArtifactDefinitionFiltersGenerator(
            self._artifacts_registry, self._environment_variables, []))

    self._file_system_searcher = dfvfs_file_system_searcher.FileSystemSearcher(
        self._file_system, self._mount_point)

    return True
