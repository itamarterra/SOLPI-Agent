@echo off
TITLE SOLPI-OS SINGULARITY BOOTLOADER
COLOR 0A
SET PYTHONPATH=%~dp0
echo ---------------------------------------------------------
echo 🚀 SOLPI-OS SINGULARITY v70.5 (Enterprise Elite)
echo ---------------------------------------------------------
echo [BOOT]: Local: %~dp0
echo [BOOT]: Verificando Ambiente Virtual...

if not exist "%~dp0.venv\Scripts\python.exe" (
    echo ❌ ERRO: Ambiente Virtual não encontrado em %~dp0.venv
    echo Tentando inicializar ambiente...
    py -m venv .venv
    .venv\Scripts\python -m pip install psutil torch transformers accelerate safetensors sentencepiece peft trl datasets pymysql pyautogui pygetwindow beautifulsoup4 python-dotenv
)

echo [BOOT]: Iniciando SOLPI-OS...
"%~dp0.venv\Scripts\python.exe" "%~dp0solpi_agent.py"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 🚨 O SISTEMA PAROU (Erro: %ERRORLEVEL%)
    pause
)
pause
