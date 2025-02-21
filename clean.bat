@echo off
echo Nettoyage des fichiers temporaires...
del /s /q *.pyc
del /s /q __pycache__
del /s /q *.log
echo Nettoyage terminé.
pause 