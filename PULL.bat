@echo off
cd /d "%~dp0"

echo === Recuperation des derniers changements ===

git pull

echo === Dechiffrement des images sensibles ===
python pull_images.py

echo === Nettoyage des fichiers temporaires Ren'Py ===

for /r %%f in (*.rpyc) do del "%%f"
for /r %%f in (*.rpymc) do del "%%f"

if exist "game\cache" rd /s /q "game\cache"

echo === Termine ===
pause
