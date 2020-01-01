@echo off
set /p ver="Enter version: v"
"C:\Program Files\7-Zip\7z.exe" a ..\..\..\Distrib\GHAutoBackup-v%ver%.zip @PackageFiles.txt
pause