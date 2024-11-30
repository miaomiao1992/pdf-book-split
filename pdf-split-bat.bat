set /p input=please enter the pdf path to split: 

pipenv run python pdf-split.py --input  %input%

@pause