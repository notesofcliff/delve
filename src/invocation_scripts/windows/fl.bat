@echo off
setlocal

SET FLASHLIGHT_HOME=%~dp0

cd /d %FLASHLIGHT_HOME%
call set-env.bat

%FLASHLIGHT_HOME%\python\%PYTHON_VERSION%\python manage.py %*
endlocal
