:: install libraries for building binaries
pip install pyinstaller
pip install requests
:: install required libraries for GME
pip install numpy
pip install h5py
pip install psutil
pip install matplotlib

:: build the binary
pyinstaller --onefile GME.py --name "GME" --clean --noconfirm

:: TODO: noconsole stops GME from working even after removing all print()
:: pyinstaller --onefile GME.py --name "GME" --clean --noconfirm --noconsole

:: copy the blender script to dist/
copy "Square Grid.blend" "dist/Square Grid.blend" /y

