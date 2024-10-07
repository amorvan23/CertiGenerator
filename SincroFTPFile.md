Tutorial para sincronizar un fichero remoto desde un FTP a un directorio Local


Paso 1: Descargar el ejecutable desde:  https://drive.google.com/file/d/13BSDNlttA-bw2E7IhHUL1eeGC1Xx1dwR/view?usp=drive_link

Paso 2: Situar el ejecutable en el directorio deseado

Paso 3: Ejecutar el .exe

Paso 4: La primera vez que se ejecuta va a fallar, debido a que necesita de la configuración de las variables de entorno. (En la primera ejecución, se crea un config.ini en el mismo directorio del script)

Paso 5: Configurar el .ini

Ejemplo .ini:


[FTP]

Host = host_ftp

port = 21

user = prohibidos

password = password_ftp

protocol = ftp


[LOCAL]

download_path = C:/Users/Default/Downloads/

remote_file = prohibidos.csv


[MYSQL]

host = host_mysql

database = prohibidos_descargas

user = user_mysql

password = password_mysql





Paso 6: Una vez configurado y gurdado el fichero, ya podemos ejecutar el .exe

IMPORTANTE: El config.ini debe de estar en el mismo directorio que el .exe, cada vez que se ejecuta, añade logs a un fichero .log del mismo directorio. 
SI el fichero de logs dice que no se puede encontrar el archivo, seguramente es porque en la ruta download_path, le hemos puesto una ruta local incorrecta. 
Si al ejecutar la aplicacion aparece una pantalla de error indicando error connection, muy probablemente sea porque las variables del apartado MYSQL no son correctas.
Si el log contiene mensajes de error de permiso, muy probablemente se deba a que el directorio en el que tratamos de escribir el archivo requiere permisos elevados. (Para elevar permisos, crear acceso directo del .exe y darle permisos de administrador.)
Si el fichero remoto ya ha sido sincronizado el script lo detectará y no lo sincronizará de nuevo hasta que el fichero remoto cambie.

Para un correcto funcionamiento, marcar una tarea programada cada día a las 9:15 con repetición cada 30 minutos. 

