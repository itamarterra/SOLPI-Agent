@echo off
SETLOCAL
TITLE SOLPI-OS SINGULARITY BOOTLOADER
COLOR 0A
SET "PYTHONPATH=%~dp0"
cd /d "%~dp0"

echo ---------------------------------------------------------
echo SOLPI-OS SINGULARITY v80.2 (Elite Engine)
echo ---------------------------------------------------------
echo [BOOT]: Local: %~dp0
echo [BOOT]: Verificando Ambiente Virtual...

set "VENV_PATH=%~dp0.venv"
set "PYTHON_EXE=%VENV_PATH%\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
    echo [BOOT]: Criando ambiente virtual...
    python -m venv .venv
)

echo [BOOT]: Validando e Instalando Dependencias...
"%PYTHON_EXE%" -m pip install requests pymysql pyautogui pygetwindow beautifulsoup4 numpy torch transformers python-dotenv concurrent-log-handler portalocker prompt_toolkit requests

echo.
echo [BOOT]: Iniciando Consciencia SOLPI...
"%PYTHON_EXE%" solpi_agent.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ALERT: O sistema parou (Erro: %ERRORLEVEL%)
    pause
)
ENDLOCAL
