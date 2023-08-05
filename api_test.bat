
@echo off
setlocal

REM Set the absolute path to the test file
set TEST_FILE="C:\Users\Llew\Documents\Llewellyn_Storage\Aura_QA_Case_Study\py_test\api_test.py"

REM Set the absolute path to the log file
set LOG_FILE="C:\Users\Llew\Documents\Llewellyn_Storage\Aura_QA_Case_Study\logs\pytest_logs.txt"

REM Get the current date and time in the format YYYY-MM-DD HH:MM:SS
for /f "tokens=1-3 delims=/ " %%a in ('echo %date%') do set "timestamp=%%c-%%a-%%b %time%"


REM Run pytest 
"C:\Users\Llew\Documents\Llewellyn_Storage\Aura_QA_Case_Study\venv\Scripts\python.exe" -m pytest %TEST_FILE% 
(
 echo %timestamp%
 "C:\Users\Llew\Documents\Llewellyn_Storage\Aura_QA_Case_Study\venv\Scripts\python.exe" -m pytest %TEST_FILE% 
)>> %LOG_FILE%
pause 
