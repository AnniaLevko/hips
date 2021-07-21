import os
import sys
sys.path.append('./herramientas/')
import crear_csv, enviar_mail, bloquear_ip, escribir_log

def ataque_ddos_dns():
    dns_file_log = os.popen("sudo cat /descargas/tcpdump_dns").read().split('\n')
    dns_file_log.pop(-1)

    ip_contador, lista_para_csv = {}, []
    cuerpo_mail = asunto_mail = ''

    for elemento_linea in dns_file_log:
        ip_atacante = elemento_linea.split()[2]
        ip_destino = elemento_linea.split()[4][:-1] # [:-1] para borrar el : final

        if (ip_atacante, ip_destino) in ip_contador:
            ip_contador[(ip_atacante, ip_destino)] = ip_contador[(ip_atacante, ip_destino)] + 1

            # Si hubieron al menos 10 ip atacante a un mismo ip destino, entonces es alarmante y tomamos una accion
            if ip_contador[(ip_atacante, ip_destino)] == 10:
                csv_diccionario = {
                    'IP ATACANTE': ip_atacante,
                    'IP DESTINO': ip_destino,
                    'motivo': 'Se registraron muchos paquetes desde el IP atacante al IP destino'
                }
                lista_para_csv.append(csv_diccionario)

                # Le damos formato para que acepte iptables
                ip_atacante_iptables = ip_atacante.split('.')[:-1]
                ip_atacante_iptables = f"{ip_atacante_iptables[0]}.{ip_atacante_iptables[1]}.{ip_atacante_iptables[2]}.{ip_atacante_iptables[3]}"
                
                bloquear_ip.bloquear_ip(ip_atacante_iptables) # Bloqueamos la IP atacante
                escribir_log.escribir_log(alarmas_o_prevencion='prevencion', tipo_alarma='Ataque DDOS', ip_o_email=ip_atacante, motivo='Se registraron muchos paquetes desde este IP a un mismo IP destino')
                cuerpo_mail = cuerpo_mail + '\n' + f"Muchos Paquetes enviados desde la IP: '{ip_atacante}' al IP: '{ip_destino}', se procedio a bloquear la IP.\n"

        else:
            ip_contador[(ip_atacante, ip_destino)] = 1

    #Procedemos a crear el csv para mostrar en la pagina web
    headers = ["IP ATACANTE", "IP DESTINO", "motivo"]
    mensaje_final ='No se encontro ningun comportamiento en los registros de DNS'

    # Si se encuentra comportamiento extranho, escribimos el mensaje del csv y enviamos una alerta(mail) al admin
    if lista_para_csv:
        asunto_mail = 'SE ENCONTRO ATAQUE DDOS!'
        mensaje_final = "Se bloqueo los IP's atacantes y se envio al mail del administrador la prevencion."
        enviar_mail.enviar_mail_asunto_body(tipo_alerta='PREVENCION!', asunto= asunto_mail, cuerpo=cuerpo_mail) # Envia el mail al administrador
    
    # Creamos el csv para mostrar en la web despues.
    crear_csv.write_csv(carpeta="verificar_logs", nombre_archivo="ataque_ddos_dns", lista=lista_para_csv, mensaje=mensaje_final, headers_list=headers)

ataque_ddos_dns()