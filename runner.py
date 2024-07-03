import subprocess

command = "clear && black . && uvicorn api.main:app --reload"

# Ejecutar el comando
subprocess.run(command, shell=True)
