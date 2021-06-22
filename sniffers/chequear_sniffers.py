
import os
import subprocess
import datetime

BLACK_LIST_SNIFFER_TOOLS = ["tcpdump", "ethereal", "wireshark"]
BLACK_LIST_LIBRARIES = ["libpcap"]

LOGS_NET_INT_PROMISCOUS_COMMAND = "cat /var/log/messages | grep -i promis"

NET_INT_TO_CHECK = ["lo", "virbr0", "virbr0-nic", "enp0s3"]

USERS_ALLOWED_TO_USE_SNIFFER_TOOLS = ["erwaen", "root"]

def log_promiscuo_mode(): 
    resultado_comando = os.popen(LOGS_NET_INT_PROMISCOUS_COMMAND).read().split("\n")
    resultado_comando.pop(-1)
    print(resultado_comando)
    print("\n\n")

def check_net_interfaces():
    promis_nets_active = []
    for net_int in NET_INT_TO_CHECK:
        command = f"ip a show {net_int} | grep -i promisc"
        resultado_ip_command = os.popen(command).read()
        print(resultado_ip_command)
        net_interface = {
            "int_name": "",
            "is_mode_promiscuo": ""
        }

        net_interface["int_name"] = net_int

        if "promisc" in resultado_ip_command.lower():
            
            net_interface["is_mode_promiscuo"] = "YES"
            print(f"La interfaz de red '{net_int}' esta en modo promiscuo")
        else:
            net_interface["is_mode_promiscuo"] = "NO"

        promis_nets_active.append(net_interface)

    print(promis_nets_active)





def buscar_y_mover_archivo_cuarentena(file_name):
    command = f"sudo find / -name {file_name} 2>/dev/null -type f" # buscamos en toda la raiz (/) el archivo, y solo queremos lo que son archivos y no directorios (type -f)
    paths_encontrados = os.popen(command).read().split("\n") # Ejecutamos el comando y guardamos en una lista los resultados
    paths_encontrados.pop(-1) # eliminamos el ultimo elemento que es un ""
    
    script_dir = os.path.dirname(os.path.abspath(__file__)) # <-- consigo el path de este script (/home/erwaen/developer/hips/sniffers)
    path_proyecto = os.path.normpath(script_dir + os.sep + os.pardir) # vuelvo un directorio atras (/home/erwaen/developer/hips)
   
    print(path_proyecto)
    with open (path_proyecto + '/resultados/sniffers/archivos_a_cuarentena.txt', 'a') as f:
        
        f.write("\n")
        for path in paths_encontrados:
            
            #Procedemos a mover el arhivo 
            new_file_name = path[1:].replace("/", "-")
            new_path = "/cuarentena/sniffer_tools/" + new_file_name

            os.system(f"sudo mv {path} {new_path}")

            time_actual = datetime.datetime.now()
            
            f.write(str(time_actual)  +" " + path + " ---> " + new_path + "\n")

    print(paths_encontrados)

def check_sniffer_tools():
    resultados_sniffers_tools = [] # Lista de diccionarios que diga que herramineta se esta ejecutando con su pid y quien

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

                    os.system(f"sudo kill -9 {process['pid']}") # Matamos el proceso
                    print(f"Proceso {process['pid']} matado....")

                    buscar_y_mover_archivo_cuarentena(tool)
                    print("Archivo encontrado y movido a cuarentena....")


                resultados_sniffers_tools.append(process)
  
    if not len(resultados_sniffers_tools):
        print("No se encontro ninguna herramienta de sniffer utilizando")
    else:
        print(resultados_sniffers_tools)








# log_promiscuo_mode()
# check_net_interfaces()
check_sniffer_tools()

