@echo off
TITLE SOLPI-OS SINGULARITY BOOTLOADER
COLOR 0A
SET PYTHONPATH=%~dp0
echo ---------------------------------------------------------
echo 🚀 SOLPI-OS SINGULARITY v70.6 (Enterprise Elite)
echo ---------------------------------------------------------
echo [BOOT]: Local: %~dp0
echo [BOOT]: Verificando Ambiente Virtual...

set VENV_PATH=%~dp0.venv
set PYTHON_EXE=%VENV_PATH%\Scripts\python.exe

if not exist "%PYTHON_EXE%" (
    echo ❌ ERRO: Ambiente Virtual não encontrado. Criando...
    py -m venv .venv
)

echo [BOOT]: Sincronizando Dependências Críticas...
"%PYTHON_EXE%" -m pip install --upgrade pip
"%PYTHON_EXE%" -m pip install psutil torch transformers accelerate safetensors sentencepiece peft trl datasets pymysql pyautogui pygetwindow beautifulsoup4 python-dotenv requests

echo.
echo [BOOT]: Iniciando Consciência SOLPI...
"%PYTHON_EXE%" "%~dp0solpi_agent.py"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 🚨 O SISTEMA PAROU (Erro: %ERRORLEVEL%)
    echo Verifique se o drive E: está acessível e se não há processos travados.
)
pause
