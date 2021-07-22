
import os
import subprocess
import datetime



BLACK_LIST_SNIFFER_TOOLS = ["tcpdump", "ethereal", "wireshark"]
BLACK_LIST_LIBRARIES = ["libpcap"]

LOGS_NET_INT_PROMISCOUS_COMMAND = "cat /var/log/messages | grep -i promis"

NET_INT_TO_CHECK = ["lo", "virbr0", "virbr0-nic", "enp0s3"]


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
            net_interface['motivo'] = f"La interfaz de red '{net_int}' esta en modo promiscuo"
            enviar_mail.enviar_mail_asunto_body(
                tipo_alerta='ALERTA!',
                cuerpo=f"Se encontro que la interfaz de red {net_interface['int_name']} esta en modo promiscuo",
                asunto=f'INTERFACES DE RED'
            )
            escribir_log.escribir_log(alarmas_o_prevencion='alarmas',tipo_alarma='INT_PROMISCUA', ip_o_email=net_int, motivo='Se encontro que la interfaz de red mencionada, esta en modo promiscuo')
        else:
            net_interface["is_mode_promiscuo"] = "NO"
            net_interface['motivo'] = f""

        promis_nets_active.append(net_interface)

    crear_csv.write_csv(
        headers_list=["Nombre Interfaz", "Modo promiscuo", "motivo"],
        carpeta='sniffers',
        nombre_archivo='check_net_interfaces',
        lista= promis_nets_active,
        mensaje='Se le envio un mail al administrador si es que hubo interfaces de red en modo promiscuo'
    )

    
    
import sys
sys.path.append('./herramientas/')
import crear_csv, enviar_mail, escribir_log

check_net_interfaces()