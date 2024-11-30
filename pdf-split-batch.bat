set /p input=please enter the pdf path to parse batch: 
set "input=%input:"=%"

for %%f in ("%input%\*.pdf") do (
@echo spliting %%f
pipenv run python pdf-split.py --input  "%%f"
)

@echo ok

@pause