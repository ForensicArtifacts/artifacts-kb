## Jump Lists

Jump Lists are a Windows Taskbar feature that gives the user quick access to recently accessed application files and actions.

Jump Lists were introduced in Windows 7

There are multiple variants of Jump Lists:

* AutomaticDestinations (*.automaticDestinations-ms) files
* CustomDestinations (*.customDestinations-ms) files
* Explorer StartPage2 ProgramsCache Registry values

### AutomaticDestinations

The AutomaticDestinations Jump List files are located in the user profile path:

```
C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations\*.automaticDestinations-ms
```

### CustomDestinations

The CustomDestinations Jump List files are located in the user profile path:

```
C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Recent\CustomDestinations\*.customDestinations-ms
```

### Explorer StartPage2 ProgramsCache

The Explorer StartPage2 ProgramsCache Jump Lists are stored in the Windows Registry:

```
Key: HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\StartPage2
Value(s): ProgramsCacheSMP, ProgramsCacheTBP
```

### References

* [ForensicsWiki: Jump Lists](https://forensicswiki.xyz/wiki/index.php?title=Jump_Lists)
* [dtFormats: Jump lists format](https://github.com/libyal/dtformats/blob/main/documentation/Jump%20lists%20format.asciidoc)
* [WinReg-KB: Programs Cache values](https://github.com/libyal/winreg-kb/blob/main/documentation/Programs%20Cache%20values.asciidoc)
