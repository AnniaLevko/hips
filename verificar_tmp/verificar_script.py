import os

import sys
sys.path.append('./herramientas/')
import crear_csv 

# Verificamos si hay archivos en /tmp que contengan al comienzo #!
def verificar_script():
    command = f"sudo find /tmp 2>/dev/null -type f" # buscamos en el directorio tmp los archivos, y solo queremos lo que son archivos y no directorios (type -f)
    archivos = os.popen(command).read().split()
    
    archivos_a_cuarentena = []
    # Procedemos a verificar los archivos
    for archivo in archivos:
        new_diccionary = {}
        
        # Si el archivo es un py, cpp, c, exe, sh, ruby, php, entra en el if
        if any(substring in archivo for substring in [".cpp", ".py", ".c", ".exe", ".sh", ".ruby", ".php"]):
            new_diccionary['ruta_archivo'] = archivo
            new_diccionary['ruta_a_mover'] = "/cuarentena/tmp_scripts/" + archivo[1:].replace("/", "-")
            new_diccionary['motivo'] = "Es un archivo tipo con extension sospechosa (.py .sh etc)"
            archivos_a_cuarentena.append(new_diccionary)
        else: # Si no, busca si el archivo tiene un #! en la primera linea, lo cual significa que es un archivo script
            try:     
                with open(f"{archivo}", "r") as f:
                    primera_linea = f.readline() # Leemos la primera linea del archivo
                    if "#!" in primera_linea:
                        new_diccionary['ruta_archivo'] = archivo
                        new_diccionary['ruta_a_mover'] = "/cuarentena/tmp_scripts/" + archivo[1:].replace("/", "-")
                        new_diccionary['motivo'] = "Es un archivo tipo script (#!)"
                        archivos_a_cuarentena.append(new_diccionary)
            except Exception:
                print("El archivo esta codeado en bytes")
        
    for archivo in archivos_a_cuarentena:
        try:
            os.system(f"sudo mv {archivo['ruta_archivo']} {archivo['ruta_a_mover']}")
        except Exception:
            print(f"No se pudo mover a cuarentena el archivo: {archivo}.")
    

    print(archivos_a_cuarentena)
    #Procedemos a escribir en el archivo
    if archivos_a_cuarentena:    
        mensaje = "Ya se movio los ultimos archivos"
    else:
        mensaje = "No se encontro archivos sospechosos en /tmp/"
    carpeta = "verificar_tmp"
    archivo_csv = "verificar_script"
    headers = ["Ruta_origen", "Ruta_destino", "Motivo"]
    if os.path.exists(f'./resultados/{carpeta}/{archivo_csv}.csv'):
        crear_csv.append_csv(mensaje=mensaje, carpeta=carpeta, nombre_archivo=archivo_csv, lista=archivos_a_cuarentena )
    else:
        crear_csv.write_csv(mensaje = mensaje, carpeta=carpeta, nombre_archivo=archivo_csv, lista = archivos_a_cuarentena, headers_list = headers)
    

    

    
        
        


verificar_script()