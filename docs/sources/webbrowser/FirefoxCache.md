## Mozilla Firefox disk cache

Mozilla Firefox uses disk cache to store resources fetched from the web so that
they can be accessed quickly at a latter time if needed.

There are 2 known disk cache formats:

* Mozilla Firefox disk cache format version 1

* Mozilla Firefox disk cache format version 2

### Firefox 1 to 31

Mozilla Firefox 1 to 31 use the Mozilla Firefox disk cache format version 1.

On Linux Mozilla Firefox 1 to 20

```
/home/$USER/.mozilla/firefox/$PROFILE.default/Cache/
```

On Linux Mozilla Firefox 21 to 31

```
/home/$USER/.cache/mozilla/firefox/$PROFILE.default/Cache/
```

On Mac OS

```
/Users/$USER/Library/Caches/Firefox/Profiles/$PROFILE.default/Cache/
```

On Windows XP

```
C:\Documents and Settings\%USERNAME%\Local Settings\Application Data\Mozilla\Firefox\Profiles\%PROFILE%.default\Cache\
```

On Windows Vista, 7

```
C:\Users\%USERNAME%\AppData\Local\Mozilla\Firefox\Profiles\%PROFILE%.default\Cache\
```

### Firefox 32 and later

Mozilla Firefox 32 and later use the Mozilla Firefox disk cache format version
2.

On Linux

```
/home/$USER/.mozilla/firefox/$PROFILE.default/cache2/
```

On Mac OS

```
/Users/$USER/Library/Caches/Firefox/Profiles/$PROFILE.default/cache2/
```

On Windows XP

```
C:\Documents and Settings\%USERNAME%\Local Settings\Application Data\Mozilla\Firefox\Profiles\%PROFILE%.default\cache2\
```

On Windows Vista, 7

```
C:\Users\%USERNAME%\AppData\Local\Mozilla\Firefox\Profiles\%PROFILE%.default\cache2\
```

### References

* [Forensicswiki: Mozilla Firefox](https://forensics.wiki/mozilla_firefox)
* [Example Mozilla Firefox Cache files](https://github.com/dfirlabs/firefox-specimens/tree/main/specimens), by firefox-specimens project
