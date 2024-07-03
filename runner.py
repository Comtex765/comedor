import subprocess

command = "uvicorn api.main:app --host 0.0.0.0 --port $PORT" #"cls && black . && uvicorn api.main:app --reload"

# Ejecutar el comando
subprocess.run(command, shell=True)
