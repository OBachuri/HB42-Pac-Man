
pyinstaller -n "PacMan-42" --windowed  --onefile -p src/ --add-data="src/inc:inc"  src/main.py

copy src\config_web.json dist\
copy src\ReadMe.txt dist\