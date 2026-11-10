@echo off
setlocal
title Tokyo Mew Mew English Patch
cd /d "%~dp0"

echo ============================================
echo   Tokyo Mew Mew PS1 - English patch injector
echo ============================================
echo.

rem ---- find Python ----
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY where python >nul 2>nul && set "PY=python"
if not defined PY goto nopython

rem ---- find the disc image: dragged onto this file, or *Track 1*.bin here ----
set "BIN=%~1"
if defined BIN goto havebin
for %%F in ("*Track 1*.bin") do set "BIN=%%~fF"
if not defined BIN for %%F in ("*Track 01*.bin") do set "BIN=%%~fF"
if not defined BIN goto nobin
:havebin
if not exist "%BIN%" goto nobin
echo Disc image: "%BIN%"
echo.

if not exist "inject.py" goto noinject

rem ---- one-time backup of the untouched image ----
if exist "%BIN%.original" goto backupdone
echo Making a one-time backup: "%BIN%.original"
echo This copies the whole image, so it may take a minute...
copy /b "%BIN%" "%BIN%.original" >nul
if errorlevel 1 goto backupfail
:backupdone
echo Backup: "%BIN%.original"
echo.

rem ---- inject whichever patched files are present ----
set "DID="
if not exist "D_SCE.BIN" goto skipsce
echo Injecting D_SCE.BIN ...
%PY% inject.py "%BIN%" "D_SCE.BIN"
if errorlevel 1 goto fail
set "DID=1"
:skipsce
if not exist "SLPM_871.78" goto skipexe
echo Injecting SLPM_871.78 ...
%PY% inject.py "%BIN%" "SLPM_871.78"
if errorlevel 1 goto fail
set "DID=1"
:skipexe
call :inj D_SYSTEM.BIN
if errorlevel 1 goto fail
call :inj D_SCREEN.BIN
if errorlevel 1 goto fail
call :inj D_FIELD.BIN
if errorlevel 1 goto fail
call :inj D_EFFECT.BIN
if errorlevel 1 goto fail
call :inj D_UNIT.BIN
if errorlevel 1 goto fail
call :inj D_FACE.BIN
if errorlevel 1 goto fail
if not defined DID goto nofiles

echo.
echo All done! Load the .cue in your emulator to play.
goto end

:inj
if not exist "%~1" exit /b 0
echo Injecting %~1 ...
%PY% inject.py "%BIN%" "%~1"
if errorlevel 1 exit /b 1
set "DID=1"
exit /b 0

:nopython
echo Python was not found. Install it from https://www.python.org/downloads/
echo and tick "Add python.exe to PATH" during setup, then run this again.
goto end
:nobin
echo Couldn't find the Track 1 .bin file.
echo Put this .bat in the same folder as the game's "(Track 1).bin",
echo or drag the Track 1 .bin file onto this .bat.
goto end
:noinject
echo inject.py is missing. Keep it in the same folder as this .bat.
goto end
:nofiles
echo No patch files found. Put the patched files (D_SCE.BIN, SLPM_871.78, D_SYSTEM.BIN...) next to this .bat.
goto end
:backupfail
echo Couldn't make the backup (disk full?). Nothing was changed.
goto end
:fail
echo.
echo Something went wrong - see the message above.
echo Your untouched copy is "%BIN%.original". To start over, delete the
echo patched .bin and rename the .original file back to .bin.
:end
echo.
pause
