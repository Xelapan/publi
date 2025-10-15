#!/bin/bash
# Esperar a que haya conexión a internet
while ! ping -c 1 8.8.8.8 &>/dev/null; do
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Esperando conexión a Internet..."
    sleep 5
done
# Esperar a que el monitor esté encendido
export DISPLAY=:0
while ! xrandr | grep " connected " &>/dev/null; do
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Esperando a que el monitor esté encendido..."
    sleep 5
done

cd /home/$USER/Desktop/publi/ || exit
. venv/bin/activate || exit
echo "$(date '+%Y-%m-%d %H:%M:%S') - Iniciando presentación..."
python3 publi.py
