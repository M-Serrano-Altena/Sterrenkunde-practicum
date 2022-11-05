@echo off
:loop

:: "Path where your Python exe is stored\python.exe" "Path where your Python script is stored\sterrenkunde_practicum.py"
"C:\Users\Marc_\anaconda3\python.exe" "C:\Users\Marc_\Documents\GitHub\Sterrenkunde-practicum\sterrenkunde_practicum.py"

set /a loop=%loop%+1
echo ...
set /p input= Type 'stop' om het programma te stoppen, klik enter om door te gaan:  
if "%input%"=="stop" goto next
goto loop

:next
