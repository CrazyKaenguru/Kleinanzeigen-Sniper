@echo off
setlocal

REM Specify your Git installation path
set "gitPath=C:\Program Files\Git"

REM Add Git to the PATH
setx PATH "%PATH%;%gitPath%\bin;%gitPath%\cmd" /M

echo Git has been added to the PATH.
echo Please restart your command prompt to use Git.