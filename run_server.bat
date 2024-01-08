::cmd /k
@echo off
start /B waitress-serve --port=8000 armsbackend.wsgi:application