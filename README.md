# ⚡ Zeus Engine v1.0 (ZUO 2.0 Universal) 💎

Zeus Engine es una suite de optimización premium para Linux, diseñada para maximizar el rendimiento y eliminar el micro-stuttering. Originalmente enfocado en plataformas X99, esta versión 2.0 es **Universal y Adaptativa**, identificando tu hardware y aplicando solo lo que necesitas.

## 🚀 Características Principales

### 🛸 Motor Adaptativo (Nativo Python)

- **Detección Automática**: Identifica si tu sistema es un X99 (Chipset Chino), Desktop Estándar o Laptop.
- **Parches de Kernel Inteligentes**: Aplica parámetros de GRUB (como nct6775) solo si son necesarios para tu hardware.
- **Zero-Dependency Core**: La lógica de optimización se ha migrado de Bash a módulos de Python puro para mayor velocidad y robustez.

### 💎 Interfaz Premium (v2.5 Stable)

- **Sudo GUI (pkexec)**: Autoriza la aplicación mediante diálogos nativos del sistema sin comprometer la estabilidad visual.
- **Multivista**: Dashboard, Optimización, Hardware y Panel de Scripts Adicionales.
- **Log Nativo**: Visualización en tiempo real de cada paso técnico, duplicado en la terminal para transparencia total.

### ⚙️ Centro de Optimización Universal

- **Dynamic Janitor**: Limpieza profunda de RAM PageCache, logs de sistema (journald) y cache de paquetes (apt).
- **GameMode & CPU**: Gestión del perfil 'Performance' y monitoreo del estado del demonio Feral GameMode.
- **Network Stack (Low Latency)**: Ajustes de TCP FastOpen y Stack de baja latencia para optimizar el ping en juegos competitivos.
- **Thermal Sync**: Reinicio y sincronización inteligente del servicio `fancontrol`.

### 🧩 Plugin System (Manifest-Based)

Zeus Engine es ahora **100% modular**. Puedes añadir tus propios scripts de optimización en la carpeta interna `/scripts`.

- **Formato Nativo**: Soporte exclusivo para scripts `.py` con el fin de mantener un ecosistema limpio y rápido.
- **Manifest Inteligente**: Cada plugin declara sus metadatos (Nombre, Descripción, Categoría), permitiendo que la GUI genere tarjetas de control ricas e informativas.

## 🛠️ Instalación y Uso

1. **Clonar y Configurar**:

   ```bash
   cd zeus-engine
   ./setup_zeus.sh
   ```

2. **Lanzar la App (Sin Sudo delante)**:

   ```bash
   ./run_zeus.sh
   ```

## 🤖 El Futuro (Fase 4: IA)

La próxima evolución integrará el **Zeus Advisor**, un asistente basado en LLM que analizará los logs de tu hardware y te dará recomendaciones personalizadas de optimización.

---

*Desarrollado para la comunidad de gaming en Linux.* 🐧🎮⚡
