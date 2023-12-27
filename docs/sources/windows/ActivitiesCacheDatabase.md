## Activities Cache Database

Windows activity history keeps track of activity on a device, such as
application and services usage, files opened, and websites browsed.

Windows uses the activity history data to provide you with personalized
experiences (such as ordering your activities based on duration of use)
and relevant suggestions (such as anticipating what your needs might be
based on your activity history).

### Significance

The Windows activity history can be used to determine system and user activity.

### On-disk path

On-disk the Windows activity history is stored in a Activities Cache database.
This SQLite database can be found in the following path:

```
C:\Users\%USERNAME%\AppData\Local\ConnectedDevicesPlatform\L.%USERNAME%\ActivitiesCache.db
```

### Versions

Windows activity history databases were first observed on Windows 10 1803.

### References

* [Windows 10 activity history and your privacy](https://support.microsoft.com/en-us/windows/-windows-activity-history-and-your-privacy-2b279964-44ec-8c2f-e0c2-6779b07d2cbd)
* [Windows 10 Timeline – Initial Review of Forensic Artefacts](https://salt4n6.com/2018/05/03/windows-10-timeline-forensic-artefacts/)
* [An examination of Win10 ActivitiesCache.db database](https://kacos2000.github.io/WindowsTimeline/WindowsTimeline.pdf)
