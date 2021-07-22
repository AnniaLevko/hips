
import os
import subprocess
import datetime

import sys
sys.path.append('./herramientas/')
import crear_csv, enviar_mail, escribir_log

BLACK_LIST_SNIFFER_TOOLS = ["tcpdump", "ethereal", "wireshark"]
BLACK_LIST_LIBRARIES = ["libpcap"]

LOGS_NET_INT_PROMISCOUS_COMMAND = "cat /var/log/messages | grep -i promis"

NET_INT_TO_CHECK = ["lo", "virbr0", "virbr0-nic", "enp0s3"]

USERS_ALLOWED_TO_USE_SNIFFER_TOOLS = ["erwaen", "root"]

 

def buscar_y_mover_archivo_cuarentena(file_name):
    command = f"sudo find / -name {file_name} 2>/dev/null -type f" # buscamos en toda la raiz (/) el archivo, y solo queremos lo que son archivos y no directorios (type -f)
    paths_encontrados = os.popen(command).read().split("\n") # Ejecutamos el comando y guardamos en una lista los resultados
    paths_encontrados.pop(-1) # eliminamos el ultimo elemento que es un ""
    
    script_dir = os.path.dirname(os.path.abspath(__file__)) # <-- consigo el path de este script (/home/erwaen/developer/hips/sniffers)
    path_proyecto = os.path.normpath(script_dir + os.sep + os.pardir) # vuelvo un directorio atras (/home/erwaen/developer/hips)
   
    print(path_proyecto)
    append_write = ""
    if os.path.exists(path_proyecto + '/resultados/sniffers/chequear_sniffer_tools.csv'):
        append_write = "a"
    else:
        append_write = "w"    
    with open (path_proyecto + '/resultados/sniffers/chequear_sniffer_tools.csv', append_write) as f:
        
        f.write("\n")
        for path in paths_encontrados:
            
            #Procedemos a mover el arhivo 
            new_file_name = path[1:].replace("/", "-")
            new_path = "/cuarentena/sniffer_tools/" + new_file_name

            os.system(f"sudo mv {path} {new_path}")

            time_actual = datetime.datetime.now()
            
            f.write(str(time_actual)  +"," + path + ",--->," + new_path + ",\n")

    print(paths_encontrados)

def check_sniffer_tools():

    resultados_sniffers_tools = [] # Lista de diccionarios que diga que herramineta se esta ejecutando con su pid y quien

    
    cuerpo_mail = asunto_mail = ''

    for tool in BLACK_LIST_SNIFFER_TOOLS:

        command = f"ps -aux | grep {tool} | grep -v grep |  awk '{{print $1, $2, $NF}}'"
        resultados_command = os.popen(command).read().split("\n")

        resultados_command.pop(-1) # Eliminamos el ultimo elemento porque es un string vacio

        for result in resultados_command:

            result_in_list = result.split(" ")
            
            process = {
                "user" : result_in_list[0],
                "pid" : result_in_list[1],
                "command" : result_in_list[2] 
            }
            
            # Si el "ps -aux | grep" encontro algo, entonces debemos analizar si un usuario valido esta usando o no
            if result != "":

                
                counter = 0
                for user in USERS_ALLOWED_TO_USE_SNIFFER_TOOLS:
                    
                    if user.lower() in result.lower():
                        process["habilitado"] = "SI"
                        escribir_log.escribir_log(alarmas_o_prevencion='alarmas', tipo_alarma='SNIFFER TOOL', ip_o_email= user, motivo=f"Se detecto una herramienta de sniffer: '{tool}' pero el usuario '{user}' esta habilitado para usar." )
                        print(f"Se detecto una herramienta de sniffer: '{tool}' pero el usuario '{user}' esta habilitado para usar.")
                    else:
                        counter = counter + 1

                # Si ningun usario de la lista blanca es el que esta usando entonces procedemos a hacer los sgtes pasos
                if counter == len(USERS_ALLOWED_TO_USE_SNIFFER_TOOLS):
                    process["habilitado"] = "NO"
                    print(
                        f"El usuario '{process['user']}'esta ejecutando la herramienta de sniffer ({tool}) pero este usuario no se encuentra en la lista blanca."
                        + "\n\n" + "Se procesara a matar el proceso y buscar la herramienta y llevarlo a una carpeta de cuarentena........"
                    )
                    
                    process['usa libreria sniffer'] = check_libraries(process["pid"]) # imprime si detecto la libreria libpcap en este proceso

                    os.system(f"sudo kill -9 {process['pid']}") # Matamos el proceso
                    print(f"Proceso {process['pid']} matado....")

                    buscar_y_mover_archivo_cuarentena(tool)
                    cuerpo_mail = cuerpo_mail + f"\nEl usuario {process['user']} esta ejecutando la herramienta de sniffer ({tool}) pero este usuario no se encuentra en la lista blanca. Se mato el proceso, se busco la herramienta y se llevo a una carpeta de cuarentena.\n"
                    escribir_log.escribir_log(alarmas_o_prevencion='prevencion', tipo_alarma='SNIFFER TOOL', ip_o_email=user, motivo= f"El usuario {process['user']} esta ejecutando la herramienta de sniffer ({tool}) pero este usuario no se encuentra en la lista blanca. Se mato el proceso, se busco la herramienta y se llevo a una carpeta de cuarentena.")
                    print("Archivo encontrado y movido a cuarentena....")
                    
                    


                resultados_sniffers_tools.append(process)
  
    if not len(resultados_sniffers_tools):
        print("No se encontro ninguna herramienta de sniffer utilizando")

        crear_csv.write_csv(
            carpeta='sniffers', 
            nombre_archivo='chequear_sniffer_tools', 
            headers_list=['Usuario', 'PID','comando', 'habilitado', 'usa libreria sniffer'], 
            lista=resultados_sniffers_tools, 
            mensaje="no se encontro herramientras de sniffer"
        )
    else:
        enviar_mail.enviar_mail_asunto_body(
            tipo_alerta="PREVENCION", 
            asunto="SE ENCONTRO HERRAMIENTA SNIFFER!", 
            cuerpo=cuerpo_mail
        )
        crear_csv.write_csv(
            carpeta='sniffers', 
            nombre_archivo='chequear_sniffer_tools', 
            headers_list=['Usuario', 'PID','comando', 'habilitado', 'usa libreria sniffer'], 
            lista=resultados_sniffers_tools, 
            mensaje="Los procesos que no estan habilitados se procedio a matar buscar la herramienta y moverlo a cuarentena"
        )


#Detecta si el proceso esta utilizando una libreria de libpcap
def check_libraries(pid):
    command = f"sudo lsof -p {pid} -e /run/user/1000/gvfs  | grep libpcap" # comando parar verificar si la libreria libpcap esta siendo usada
    resultado_comando = os.popen(command).read().split("\n") # Ejecutamos el comando y guardamos en una lista las lineas
    resultado_comando.pop(-1)  # Eliminamos el ultimo elemento porque es un string vacio
    print(resultado_comando)
    # Si la lista es vacia es porque no encontro nada
    if not len(resultado_comando):
        return "no"
    else:
        return "yes"
    



#



# log_promiscuo_mode()
# check_net_interfaces()
check_sniffer_tools()





