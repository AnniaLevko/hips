#!/bin/bash python3
import subprocess

# Ejecuta el comando de linux "who -H" 
# Para saber quienes son los usuarios conectados y desde donde.

try:
    byte_output = subprocess.check_output("who -H", shell=True) # El retorno es de tipo bytes y no str
    output = byte_output.decode('utf-8') # decodeamos para que sea str
    output = output.split('\n')
    
    output.pop(-1) # Eliminamos el ultimo valor de la lista que es un "'" que no se de donde sale
    for out in output:
        print(out)
    
    # Creamos o Reescribimos en un txt con el nombre de este programa .py
    with open("./resultados/usuarios_conectados.txt", "w") as f:
        for out in output:
            f.write(out + "\n")
        
    
except Exception:
    print("No se pudo mostrar los usuarios conectados")
