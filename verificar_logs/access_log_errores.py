import os
import sys
sys.path.append('./herramientas/')
import crear_csv, enviar_mail, bloquear_ip, escribir_log

def verificar_access_log():
    command_to_execute = "sudo cat /var/log/httpd/access.log | grep -i 'HTTP' | grep -i '404'"
    access_file_errores = os.popen(command_to_execute).read().split('\n')
    access_file_errores.pop(-1)

    ip_contador, lista_para_csv = {}, []
    cuerpo_mail = asunto_mail = ''

    for elemento_linea in access_file_errores:
        ip =  elemento_linea.split()[0]
        
        if ip in ip_contador:
            ip_contador[ip] = ip_contador[ip] + 1
            if ip_contador[ip] == 20:
                csv_diccionario = {
                    'IP': ip,
                    'motivo': 'Muchas errores de carga de paginas desde un mismo IP'
                }
                lista_para_csv.append(csv_diccionario)
                escribir_log.escribir_log(alarmas_o_prevencion='prevencion', tipo_alarma='MASIVOS 404', ip_o_email=ip, motivo='Se registraron muchas respuestas 404 desde la misma IP, se bloqueo el IP')
                bloquear_ip.bloquear_ip(ip) # bloqueamos la ip 
                cuerpo_mail = cuerpo_mail + '\n' + f"Muchos errores de carga de paginas por parte del IP: '{ip}', se procedio a bloquear el IP.\n"
        else:
            ip_contador[ip] = 1

    #Procedemos a crear el csv para mostrar en la pagina web
    headers = ["IP involucrado", "motivo"]
    mensaje_final ='No se encontro ningun comportamiento raro de respuestas http en /var/log/httpd/access.log'

    # Si se encuentra comportamiento extranho, escribimos el mensaje del csv y enviamos una alerta(mail) al admin
    if lista_para_csv:
        asunto_mail = 'MASIVOS ERRORES RESPUESTAS HTTP en /var/log/httpd/access.log!'
        mensaje_final = "Se bloque los IP's y se envio al mail del administrador la alerta."
        enviar_mail.enviar_mail_asunto_body(tipo_alerta='PREVENCION!', asunto= asunto_mail, cuerpo=cuerpo_mail) # Envia el mail al administrador
    
    # Creamos el csv para mostrar en la web despues.
    crear_csv.write_csv(carpeta="verificar_logs", nombre_archivo="access_log_errores", lista=lista_para_csv, mensaje=mensaje_final, headers_list=headers)

verificar_access_log()