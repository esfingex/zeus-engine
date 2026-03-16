#!/bin/bash
# setup_zeus.sh - Instalador de dependencias y lanzador para Zeus Engine

echo -e "⚡ \033[1;34mPreparando Zeus Engine (Instalador Universal)\033[0m"

# 1. Instalar dependencias de interfaz y fuentes
echo "📦 Instalando dependencias de interfaz y fuentes..."
sudo apt-get update && sudo apt-get install -y fonts-material-design-icons-iconfont libcanberra-gtk-module fonts-noto-color-emoji

# 1. Verificar/Instalar dependencias del sistema (Requiere sudo)
echo "🔍 Verificando herramientas del sistema..."

missing_apps=()
for app in pip3 dmidecode cpupower gamemoded; do
    if ! command -v $app &> /dev/null; then
        missing_apps+=($app)
    fi
done

if [ ${#missing_apps[@]} -gt 0 ]; then
    echo "📦 Faltan dependencias: ${missing_apps[*]}"
    echo "Instalando via APT..."
    sudo apt update
    # Mapa de nombres de apps a paquetes de apt
    for app in "${missing_apps[@]}"; do
        case $app in
            pip3) sudo apt install -y python3-pip ;;
            dmidecode) sudo apt install -y dmidecode ;;
            cpupower) sudo apt install -y linux-tools-common linux-tools-$(uname -r) ;;
            gamemoded) sudo apt install -y gamemode ;;
        esac
    done
fi

# 2. Configurar Entorno Virtual (VENV)
VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "🌐 Creando entorno virtual Python (venv)..."
    python3 -m venv "$VENV_DIR"
fi

echo "🔌 Activando entorno virtual..."
source "$VENV_DIR/bin/activate"

# 3. Instalar dependencias dentro del VENV
echo "🐍 Instalando dependencias desde requirements.txt..."
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    pip install flet rich
fi

# 4. Lanzar la aplicación
echo "🚀 Lanzando Zeus Engine (GUI Mode en VENV)..."
export PYTHONPATH=$PYTHONPATH:.
python3 main.py
