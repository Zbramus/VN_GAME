@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo === Recuperation des derniers changements ===

git pull

echo === Restauration des fichiers supprimes localement dans les dossiers d'images ===
for /f "usebackq delims=" %%L in ("crypt_targets.txt") do (
    set "line=%%L"
    if not "!line!"=="" if not "!line:~0,1!"=="#" (
        git checkout -- "!line!" 2>nul
    )
)

echo === Dechiffrement des images sensibles ===
python pull_images.py

echo === Nettoyage des fichiers temporaires Ren'Py ===

for /r %%f in (*.rpyc) do del "%%f"
for /r %%f in (*.rpymc) do del "%%f"

if exist "game\cache" rd /s /q "game\cache"

echo === Termine ===
pause