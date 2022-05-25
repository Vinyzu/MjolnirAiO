# Changelog

Every new change will be logged

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
