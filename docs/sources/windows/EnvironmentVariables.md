## Environment variables

Name | Scope | Description
--- | --- | ---
`%AllUsersProfile%` | System | Path of the of the "All Users" or "Common" profile directory
`%APPX_PROCESS%` | User | .NET applications will attempt to load WinAppXRT.dll from %PATH%
`%COMMONPROGRAMFILES%` | System | Path of the common program files folder
`%COMMONPROGRAMFILES(X86)%` | System | Path of the 32-bit common program files folder on a 64-bit Windows installation
`%ComSpec%` | System | Path of the command processor, typically "cmd.exe"
`%DriverData%` | System | Path of the directory used for temporary state files of user-mode drivers
`%PATH%` | System and User | Ordered list of paths of directories that will be searched on execution request without a specific path
`%ProfilesDirectory%` | System | Path of a directory that contains the users' profile directories, typically "%SystemDrive%\Users"
`%ProgramData%` | System | Path of the "Program Data" directory
`%ProgramFiles%` | System | Path of the "Program Files" directory
`%ProgramFiles(x86)%` | System | Path of the 32-bit "Program Files" directory on a 64-bit Windows installation
`%SystemDrive%` | System | Letter of the drive in which the system directory is located, typically "C:"
`%SystemRoot%` | System | Path of the system directory, typically "C:\Windows"
`%TEMP%` | User |
`%WinDir%` | System | Path of the Windows directory, typically "C:\Windows"

### References

* [Wikipedia: Environment variable - Windows](https://en.wikipedia.org/wiki/Environment_variable#Windows)
* [Recognized Environment Variables](https://learn.microsoft.com/en-us/windows/deployment/usmt/usmt-recognized-environment-variables)
* [Driver Package Isolation - DriverData and ProgramData](https://learn.microsoft.com/en-us/windows-hardware/drivers/develop/driver-isolation#driverdata-and-programdata)
* [About User Profiles](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/legacy/bb776892(v=vs.85))

#### APPX_PROCESS environment variable

* [Beyond good ol’ Run key, Part 17](http://www.hexacorn.com/blog/2014/08/31/beyond-good-ol-run-key-part-17/)
* [.NET Framework 4.6 allows side loading of Windows API Set DLL](https://www.securify.nl/advisory/net-framework-46-allows-side-loading-of-windows-api-set-dll)

#### Windows Registry environment variable expansion

* [Expanding Environment Variables](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-even/7d43656f-4f9f-4994-a919-50db71e01af9)
