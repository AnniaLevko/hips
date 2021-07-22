import os
import sys
sys.path.append('./herramientas/')
import crear_csv, enviar_mail, bloquear_ip, escribir_log


def verificar_sshd_logs():
    ssh_file_err = os.popen("sudo cat /var/log/secure | grep -i 'sshd' | grep -i 'Failed password'").read().split('\n')
    ssh_file_err.pop(-1)
   
    ip_contador, lista_para_csv = {}, []
    cuerpo_mail = asunto_mail = ''

    for element_line in ssh_file_err:
        ip_origen = element_line.split()[-4]
        # ip_origen = [word for word in element_line.split() if 'rhost=' in word][0].split('=')[-1] # conseguimos solo el ip de origen
        
        if ip_origen in ip_contador:
            ip_contador[ip_origen] = ip_contador[ip_origen] + 1
            if ip_contador[ip_origen] == 5:
                csv_diccionario = {
                    'IP': ip_origen,
                    'motivo': 'Muchos intentos de accesso no valido por esta IP'
                }
                lista_para_csv.append(csv_diccionario)
                escribir_log.escribir_log(alarmas_o_prevencion='prevencion', tipo_alarma='MASIVO_SSH_FAIL', ip_o_email=ip_origen, motivo='Mucho intentos de accessos no validos, Se bloqueo la IP')
                bloquear_ip.bloquear_ip(ip_origen) # bloqueamos la ip 
                cuerpo_mail = cuerpo_mail + '\n' + f"Muchos auth failure por ssh por la IP: '{ip_origen}', se procedio a bloquear el IP.\n"
        else:
            ip_contador[ip_origen] = 1

    #Procedemos a crear el csv para mostrar en la pagina web
    headers = ["IP involucrado", "motivo"]
    mensaje_final ='No se encontro ningun comportamiento raro de intentos de sesion mediante ssh /var/log/secure'

    # Si se encuentra comportamiento extranho, escribimos el mensaje del csv y enviamos una alerta(mail) al admin
    if lista_para_csv:
        asunto_mail = 'MASIVOS AUTH FAIL SSH!'
        mensaje_final = "Se bloqueo las IP's y se envio al mail del administrador la alerta."
        enviar_mail.enviar_mail_asunto_body(tipo_alerta='PREVENCION!', asunto= asunto_mail, cuerpo=cuerpo_mail) # Envia el mail al administrador
    
    # Creamos el csv para mostrar en la web despues.
    crear_csv.write_csv(carpeta="verificar_logs", nombre_archivo="ver_sshd_logs", lista=lista_para_csv, mensaje=mensaje_final, headers_list=headers)

verificar_sshd_logs()