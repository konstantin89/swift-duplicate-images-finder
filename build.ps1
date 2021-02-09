pyinstaller src/main.py `
     --onefile `
     --hidden-import dearpygui `
     --icon=resources/icon.ico `
     --noconsole `
     --add-data 'resources/logo.png;resources'


