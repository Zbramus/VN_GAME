@echo off
echo === Sauvegarde du projet en cours ===

git add .
git commit -m "Session du %date% a %time%"
git push

echo === Termine ===
pause
