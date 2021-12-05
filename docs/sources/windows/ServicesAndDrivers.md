## Services and drivers

### Significance

Malware can add new services or drivers to gain persistence, or modify existing
ones to avoid detection.

For example the ZeroAccess rootkit will make the following changes to the
Windows Security Service Center (WSCSVC), Windows Defender (WINDEFEND), and
Windows Firewall (MPSSVC) services, among others.

* Set the 'Start' value to 4, indicating that the service should be disabled
* Set the 'DeleteFlag' value to 1, indicating that the service should be removed
* Set the 'ErrorControl' value to 0 and 'Type' value to 32, causing it to fail to be started by the Service Controller without generating error messages

### Settings

The services and drivers settings can be found in the Windows Registry key:

```
HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services
```

### References

* [Services and drivers](https://winreg-kb.readthedocs.io/en/latest/sources/system-keys/Services-and-drivers.html)
