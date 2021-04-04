## Windows Registry files

The Windows Registry is a hierarchical database that stores various settings
for the Windows operating system and applications.

### Windows 3.1

Windows 3.1 uses the SHCC Windows Registry file format

### Windows 9x/Me

On Windows 95, 98 and Me the Windows Registry files can be found in:

```
%SystemRoot%\
```

Windows 95, 98 and Me uses the CREG Windows Registry file format

### Windows NT4 and later

On Windows NT4 and later the Windows Registry files can be found in:

```
%SystemRoot%\System32\Config\
%UserProfile%\
%UserProfile%\Local Settings\Application Data\Microsoft\Windows\
%UserProfile%\AppData\Local\Microsoft\Windows\
```

Windows NT4 and later uses the REGF Windows Registry file format

### References

* [Wikipedia: Windows Registry](https://en.wikipedia.org/wiki/Windows_Registry)
* [Forensicswiki: Windows Registry](https://forensicswiki.xyz/wiki/index.php?title=Windows_Registry)
* [WinReg-KB: Registry - Files](https://winreg-kb.readthedocs.io/en/latest/sources/windows-registry/Files.html)
* [The Windows NT Registry File Format](http://www.sentinelchicken.com/data/TheWindowsNTRegistryFileFormat.pdf)
* [Windows 9x Registry File (CREG) format specification](https://github.com/libyal/libcreg/blob/main/documentation/Windows%209x%20Registry%20File%20(CREG)%20format.asciidoc)
* [Windows NT Registry File (REGF) format specification](https://github.com/libyal/libregf/blob/main/documentation/Windows%20NT%20Registry%20File%20(REGF)%20format.asciidoc)
* [Windows registry file format specification](https://github.com/msuhanov/regf/blob/master/Windows%20registry%20file%20format%20specification.md)
