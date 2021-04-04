## Windows Event Log

The Windows Event Log is used by Microsoft Windows to store application and
system logs. Typical Event Logs are: Application, System, and Security

Entries in Event Log files contain very little human-readable data. EventViewer,
which is the Windows native Event Log viewing application, makes Event Log
entries human-readable by combining pre-defined message string templates, which
are stored in DLLs and EXEs, with variable data stored in the Event Log entry.

The combination of event identifier, its qualifiers and provider is needed to
determine the message string template for a specific Event Log entry.
Information about Windows Event Log providers can be found in the Windows
Registry.

A common misconception is that event identifiers are globally unique, however
they are only unique in the context of a specific version of a specific
Log provider.

### Windows NT4

On Windows NT4 the Event Logs files can be found in:

```
C:\WINNT\System32\config
```

Windows NT4 uses the Windows Event Log (EVT) format.

### Windows 2000, XP and 2003

On Windows 2000, XP and 2003 the Event Logs files can be found in:

```
C:\Windows\System32\config
```

Windows 2000, XP and 2003 uses the Windows Event Log (EVT) format.

### Windows Vista and later

On Windows Vista and later the Event Logs files can be found in:

```
C:\Windows\System32\winevt\Logs\
```

Windows Vista and later uses the Windows XML Event Log (EVTX) format.

### References

* [Wikipedia: Event Viewer](https://en.wikipedia.org/wiki/Event_Viewer)
* [Wikipedia: Log file](https://en.wikipedia.org/wiki/Log_file)
* [ForensicsWiki: Windows Event Log (EVT)](https://forensicswiki.xyz/wiki/index.php?title=Windows_Event_Log_(EVT))
* [ForensicsWiki: Windows XML Event Log (EVTX)](https://forensicswiki.xyz/wiki/index.php?title=Windows_XML_Event_Log_(EVTX))
* [Windows Event Viewer Log (EVT) format](https://github.com/libyal/libevt/blob/main/documentation/Windows%20Event%20Log%20(EVT)%20format.asciidoc)
* [Windows XML Event Log (EVTX) format](https://github.com/libyal/libevtx/blob/main/documentation/Windows%20XML%20Event%20Log%20(EVTX).asciidoc)
* [EventLog keys](https://winreg-kb.readthedocs.io/en/latest/sources/EventLog-keys.html)
* [Sysinternals Sysmon unleashed](https://docs.microsoft.com/en-us/archive/blogs/motiba/sysinternals-sysmon-unleashed)
* [Export corrupts Windows Event Log files](https://blog.fox-it.com/2019/06/04/export-corrupts-windows-event-log-files/)

