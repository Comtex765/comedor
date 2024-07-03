import subprocess

command = "cls && black . && uvicorn api.main:app --reload"
# command = "uvicorn api.main:app --host 0.0.0.0 --port $PORT"

# Ejecutar el comando
subprocess.run(command, shell=True)
