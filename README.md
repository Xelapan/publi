# Configuracion Pantalla publicidad
## _Xelapan_

Repo para implementar en las pantallas de publicidad en Xelapan, para losiguiente es verificar las configuraciones necesarias para el correcto funcionamiento del archivo `config.json`

## JSON

Se puede configurar de dos maneras el archivo json:
- Repositorio GIT
- Repositorio LOCAL

Si el JSON tiene configurado la `OPTION = 0` hace uso del Repositorio GIT donde se agrego previamente el link del repositorio a utilizar
de lo contrario con la configuracion `OPTION = 1` hace uso del Repositorio LOCAL en la cual se debe tener previamente las imagenes que son obtenidas a traves de un JSON para luego descargar las imagenes que estan en el servidor LOCAL

## TIME

Se tiene tres variables para la configuracion del _TIME_ donde se encuentra lo siguiente:

- APAGAR:  se debe definir horario en formato de 24hrs solo hora donde empieza a verificar cambios en el repositorio
- ENCENDER: se define el horario donde se termina la comprobacion y actualizacion del repositorio
- UPDATE: se define horario para comprobar si existen cambios en el repositorio GIT


## ARCHIVOS

Crear los archivos siguientes necesarios

Archivo para registrar los logs de publicidad
```sh
touch log_publicidad
```

Archivos para registrar los logs de eventos en el script de python
```sh
touch error.log
```
