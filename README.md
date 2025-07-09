# Proyecto de API Biblioteca - Diego Troche

## Descripción del Proyecto

Este proyecto es una API RESTful desarrollada con **Django** y **Django REST Framework** para gestionar una biblioteca. La aplicación permite manejar libros, autores, géneros literarios y calificaciones por parte de los usuarios. Además, incluye funciones para registrar usuarios, calificar libros y visualizar estadísticas relacionadas con las calificaciones y libros.

## Pasos para crear el proyecto

### 1. Crear una carpeta para el proyecto

Primero, crea una carpeta para tu proyecto. Puedes llamarla **Biblioteca** o el nombre que prefieras.

```bash
mkdir Biblioteca
cd Biblioteca
```
###2. Crear un entorno virtual
Entra en la carpeta del proyecto y crea un entorno virtual con el siguiente comando:
```bash
python -m venv venv
```
###3. Activar el entorno virtual
Una vez creado el entorno virtual, actívalo con:

Windows:
```bash
.\venv\Scripts\activate
```

### 4. Instalar las librerías necesarias

Con el entorno activado, instala las librerías necesarias utilizando el siguiente bloque de comandos:

```bash
# Instalar Django 4.2
pip install django==4.2  # Framework principal para el desarrollo web.

# Instalar psycopg2-binary
pip install psycopg2-binary  # Driver para conectar Django con bases de datos PostgreSQL.

# Instalar Django Rest Framework
pip install djangorestframework  # Proporciona herramientas para construir APIs RESTful en Django.

# Instalar Simple JWT
pip install djangorestframework-simplejwt  # Proporciona autenticación con tokens JWT para la API.
```






