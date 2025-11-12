#!/bin/bash
# Esperar a que haya conexión a internet
echo "Verificando conexión a Internet..."
until ping -c 1 8.8.8.8 &>/dev/null; do
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Esperando conexión a Internet..."
    sleep 5
done
echo "$(date '+%Y-%m-%d %H:%M:%S') - Conexión establecida ▒^|^e"

# Asegurar UTF-8 para Python
export PYTHONIOENCODING=utf-8
export LANG=C.UTF-8
export LC_ALL=C.UTF-8

# Esperar a que el monitor esté encendido
echo "Verificando monitor..."
DISPLAY=${DISPLAY:-:0}
export DISPLAY

if xrandr | grep " connected " &>/dev/null; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Monitor detectado ▒^|^e"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - No se detecta monitor, esperando..."
    until xrandr | grep " connected " &>/dev/null; do
        sleep 5
    done
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Monitor conectado ▒^|^e"
fi

cd /home/$USER/Desktop/publi/ || exit
. venv/bin/activate || exit
echo "$(date '+%Y-%m-%d %H:%M:%S') - Iniciando presentación..."
python3 publi.py

