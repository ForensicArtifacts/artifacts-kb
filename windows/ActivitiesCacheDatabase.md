## Activities Cache Database

Windows activity history keeps track of activity on a device, such as apps and
services usage, files opened, and websites browsed. This activity history is
stored locally on the device in a SQLite database file:

```
C:\Users\%USERNAME%\AppData\Local\ConnectedDevicesPlatform\L.%USERNAME%\ActivitiesCache.db
```

### Versions

The activity cache databases were first observed on Windows 10 1803.

### References

* [Windows 10 activity history and your privacy](https://support.microsoft.com/en-us/help/4468227/windows-10-activity-history-and-your-privacy-microsoft-privacy)
* [CCL Group: Windows 10 Timeline Forensic Artefacts](https://cclgroupltd.com/2018/05/03/windows-10-timeline-forensic-artefacts/)
* [Salt Forensics: Windows 10 Timeline – Initial Review of Forensic Artefacts](https://salt4n6.com/2018/05/03/windows-10-timeline-forensic-artefacts/amp/)
* [An examination of Win10 ActivitiesCache.db database](https://kacos2000.github.io/WindowsTimeline/WindowsTimeline.pdf)
