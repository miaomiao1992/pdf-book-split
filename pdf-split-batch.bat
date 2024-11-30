@echo off

set /p input=please enter the pdf path to parse batch: 
set "input=%input:"=%"

if not exist "%input%" (
@echo not exist %input% !
@pause
exit /b
)

for %%f in ("%input%\*.pdf") do (
@echo spliting %%f
pipenv run python pdf-split.py --input  "%%f"
)

@echo ok

@pause