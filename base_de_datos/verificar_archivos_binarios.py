import os
from principal import *


passwd_dir = "/etc/passwd"
shadow_dir = "/etc/shadow"
directorios = [passwd_dir, shadow_dir]
def comparar_md5sum(dirs):
    
    files = [] # guardamos en una lista de diccionarios los md5sum actuales del sistema

    # Obtenemos los md5sum actuales del sistema y guardamos en una lista
    for dir in dirs:
        command = f"md5sum {dir}" #+ " | awk '{print $1}'"
        file_with_md5sum = os.popen(command).read().split() # Guardamos en una lista el nombre del archivo y su md5sum
        
        if file_with_md5sum:
            file = {
                "file_name" : file_with_md5sum[1],
                "md5sum" : file_with_md5sum[0]
            }
            files.append(file)
    # print(files) 

    # Comparamos los md5sum actuales con los md5sum de la base de datos.
    for file in files:
        
        # Buscamos en la base de datos el md5sum guardado
        cur.execute(f"SELECT * FROM file WHERE file_name='{file['file_name']}'")
        query = cur.fetchall() # Guardamos en query lo que retorno el comando de BD
        print(query)

        # comparacion si los md5sum siguen iguales o no
        if file['md5sum'] == query[0][2]: # query[0][2] el [0] porque query es una lista de un elemento, y el [2] porque es una tupla de 3 elementos y en la posicion 2 esta el md5sum que se guardo en la BD
            print("No hubo modificacion en", file['file_name'])
        else:
            print("Hubo modificacion! en", file['file_name'])


comparar_md5sum(directorios)   
