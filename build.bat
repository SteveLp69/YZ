@echo off

"C:/Program Files/Python313/python.exe" "d:/Large Python/yz/script/funktions/onfile.py" "main.py" "programm.py"

pyinstaller --onefile --argv-emulation --distpath "D:\Large Python\yz\builds" "programm.py" -n "yz" -i "NONE"

"C:/Program Files/Python313/python.exe" "d:/Large Python/yz/script/funktions/clean.py"