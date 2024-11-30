@echo off
git pull
echo "git pull success"
set /p input=please enter the comments: 

set "Time=%time:~0,8%"
set "t=%Time: =0%"

set "remarks=%date:~,4%-%date:~5,2%-%date:~8,2%-%t%-push-miaomiao1992-%input%"
echo %remarks%

git add .

git commit -m  %remarks%
git push origin master

echo --End--
@pause