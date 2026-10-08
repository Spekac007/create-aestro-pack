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

call :refresh || goto :error
git add -A || goto :error
git diff --cached --quiet
if errorlevel 1 (
  git commit -m "%~1" || goto :error
) else (
  echo Ziadne nove zmeny na commitnutie.
)

git push && goto :done

rem Push nepresiel: niekto iny medzitym pushol. index.toml a pack.toml sa vtedy
rem vzdy pohadzu, tak zmeny spojime (pri konflikte vyhra ta nasa) a index prepocitame.
echo.
echo Push nepresiel - niekto medzitym poslal svoje zmeny. Spajam ich s tvojimi...
git pull --rebase -X theirs || goto :conflict
call :refresh || goto :error
git add -A || goto :error
git diff --cached --quiet
if errorlevel 1 (
  git commit -m "Obnoveny index po spojeni zmien" || goto :error
)
git push || goto :error

:done
echo.
echo Hotovo. Kamosi dostanu update pri dalsom spusteni hry (GitHub Pages sa obnovi do 1-2 minut).
exit /b 0

:refresh
rem Configy oznaci ako preserve, aby sa hracom neprepisali ich vlastne nastavenia
"%PACKWIZ%" refresh || exit /b 1
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0preserve-configs.ps1" || exit /b 1
"%PACKWIZ%" refresh || exit /b 1
exit /b 0

:conflict
echo.
echo CHYBA: zmeny sa nepodarilo spojit automaticky.
echo Spusti "git rebase --abort" a napis spravcovi packu.
exit /b 1

:error
echo.
echo CHYBA: nieco zlyhalo, pozri vypis vyssie.
exit /b 1
