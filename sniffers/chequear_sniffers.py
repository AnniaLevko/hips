
import os
import subprocess

BLACK_LIST_SNIFFER_TOOLS = ["tcpdump", "ethereal", "wireshark"]
BLACK_LIST_LIBRARIES = ["libpcap"]

LOGS_NET_INT_PROMISCOUS_COMMAND = "cat /var/log/messages | grep -i promis"

NET_INT_TO_CHECK = ["lo", "virbr0", "virbr0-nic"]

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



def check_sniffer_tools():
    for tool in BLACK_LIST_SNIFFER_TOOLS:
        command = f"ps -aux | grep {tool} | grep -v grep |  awk '{{print $1, $2, $NF}}'"
        resultados_command = os.popen(command).read().split("\n")
        print(resultados_command)
        for result in resultados_command:

            print("xd")
            if result != "":

                there_is_a__user = False
                counter = 0
                for user in USERS_ALLOWED_TO_USE_SNIFFER_TOOLS:
                    
                    print(result.lower())
                    if user.lower() in result.lower():
                        print(f"Se detecto una herramienta de sniffer: '{tool}' pero el usuario '{user}' esta habilitado para usar.")
                    else:
                        counter = counter + 1

                if counter == len(USERS_ALLOWED_TO_USE_SNIFFER_TOOLS):
                    print(f"Un usuario esta ejecutando esta herramienta de sniffer ({tool}) no se encuentra en la lista blanca.")

                
        


        else:
            "No hay ninguna herramienta de sniffer ejecutandose"








# log_promiscuo_mode()
# check_net_interfaces()
check_sniffer_tools()