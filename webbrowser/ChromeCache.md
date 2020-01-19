## Google Chrome/Chromium disk cache

Google Chrome/Chromium uses disk cache to store resources fetched from the web
so that they can be accessed quickly at a latter time if needed.

### Cache version 2

On Linux Google Chrome/Chromium 8
```
/home/$USER/.cache/chromium/Cache/
/home/$USER/.cache/google-chrome/Cache/
```

On Linux Google Chrome/Chromium 9 to 51
```
/home/$USER/.cache/chromium/$PROFILE/Cache/
/home/$USER/.cache/google-chrome/$PROFILE/Cache/
```

On MacOS
```
/Users/$USER/Library/Caches/Google/Chrome/$PROFILE/Cache/
```

Where the $PROFILE contains the name of the profile. The default profile is
named "Default".

On Windows XP
```
C:\Documents and Settings\%USERNAME%\Local Settings\Application Data\Google\Chrome\User Data\%PROFILE%\Cache\
```

On Windows Vista, 7
```
C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\%PROFILE%\Cache\
```

Where the %PROFILE% contains the name of the profile. The default profile is
named "Default".

### Media Cache

```
/home/$USER/.cache/chromium/$PROFILE/Media Cache/
/home/$USER/.cache/google-chrome/$PROFILE/Media Cache/
```

### Application Cache

```
/home/$USER/.config/chromium/$PROFILE/Application Cache/Cache/
/home/$USER/.config/google-chrome/$PROFILE/Application Cache/Cache/
```

### GPUCache

On Linux Google Chrome/Chromium 68
```
/home/$USER/.config/google-chrome/$PROFILE/GPUCache/
/home/$USER/.config/google-chrome/$PROFILE/Storage/ext/$EXTENSION/def/GPUCache/
/home/$USER/.config/google-chrome/ShaderCache/GPUCache/
```

Where the $EXTENSION contains the identifier of the extension such as
"nmmhkkegccagdldgiimedpiccmgmieda".

### References

* [Forensicswiki: Google Chrome](https://forensicswiki.xyz/wiki/index.php?title=Google_Chrome)
* [Example Google Chrome Cache files](https://github.com/dfirlabs/chrome-specimens/tree/master/specimens), by chrome-specimens project

### Test versions

Software | Version | Platform
-- | -- | --
Google Chrome | 8.0.552.237 | Linux 32-bit
Google Chrome | 9.0.597.107 | Linux 32-bit
Google Chrome | 10.0.648.205 | Linux 32-bit
Google Chrome | 11.0.696.60 | Linux 32-bit
Google Chrome | 12.0.742.124 | Linux 32-bit
Google Chrome | 13.0.782.220 | Linux 32-bit
Google Chrome | 14.0.835.186 | Linux 32-bit
Google Chrome | 15.0.874.121 | Linux 32-bit
Google Chrome | 16.0.912.77 | Linux 32-bit
Google Chrome | 17.0.963.83 | Linux 32-bit
Google Chrome | 18.0.1025.168 | Linux 32-bit
Google Chrome | 19.0.1084.52 | Linux 32-bit
Google Chrome | 20.0.1132.57 | Linux 32-bit
Google Chrome | 31.0.1650.48 | Linux 32-bit
Google Chrome | 40.0.2214.115 | Linux 64-bit
Google Chrome | 50.0.2661.75 | Linux 64-bit
Google Chrome | 51.0.2704.84 | Linux 64-bit
Google Chrome | 68.0.3440.84 | Linux 64-bit

