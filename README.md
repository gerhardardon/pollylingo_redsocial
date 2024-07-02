# POLLYLINGO RED SOCIAL
## Descripcion del proyecto
**Curso: Seminario de sistemas 1
Universidad de San Carlos de Guatemala** 

Este proyecto fue realizado en grupos de tres personas, consiste en el desarrollo de una aplicacion web para el aprendizaje de idiomas en apoyo a los estudiantes de la Ecuela de Aprendizaje de Lenguas de La Universidad San Carlos de Guatemala CALUSAC.
Podra ver mas informacion sobre la interfaz y el uso del mismo leer **"users manual.pdf"** en el repositorio

Esta aplicacion web consiste de la creacion y comentarios de posts de distintos idiomas, permitiendo la traduccion y la lectura del texto utilizando servicios de Amazon AWS. 

En los posts se podra comentar y mostrar tags creadas automaticamente por servicios AWS. Ademas de la suscripcion y manejo de "retos" que seran enviados por medio de correos electronicos 
## Servicios y tecnologias utilizadas
 Amazon aws
 - EC2
 - S3
 - RDS
 - Rekognition
 - Lex
 - Polly
 - Translate
 - SES
 
 Bases de datos
 - MySql
 
 Backend 
 - Flask
 - python
 
 Frontend
 - React
 
# Manual Técnico para la Configuración del Proyecto 🖼️

Este manual técnico proporciona una guía paso a paso para la configuración y despliegue de un proyecto que utiliza REACT, Node.js junto con Flask, y un load balancer. Se incluyen detalles técnicos sobre la configuración de SSH desde PowerShell y el manejo de dependencias y entornos virtuales en Python.

## Creación de un Nuevo Correo Electrónico para el Sitio Web

1. Para la creación de un correo electrónico dedicado al sitio web, se recomienda utilizar servicios como Google Workspace o Microsoft 365, que permiten una gestión profesional y segura del correo.

## Configuración de REACT

1. Asegúrate de tener instalado Node.js y npm en tu sistema.
2. Utiliza `npx create-react-app my-app` para crear una nueva aplicación React.
3. Navega dentro del directorio de tu aplicación utilizando `cd my-app`.
4. Inicia la aplicación con `npm start`.

## Configuración de Node + Flask

1. **Instalación de Flask y Flask-SQLAlchemy:**

    ```bash
    pip install Flask SQLAlchemy Flask-SQLAlchemy
    ```

    Nota: Flask-SQLAlchemy puede ser eliminado si no se requiere manejo de bases de datos.

2. **Configuración de Entorno Virtual:**

    Crear un entorno virtual permite gestionar las dependencias de manera aislada.

    ```bash
    python3 -m venv venv # Crea un nuevo entorno virtual
    source venv/bin/activate # Activa el entorno virtual
    ```

3. **Instalación de Dependencias:**

    Asegúrate de tener un archivo `requirements.txt` con todas las dependencias del proyecto.

    ```bash
    pip install -r requirements.txt
    ```

## SSH desde PowerShell

Para configurar SSH en PowerShell para conectarse a una instancia EC2 de AWS, sigue estos pasos:

1. **Configuración de Permisos para la Llave SSH:**

    ```powershell
    $path = ".\aws-ec2-key.pem"
    icacls.exe $path /reset
    icacls.exe $path /GRANT:R "$($env:USERNAME):(R)"
    icacls.exe $path /inheritance:r
    ```

2. **Conexión SSH:**

    Utiliza el siguiente comando para conectarte a tu instancia EC2, reemplazando `ec2-user@your-ec2-instance` con tu dirección específica y `aws-ec2-key.pem` con tu archivo de clave:

    ```bash
    ssh -i "aws-ec2-key.pem" ec2-user@your-ec2-instance.amazonaws.com
    ```

## Utilización de AWS

Para el despliegue del proyecto en AWS, considera lo siguiente:

1. Utiliza EC2 para la instancia de servidor donde se alojará tu aplicación.
2. Configura un Load Balancer para distribuir el tráfico entre múltiples instancias y asegurar la disponibilidad.
3. Asegúrate de configurar los Grupos de Seguridad adecuados para permitir el acceso a los puertos necesarios (por ejemplo, el puerto 80 para HTTP y el puerto 443 para HTTPS).

Para más detalles sobre la configuración específica en AWS, visita la documentación oficial de AWS o consulta guías específicas basadas en tu arquitectura y necesidades del proyecto.

## Imágenes

Las imágenes mencionadas en el manual deben ser revisadas y reemplazadas por enlaces directos o subidas a un servidor de imágenes para garantizar su accesibilidad.

---

# Ingreso a AWS 
![image](https://github.com/Vallit0/PR1_SSG1/assets/79114580/37f7d768-4318-450e-a723-2b2cbe56e9f0)
Luego del ingreso a AWS se pueden verificar algunas secciones dentro de la creación de instancias. Dichas instancias deben ser conectadas por medio de ciertos puertos y configuracion de algunos puntos de seguridad. 
![image](https://github.com/Vallit0/PR1_SSG1/assets/79114580/77100548-1b6c-4891-8d74-3dc49287f942)

## EC2 - instancias generales
![image](https://github.com/Vallit0/PR1_SSG1/assets/79114580/7ecff682-b94d-4978-97bb-e6e7644f51cf)

# Confoguracion S3 
Dentro del S3 se realizaron 
![image](https://github.com/Vallit0/PR1_SSG1/assets/79114580/cf94e632-e34c-41a2-bb2c-16fe1bf88ca2)

![image](https://github.com/Vallit0/PR1_SSG1/assets/79114580/d1628133-a6d8-41c6-8791-07ec8a492556)

![image](https://github.com/Vallit0/PR1_SSG1/assets/79114580/3c6bf4a5-de27-4b00-8567-6b49b0c1777c)

# Creacion de Chatbot



    ```bash
    npm install react-simple-chatbot --save
    ```

# Implementacion de SDK 


```
pip install boto3
``
