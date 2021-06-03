import subprocess

try:
    subprocess.run("w")
except Exception:
    print("No se pudo mostrar los usuarios conectados")
