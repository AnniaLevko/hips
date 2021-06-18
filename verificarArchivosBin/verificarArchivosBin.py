import subprocess
import os

def guardar_archivos_binarios():
    # Agarramos todos los archivos binarios del sistema
    bin_path = "/bin/"
    files_list = os.listdir(bin_path)

    #print(files_list)

    # Conseguimos el md5sum de cada archivo
    for file in files_list:
        command = f"md5sum /bin/{file}" + " | awk '{print $1}'"
        md5sum_file = os.popen(command).read().replace('\n', "") # Guardamos el md5sum 
        print(md5sum_file)
        
guardar_archivos_binarios()