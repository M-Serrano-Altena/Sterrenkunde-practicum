@echo off
:loop

"C:\Users\Marc_\anaconda3\python.exe" "C:\Users\Marc_\Documents\GitHub\Sterrenkunde-practicum\sterrenkunde_practicum.py"

set /a loop=%loop%+1
echo ...
set /p input= Type 'stop' om het programma te stoppen, klik enter om door te gaan:  
if not x%input:stop=%==x%input% goto next
goto loop

:next
