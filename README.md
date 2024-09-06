# CertiGenerator

CertiGenerator es una herramienta que permite generar certificados de manera rápida y sencilla. A continuación, se explican tres formas diferentes de proceder dependiendo del nivel de conocimientos técnicos y las preferencias de uso.


## 1. Usar el Programa Ejecutable (Sin Conocimientos Técnicos)

La forma más sencilla de utilizar CertiGenerator es descargando el ejecutable. Esta opción no requiere que tengas conocimientos de programación ni que instales Python.

Pasos para usar el ejecutable:

### Descargar el ejecutable:
    
        https://drive.google.com/file/d/12NCg_faFQ0Btc8UQhJXU5Cc_xKjEVMck/view?usp=sharing

### Ejecutar el programa:
    
        Abre el archivo descargado y sigue los siguientes pasos:
        
            * Introduce el CIF (Código de Identificación Fiscal) y la razón social de la empresa en los campos correspondientes.
            * En Tipo de algoritmo, selecciona RSA.
            * Haz clic en el botón Generar Certificado.
            * Una vez generado el certificado, pulsa el botón Descargar ZIP.
            * Dentro del archivo ZIP encontrarás un fichero .txt, que es el que debes adjuntar en la solicitud de Alta en Consellería.

Esta es la opción más directa y rápida, especialmente diseñada para usuarios que prefieren no interactuar con código o configuraciones técnicas.



## 2. Usar Python para Ejecutar el Programa (Conocimientos Básicos)

Si tienes conocimientos básicos de programación o prefieres utilizar Python, también puedes ejecutar el programa descargando el script y sus dependencias.
Pasos para usar el programa con Python:


   ### Instalar Python (si no lo tienes instalado):
   
        * Descarga la última versión de Python desde python.org.
        * Durante la instalación, asegúrate de seleccionar la opción "Add Python to PATH".
        * Una vez instalado, abre una terminal (cmd o PowerShell) y verifica la instalación ejecutando: python --version

   
   ### Descargar el script y los requisitos:

    * Descarga el script certi_generator.py desde el siguiente enlace: Descargar Script.
    * Descarga el archivo de requisitos para instalar las dependencias necesarias: Descargar Requisitos.

   
   ### Instalar las dependencias:

    Abre la terminal y navega hasta la carpeta donde descargaste el script y el archivo requirements.txt. Luego ejecuta:

    bash

    pip install -r requirements.txt

   
   ### Ejecutar el programa:

    Una vez instaladas las dependencias, ejecuta el programa con el siguiente comando:

    bash

        python certi_generator.py

    ### Uso del programa:
    
        Al igual que en la opción del ejecutable, introduce el CIF, la razón social de la empresa, selecciona RSA como tipo de algoritmo, y haz clic en Generar Certificado.
        Una vez generado, pulsa el botón Descargar ZIP para obtener el archivo .txt que debes adjuntar en la solicitud de Alta en Consellería.



## 3. Seguir la Guía de Consellería (Procedimiento Manual)

La tercera opción consiste en seguir la guía oficial proporcionada por la administración pública para generar el certificado. Este procedimiento es más técnico y está dirigido a usuarios que desean realizar todo el proceso de manera manual.
