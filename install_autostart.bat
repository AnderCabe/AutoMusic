@echo off
chcp 65001 > nul
title Instalando AutoMusic en Inicio

echo =========================================
echo    INSTALANDO AUTOMUSIC EN EL INICIO
echo =========================================
echo.

REM Crear carpeta de logs si no existe
if not exist "logs" mkdir "logs"

REM Crear tarea programada con TU comando favorito
echo [1/2] Creando tarea programada...
schtasks /create /tn "AutoMusic" /tr "cmd /c start /B pythonw \"%~dp0automusic.pyw\"" /sc onlogon /ru %username% /rl highest /f

if %errorlevel% equ 0 (
    echo ✓ Tarea creada: "AutoMusic"
    echo ✓ Comando: start /B pythonw automusic.pyw
) else (
    echo ✗ Error creando tarea
    pause
    exit /b 1
)

REM Crear script de inicio rapido
echo [2/2] Creando script de inicio rapido...
echo @echo off > "start_silent.bat"
echo start /B pythonw "%%~dp0automusic.pyw" >> "start_silent.bat"
echo exit >> "start_silent.bat"

echo.
echo =========================================
echo    INSTALACION COMPLETADA
echo =========================================
echo.
echo ✓ AutoMusic se ejecutara al iniciar sesion
echo ✓ Con tu comando favorito: start /B pythonw
echo ✓ Sin ventanas de consola
echo.
echo Para iniciar manualmente ahora:
echo   1. start_silent.bat
echo   2. O: start /B pythonw automusic.pyw
echo.
echo Para desinstalar: Ejecuta uninstall_autostart.bat
echo.
echo Iniciando AutoMusic ahora...
start /B pythonw "automusic.pyw"
echo ✓ AutoMusic iniciado en segundo plano
echo.
pause