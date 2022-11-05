@echo off
:loop

"Path where your Python exe is stored\python.exe" "Path where your Python script is stored\sterrenkunde_practicum.py"

set /a loop=%loop%+1
echo ...
set /p input= Type 'stop' om het programma te stoppen, klik enter om door te gaan:  
if not x%input:stop=%==x%input% goto next
goto loop

:next
