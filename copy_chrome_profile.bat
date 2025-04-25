@echo off
set "source=C:\Users\justi\AppData\Local\Google\Chrome\User Data"
set "destination=C:\Users\justi\chrome_user_data_copy"

rem Terminate any running Chrome processes
echo Terminating all Chrome processes...
taskkill /F /IM chrome.exe
rem Check if the destination directory exists

if not exist "%destination%" (
    echo Destination folder does not exist. Creating new folder and copying data...
    robocopy "%source%" "%destination%" /MIR /Z
) else (
    echo Destination folder already exists.
)

echo Chrome profile has been copied successfully.

exit /b
