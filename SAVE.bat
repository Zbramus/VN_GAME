@echo off
cd /d "%~dp0"

echo === Chiffrement des images sensibles ===
python save_images.py
if errorlevel 1 (
    echo [!] Le chiffrement a echoue, arret pour eviter de pousser des images en clair.
    pause
    exit /b 1
)

echo === Sauvegarde du projet en cours ===

git add .
git commit -m "Session du %date% a %time%"
git push

echo === Restauration des images en clair pour continuer a travailler ===
python pull_images.py

echo === Termine ===
pause
