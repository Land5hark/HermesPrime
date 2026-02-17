@echo off
chcp 65001 >nul
cls

echo 🧠 Second Brain Tunnel Connector
echo ================================
echo.

set SERVER_IP=187.77.11.213
set SERVER_USER=clawd
set LOCAL_PORT=8080
set REMOTE_PORT=8080
set PID_FILE=%TEMP%\second-brain-tunnel.pid

:: Check if tunnel already running
tasklist /FI "IMAGENAME eq ssh.exe" 2>nul | find /I "ssh.exe" >nul
if %ERRORLEVEL% EQU 0 (
    echo ⚠ SSH process detected. Checking if it's our tunnel...
    
    :: Try to find existing tunnel
    for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq ssh.exe" /NH 2^>nul') do (
        set SSH_PID=%%a
        goto :CHECK_TUNNEL
    )
)

goto :START_TUNNEL

:CHECK_TUNNEL
if exist "%PID_FILE%" (
    set /p SAVED_PID=<"%PID_FILE%"
    if "%SAVED_PID%"=="%SSH_PID%" (
        echo.
        echo ✓ Tunnel already running (PID: %SSH_PID%)
        echo   Access at: http://localhost:%LOCAL_PORT%
        echo.
        choice /C YN /M "Kill existing tunnel and restart"
        if %ERRORLEVEL% EQU 1 (
            taskkill /PID %SSH_PID% /F >nul 2>&1
            del "%PID_FILE%" 2>nul
            echo ✓ Killed existing tunnel
            timeout /t 1 >nul
        ) else (
            echo Keeping existing tunnel.
            goto :OPEN_BROWSER
        )
    )
)

:START_TUNNEL
echo.
echo Testing SSH connection to %SERVER_USER%@%SERVER_IP%...
ssh -o ConnectTimeout=5 -o BatchMode=yes %SERVER_USER%@%SERVER_IP% exit 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ✗ SSH connection failed
    echo.
    echo Possible issues:
    echo   • SSH key not set up (run: ssh-keygen, then ssh-copy-id %SERVER_USER%@%SERVER_IP%)
    echo   • OpenSSH client not installed
    echo   • Server not reachable
    pause
    exit /b 1
)

echo ✓ SSH connection successful
echo.
echo Creating SSH tunnel...
echo   Local:  http://localhost:%LOCAL_PORT%
echo   Remote: %SERVER_IP%:%REMOTE_PORT%
echo.

:: Start SSH tunnel in background
start /B ssh -N -L %LOCAL_PORT%:localhost:%REMOTE_PORT% %SERVER_USER%@%SERVER_IP% -o ServerAliveInterval=60 -o ServerAliveCountMax=3

:: Wait a moment for connection
timeout /t 2 >nul

:: Find the PID
tasklist /FI "IMAGENAME eq ssh.exe" /NH 2>nul | findstr "ssh.exe" > %TEMP%\ssh_pids.txt
for /f "tokens=2" %%a in (%TEMP%\ssh_pids.txt) do (
    echo %%a > "%PID_FILE%"
    set SSH_PID=%%a
)
del %TEMP%\ssh_pids.txt 2>nul

echo ✓ Tunnel created successfully!
echo.
echo 🌐 Opening: http://localhost:%LOCAL_PORT%
echo.
start http://localhost:%LOCAL_PORT%

echo.
echo To disconnect: taskkill /F /IM ssh.exe
echo.
pause

:OPEN_BROWSER
start http://localhost:%LOCAL_PORT%
