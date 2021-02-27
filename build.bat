pyinstaller src/main.py ^
     --name dup-image-finder ^
     --onefile ^
     --hidden-import dearpygui ^
     --icon=resources/icon.ico ^
     --noconsole ^
     --add-data 'resources/logo.png;resources'


