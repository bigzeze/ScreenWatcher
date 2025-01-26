# MacOS

```shell
pyinstaller src/ScreenWatcher.py -w --icon=Resources/icons/icon.icns --add-data Resources/icons:icons --add-data config.ini:. -y
```

# Windows

```shell
pyinstaller src/ScreenWatcher.py -w --icon=Resources/icons/icon.icns -y
```

Then copy *'Resources'* directory to the built 'dist/*ScreenWatcher/' directory.*
