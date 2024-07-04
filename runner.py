import subprocess

command = "pip install --upgrade pip & uvicorn api.main:app --host 0.0.0.0 --port $PORT"
#command = "cls && black . && uvicorn api.main:app --reload"

# Ejecutar el comando
subprocess.run(command, shell=True)
