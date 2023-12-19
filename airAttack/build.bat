@echo off
set zipFile=chromedriver-win64.zip
set outputPath=%USERPROFILE%\Downloads\chromedriver-win64.zip

for /f "tokens=2*" %%A in ('REG QUERY HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon /v version ^| find "version"') do set CHROME_VERSION=%%B

set CHROME_MINIMUM_VERSION=118

if "!CHROME_VERSION!" LSS "!CHROME_MINIMUM_VERSION!" (
    echo [ERROR] Chrome version is less than 118. Please update Chrome.
    echo ========================
    echo Google Chrome Update Prompt
    echo ========================
    echo.
    echo Please follow these steps to manually update Google Chrome:
    echo.
    echo 1. Open Google Chrome browser.
    echo.
    echo 2. Click on the menu icon in the top right corner "three vertical dots".
    echo.
    echo 3. Hover your mouse over the "Help" menu item.
    echo.
    echo 4. In the submenu that appears, click on "About Google Chrome."
    echo.
    echo 5. Chrome will automatically check for updates and display the update progress.
    echo.
    echo 6. If updates are available, Chrome will prompt you to restart the browser to complete the update.
    echo.
    echo 7. Restart Chrome, and your browser will be up to date.
    echo.
    pause
    exit
)

for /f "tokens=2 delims==" %%A in ('wmic os get osarchitecture /value ^| find "="') do set OSARCH=%%A

if "%OSARCH%"=="64-bit" (
     set url=https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/win64/chromedriver-win64.zip
) else (
     set url=https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/win32/chromedriver-win32.zip
)

echo.
echo [INFO] Downloading chromedriver.zip...
curl -o %outputPath% %url%
if %errorlevel% neq 0 (
    echo [ERROR] Failed to Download!
    pause
    exit
)
if exist %outputPath% (
    echo [INFO] Complete download!
    echo.
    echo [INFO] Unpacking chromedriver.zip to "%~dp0"^...
    tar -xf %outputPath% -C %~dp0
    del %outputPath%
) else (
    echo [WARNING] No such file!Plese goto "%url%" Download zip!
    pause
    exit
)
if %errorlevel% neq 0 (
    echo [ERROR] Failed to unpack!Plese unpack "%outputPath%" file to "%~dp0"!
    pause
    exit
)
echo [INFO] Complete unpack!
echo.
echo [INFO] Installing pip module...
pip install selenium requests
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install!
    pause
    exit
)
echo [INFO]  Complete install!
echo.
echo ======================================
echo This is an automatic booking system!
echo Run "python3 main.py" to start the program!
echo Here have some function you can use!
echo ======================================
echo.
echo "-h" or "--help": Display help information
REM echo "-t" or "--time": Specify the pause time in seconds
echo "-o" or "--org": Specify the origin, default is TPE
echo "-d" or "--des": Specify the destination, default is KIX
REM echo "-c" or "--cost": Set the cost limit
REM echo "-a" or "--amount": Specify the tickets quantity
REM echo "-b" or "-back": For round-trip tickets
REM echo "-s" or "--speed": Speed up
echo.
