# Changelog

Every new change will be logged

## v1.0.7
```
+ Updated Generator.html, Request-Buttons overwrote Desktop-Buttons (for example the Desktop Proxy Button didnt work)
+ Added a General-Class, for functions that are used multiple times (reduces lines of code)
+ Added new Desktop-Spotify self-killing function (to avoid closing threads if the main call has an error)
+ Fixxed the Request-Passwords, before sometimes the Password was to short
+ Fixxed the .exe Loggings (was coded for Selling as .exe, now is .py)
+ Fixxed Username-Password splitting everywhere (Now you can also leave the :name at the end)
+ Some unnecessary lines were removed and some indentations cleaned up
```

## v1.0.6
```
+ Fixxed Like Probability (Liked every time before)
+ Added Exception-Catcher on Browser-Crasher (threw an error sometimes before that you can just ignore)
+ Recoded DesktopStreamer´s combo Algorithm (used the same account over and over again before)
-> Note: Maight have to recode same Algorithm on other features!
```

## v1.0.5
```
+ Edited Sandbox Deletion (No AdminPerms required anymore and beforehand it didnt delete them sometimes)
+ Fixxed DesktopStreamer Mute Feature
+ Fixxed DesktopStreamer Preferences-Setting
+ Fixxed WebStreamer Threads
+ Some (a bit unnecessary) Sandbox renaming to avoid Sandbox-issues
```

## v1.0.4
```
+ Recoded the WebStreamer Calling Algorithm (Called one combo over and over again before)
+ Changed Usage of executable_path to service object when calling selenium
+ Added Login Button Click in the DesktopStreamer (Failed to Login before if u werent logged in yet)
```

## v1.0.3
```
+ Deleted unnecessary requirements (Packages are already inbuilt since python 3.x)
+ Added Git and Pip to Program Requirements (for mjolnir installation)
+ Changed Variable-name from "password" to "pw" in the Liker
+ Doc-stringed "proxy-select" interactions (broke web-stream-button)  
```

## v1.0.2
```
+ Deleted unnecessary prints
+ Deleted "print_first_line=False, log_level=0" when calling ChromeDriverManager, not supported on new versions
+ Added "logging.getLogger('WDM').setLevel(logging.NOTSET)" to replace functionality of above update
+ Changed path adding of "[INFO] Coded by Vinyzu (https://github.com/Vinyzu/MjolnirAiO)" (Before it was shown letter by letter in the logs)
+ Removing "If you paid for this you got scammed" when Logs show up (they overlapped)
+ Changed twocaptcha requirement to 2captcha-python (wrong package was put on initial commit)
```

## v1.0.1
```
+ Changed Download to Sandboxie (Old Dowload suggested Sandboxie-Plus, which was not supported)
+ Changed websocket requirement to websocket-client (wrong package was put on initial commit)
+ Added " replacement in Desktop-Generator´s output_path
+ Song-Count Request is now converted to an int() to  compare with start-position, which is an int
```

## v1.0
```
+ First Commit
```
