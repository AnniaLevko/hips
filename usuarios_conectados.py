#!/bin/bash python3
import subprocess
import re

# Ejecuta el comando de linux "who -H" 
# Para saber quienes son los usuarios conectados y desde donde.

try:
    byte_output = subprocess.check_output("who -H", shell=True) # El retorno es de tipo bytes y no str
    output = byte_output.decode('utf-8') # decodeamos para que sea str
 
    output_list = output.split('\n')
    
    output_list.pop(-1) # Eliminamos el ultimo valor de la lista que es un "'" que no se de donde sale

    # Separamos en comas (,) cada palabra para despues crear un CSV
    for index, item in enumerate(output_list):
        output_list[index] = re.sub("\s+", ",", item.strip())
    

    # Renombramos los headers
    output_list[0] = "NAME,LINE,DATE,TIME,COMMENT"

    # Escribimos en un csv y dejamos los datos de tal manera
    # columna1,columna2,columna3
    # erwaen,daskldjls, fdsflsfsd
    # annia,dsjakdasjd, fdksladl
    with open ('./resultados/usuarios_conectados.csv', 'w') as csv_file:
        for item in output_list:
            csv_file.write(item + "\n")


    # Creamos o Reescribimos en un txt con el nombre de este programa .py
    # NO SE TODAVIA SI VAMOS A USAR ESTO.
    with open("./resultados/usuarios_conectados.txt", "w") as f:
        for out in output_list:
            f.write(out + "\n")
        
    
except Exception:
    print("No se pudo mostrar los usuarios conectados")
