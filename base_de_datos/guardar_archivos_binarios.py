import subprocess
import os
import psycopg2
from principal import cur, conn

def borrar_archivos_binarios():
    bd_command = (
        "TRUNCATE file;"
        "DELETE FROM file;"
    )
    
    cur.execute(bd_command)
    conn.commit()
    


PASSWD_DIR = "/etc/passwd"
SHADOW_DIR = "/etc/shadow"
DIRS = [PASSWD_DIR, SHADOW_DIR]
def guardar_archivos_binarios():
    # Agarramos todos los archivos binarios del sistema
    # bin_path = "/bin/"
    # files_list = os.listdir(bin_path)


    #print(files_list)

    # Conseguimos el md5sum de cada archivo y guardamos en la base de datos
    for dir in DIRS:

        command = f"md5sum {dir}" #+ " | awk '{print $1}'"
        file_with_md5sum = os.popen(command).read().split() # Guardamos en una lista el nombre del archivo y su md5sum

        # Procedemos a guardar en la base de datos
        try:
            bd_command = (
                "INSERT INTO file(file_name, md5sum)"
                f"VALUES ('{file_with_md5sum[1]}', '{file_with_md5sum[0]}');"
            )
            cur.execute(bd_command)
        except Exception:
            print("no funco")
        
    conn.commit()

      

    
borrar_archivos_binarios()        
guardar_archivos_binarios()

