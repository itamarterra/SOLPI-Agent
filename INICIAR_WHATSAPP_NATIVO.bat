@echo off
chcp 65001 > nul
TITLE SOLPI-OS NATIVE WHATSAPP BRIDGE
COLOR 0B
echo ---------------------------------------------------------
echo 🌉 SOLPI-OS NATIVE WHATSAPP BRIDGE v80.2
echo ---------------------------------------------------------
echo [BOOT]: Verificando Node.js...
node -v > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ ERRO: Node.js não encontrado. Por favor, instale o Node.js v22+.
    pause
    exit /b 1
)

echo [BOOT]: Iniciando Bridge Baileys em E:\SOLPI-Agent\solpi-engine\scripts\whatsapp-bridge
cd /d "E:\SOLPI-Agent\solpi-engine\scripts\whatsapp-bridge"

echo [BOOT]: Conectando...
node bridge.js --port 3000

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 🚨 A BRIDGE PAROU (Erro: %ERRORLEVEL%)
    echo Verifique se a porta 3000 está livre.
)
pause
