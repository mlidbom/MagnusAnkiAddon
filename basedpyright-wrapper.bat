@echo off
call "%~dp0venv\Scripts\activate.bat"
basedpyright --project basedpyright-wrapper-config.json
