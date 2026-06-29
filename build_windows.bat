
pyinstaller -n "PacMan-42" --windowed -p src/ --add-data="src/inc:inc"  src/main.py

copy src\config_web.json dist\PacMan-42\
