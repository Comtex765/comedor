# Comedor ESPOCH

Comedor ESPOCH es una aplicación diseñada para la gestión de reservas en el comedor de la Escuela Superior Politécnica de Chimborazo (ESPOCH). Utiliza una base de datos PostgreSQL, el framework FastAPI en Python, y varias otras herramientas para proporcionar una solución completa y eficiente.

## Tecnologías Utilizadas

- **Python**: Lenguaje de programación principal.
- **FastAPI**: Framework para el desarrollo del backend.
- **PostgreSQL**: Sistema de gestión de bases de datos.
- **NextJS**: Para el desarrollo del frontend.

## Requisitos Previos

- Python 3.x instalado en el sistema.
- PostgreSQL configurado y en funcionamiento.

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```plaintext
comedor/
│
├── api/
│   ├── crud/              # Operaciones CRUD
│   ├── email/             # Funcionalidades de email's
│   ├── img/               # Imágenes temporales en la aplicación (QR's)
│   ├── routes/            # Definición de rutas de la API
│   ├── schemas/           # Esquemas de datos Pydantic
│   ├── utils/             # Utilidades diversas
│   ├── __init__.py        # Archivo de inicialización del módulo API
│   ├── database.py        # Configuración de la base de datos
│   ├── main.py            # Punto de entrada principal de la aplicación
│   ├── models.py          # Definición de modelos de la base de datos
│
├── extra/                 # Archivos adicionales no específicos del código
├── sql/                   # Archivos SQL para la base de datos
├── venv/                  # Entorno virtual Python (ignorado por git)
├── .env                   # Archivo de configuración de variables de entorno
├── .gitignore             # Archivo para especificar qué archivos ignorar en git
├── index.html             # Archivo HTML principal
├── local_runner.py        # Script para ejecución local
├── requirements.txt       # Lista de dependencias de Python
└── runner.py              # Script principal para ejecución del proyecto en cloud
```

## Instalación y Configuración

### Paso 1: Crear un Entorno Virtual

Primero, cree un entorno virtual para gestionar las dependencias del proyecto.

```bash
python -m venv venv
```

### 2. Activar el entorno virtual

#### En Windows

```bash
.\venv\Scripts\activate.bat
```

#### En macOS/Linux

```bash
source venv/bin/activate
```

### Paso 3: Instalar las dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar el archivo .env

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

*Variables con texto son fijas, según tu caso cambia las variables que contienen []*

```plaintext
DB_NAME=comedor
DB_HOST=[]
DB_PASSWORD=[]
DB_DIALECT=[]
DB_USER=comex
SECRET_KEY=mi_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
PASSWORD=Contraseña_de_encriptación
EMAIL_SENDER=ferchon123443@gmail.com
EMAIL_PASSWORD=tuhw uauo hwck smlq
IVA=0.15
```

### Paso 5: Ejecución Local

Para ejecutar el proyecto localmente, puedes utilizar el script `local_runner.py`:

```bash
python local_runner.py
```