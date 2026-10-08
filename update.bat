@echo off
rem Obnovi index packu a pushne zmeny na GitHub.
rem Pouzitie: update.bat "Pridany mod XY"
setlocal
chcp 65001 >nul
cd /d "%~dp0"

if "%~1"=="" (
  echo Pouzitie: update.bat "sprava commitu"
  exit /b 1
)

set "PACKWIZ=packwiz"
where packwiz >nul 2>nul || set "PACKWIZ=%USERPROFILE%\Documents\packwiz-tools\packwiz.exe"

"%PACKWIZ%" refresh || goto :error
git add -A || goto :error
git diff --cached --quiet && (
  echo Ziadne zmeny na commitnutie.
  exit /b 0
)
git commit -m "%~1" || goto :error
git push || goto :error

echo.
echo Hotovo. Kamosi dostanu update pri dalsom spusteni hry (GitHub Pages sa obnovi do 1-2 minut).
exit /b 0

:error
echo.
echo CHYBA: nieco zlyhalo, pozri vypis vyssie.
exit /b 1
