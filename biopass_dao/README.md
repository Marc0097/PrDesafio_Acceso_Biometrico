# BioPass DAO

Sistema de control de accesos biométrico utilizando Python, PostgreSQL, OpenCV y Tkinter.

## Requisitos Previos

- Python 3.x
- PostgreSQL instalado y ejecutándose.

## Instalación

1.  Crea un entorno virtual (opcional pero recomendado):
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

2.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Configuración de la Base de Datos

1.  Crea una base de datos en PostgreSQL llamada `biopass_db` (o el nombre que prefieras).
2.  Ejecuta el script SQL para crear las tablas:
    - Puedes usar pgAdmin o la línea de comandos:
      ```bash
      psql -U postgres -d biopass_db -f db/create_tables.sql
      ```
3.  Configura el archivo `.env`:
    - Abre el archivo `.env` y ajusta `DB_USER`, `DB_PASSWORD` etc. según tu configuración local.

## Ejecución

Para iniciar la aplicación, ejecuta desde la carpeta `biopass_dao`:

```bash
python src/biopass_app.py
```
