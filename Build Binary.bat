:: pip install pyinstaller
:: pip install requests

:: build the binary
pyinstaller --onefile GME.py --name "GME" --clean --noconfirm

:: TODO: noconsole stops GME from working even after removing all print()
:: pyinstaller --onefile GME.py --name "GME" --clean --noconfirm --noconsole

:: copy the blender script to dist/
copy "Square Grid.blend" "dist/Square Grid.blend" /y

