# Comedor ESPOCH

Comedor ESPOCH is an application designed for the management of reservations in the dining room of the Escuela Superior Politécnica de Chimborazo (ESPOCH). It uses a PostgreSQL database, the FastAPI framework in Python, and several other tools to provide a complete and efficient solution.

## Technologies Used

- **Python**: Main programming language.
- **FastAPI**: Framework for backend development.
- **PostgreSQL**: Database management system.
- **NextJS**: For frontend development.

## Prerequisites

- _Python 3.x installed on the system._
- _PostgreSQL configured and running._

## Project Structure

The project is organized as follows:

```plaintext
dining room/
│
├── api/
│ ├─── crud/ # CRUD operations
│ ├─── email/ # email's functionalities.
│ ├─── img/ # Temporary images in the application (QR's).
│ ├─── routes/ # API routes definition.
│ ├─── schemas/ # Pydantic data schemas.
│ ├─── utils/ # Miscellaneous utilities.
│ ├─── __init__.py # API module initialization file.
│ ├─── database.py # Database configuration.
│ ├─── main.py # Main entry point of the application
│ ├─── models.py # Database models definition.
│
├─── extra/ # Additional non-code specific files.
├─── sql/ # SQL files for the database.
├─── venv/ # Python virtual environment (ignored by git).
├─── .env # Environment variables configuration file.
├─── .gitignore # File to specify which files to ignore in git.
├─── index.html # Main HTML file.
├─── local_runner.py # Script for local execution
├─── requirements.txt # List of Python dependencies.
└─── runner.py # Main script for project execution in cloud.
```

## Installation and Configuration

### Step 1: Create a Virtual Environment

First, create a virtual environment to manage the project dependencies.

```bash
python -m venv venv
```

### 2. Activate the virtual environment

#### On Windows

```bash
.\venv\Scripts\activate.bat
```

#### On macOS/Linux

```bash
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure the .env file

Create an `.env` file in the root of the project with the following variables:

*Variables with text are fixed, depending on your case change the variables containing []*.

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

### Step 5: Local Execution

To run the project locally, you can use the `local_runner.py` script:

```bash
python local_runner.py
```

## Access to the application
The application will be up on localhost:8000

_FastAPI documentation is located in /docs and /redoc_
