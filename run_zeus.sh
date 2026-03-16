#!/bin/bash
# run_zeus.sh - Lanzador oficial para Zeus Engine

# Obtener el directorio real del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# SEGURIDAD: Prevenir ejecución como ROOT/SUDO
if [ "$EUID" -eq 0 ]; then
   echo "❌ ERROR: No puedes ejecutar Zeus Engine con 'sudo'."
   echo "   Las aplicaciones gráficas fallan al ser ejecutadas como root."
   echo "   Ejecuta simplemente: ./run_zeus.sh"
   exit 1
fi

# 1. Verificar si existe el entorno virtual
VENV_DIR="$SCRIPT_DIR/venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "⚠️  Entorno virtual no encontrado. Ejecutando setup inicial..."
    ./setup_zeus.sh
else
    # 2. Pre-validación de SUDO (Importante para que Zeus funcione internamente)
    echo "🔑 Solicitando permisos para optimización..."
    sudo -v || exit 1
    
    # 3. Activar y Lanzar
    echo "⚡ Lanzando Zeus Engine 2.0..."
    source "$VENV_DIR/bin/activate"
    export PYTHONPATH=$PYTHONPATH:.
    python3 main.py
fi
