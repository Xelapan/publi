# Configuracion Pantalla publicidad

Repositorio para implementar en las pantallas de publicidad en Xelapan, para lo siguiente es verificar las configuraciones necesarias para el correcto funcionamiento del archivo `config.json`

---
## JSON

Se puede configurar de dos maneras el archivo json:
- Repositorio GIT
- Repositorio LOCAL

Si el JSON tiene configurado la `OPTION = 0` hace uso del Repositorio GIT donde se agrego previamente el link del repositorio a utilizar
de lo contrario con la configuracion `OPTION = 1` hace uso del Repositorio LOCAL en la cual se debe tener previamente las imagenes que son obtenidas a traves de un JSON para luego descargar las imagenes solo en formato `jpg` que estan en el servidor LOCAL

---
## TIME
Se tiene tres variables para la configuracion del _TIME_ donde se encuentra lo siguiente:

- APAGAR:  se debe definir horario en formato de 24hrs solo hora donde empieza a verificar cambios en el repositorio
- ENCENDER: se define el horario donde se termina la comprobacion y actualizacion del repositorio
- UPDATE: se define horario para comprobar si existen cambios en el repositorio GIT
---
## Creacion de archivos necesarios

Crear los archivos siguientes necesarios para el funcionamento del script de python.
>  Los archivos siguientes se debe crear desde este directorio donde estan los archivos del repositorio

Archivo para registrar los logs de publicidad
```sh
touch log_publicidad
```

Archivos para registrar los logs de eventos en el script de python
```sh
touch error.log
```

Crear carpeta en la cual se guardaran las imagenes descargadas de publicidad
```sh
mkdir publicidad
```
---

## Configuraciones
Se debe realizar los siguientes pasos para la configuracion
- Dar permiso de ejeucion al archivo `start.sh`
    ```sh
    chmod +x start.sh
    ```
- Dar permiso de ejeucion al archivo `inicio.sh`
    ```sh
    chmod +x inicio.sh
    ```
- Mover el archivo `inicio.sh` a la carpeta de inicio de linux
    ```sh
    mv inicio.sh /home/$USER/Desktop
    ```
- Configuracion de CRONTAB
    
    Abrir el archivo de configuracion de CRONTAB
    ```sh
    crontab -e
    ```
    > Agregar la informacion que esta en el archivo `crontab.txt` que esta adjunto a este repositorio

- Configuracion para que el arrance del script de python se ejecute al iniciar el OS automaticamente
    ```sh
   sudo nano /etc/rc.local
    ```
    > Agregar la informacion siguiente antes del `exit 0`
    ```sh
    sh /home/$USER/Desktop/start.sh
    ```
- Verificar el path del script que esta en el archivo `inicio.sh` si es necesario en indicar la ruta completa del script de python
    ```sh
    nano inicio.sh
    ```
***IMPORTANTE VERIFICAR EL PATH ESTE CORRECTAMENTE***
- _Nombre de usuario del Sistema Operativo_
- _Nombre de la carpeta de Escritorio o Desktop_
- Archivos a verificar:
    - `start.sh`
    - `inicio.sh`
    - `crontab.txt`
---

## Ejecucion del script manualmente
Las siguientes instrucciones son las necesarias para la ejecucion del script de python en la cual se puede realizar de dos maneras:
- Ejecucion por medio del archivo `start.sh`
    ```sh
    ./start.sh
    ```
    > Muy importante que este archivo debe estar ubicado en el escritorio del OS
- Ejecucion por medio del archivo `slideshw.py`
    ```sh
    python3 slideshw.py
    ```