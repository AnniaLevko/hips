import os
import sys
sys.path.append('./herramientas/')
import crear_csv, enviar_mail, bloquear_email, escribir_log


# Buscamos el authid en los logs de /var/log/maillog
# Verificamos si un mail envio cantidad masivas de mails.
def verificar_ataques_smtp_maillog():
    command_to_execute = "sudo cat /var/log/maillog | grep -i 'authid' "
    message_file_alerts = os.popen(command_to_execute).read().split("\n")
    message_file_alerts.pop(-1)

    email_contador, lista_para_csv = {}, []
    cuerpo_mail = asunto_mail = ''
    for elemnto_linea in message_file_alerts: # Reccorremos las lineas de las alertas
        authid = [word for word in elemnto_linea.split() if 'authid=' in word][0] # Procedemos a guardar el authid de la linea
        email = authid.split("=")[-1][:-1] # Sacamos el 'authid=' y la ',' al final. Finalmente obtenemos el email.

        if email in email_contador:
            email_contador[email] = email_contador[email] + 1 # Incrementamos el contador de cuantos email lleva este email
            if email_contador[email] == 50:  # Si el email envio mas de 50 mails, lo consideramos masivos
                csv_diccionario = {
                    'usuario': email,
                    'motivo': 'Muchos mails de smtp de este mismo correo se encontro en el archivo /var/log/maillog'
                }
                lista_para_csv.append(csv_diccionario)
                escribir_log.escribir_log(alarmas_o_prevencion='prevencion', tipo_alarma='Email Bomb', ip_o_email=email, motivo='Se registraron muchos mails por parte de este email, se paso a bloquear el email.')
                bloquear_email.bloquear_email(email) # Bloqueamos el email
                cuerpo_mail = cuerpo_mail + '\n' + f"Muchos mails por parte del email: '{email}', se procedio a bloquear el email.\n"
        else:
            email_contador[email] = 1
        
    #Procedemos a crear el csv para mostrar en la pagina web
    headers = ["Email involucrado", "motivo"]
    mensaje_final ='No se encontro ningun comportamiento raro de emails de smtp en /var/log/maillog'

    # Si se encuentra comportamiento extranho, escribimos el mensaje del csv y enviamos una alerta(mail) al admin
    if lista_para_csv:
        asunto_mail = 'MASIVOS EMAILS de SMTP en /var/log/maillog!'
        mensaje_final = "Se cambio la contrasenha de estos usuarios y se envio al mail del administrador las nuevas contrasenhas."
        enviar_mail.enviar_mail_asunto_body(tipo_alerta='PREVENCION!', asunto= asunto_mail, cuerpo=cuerpo_mail) # Envia el mail al administrador
    
    # Creamos el csv para mostrar en la web despues.
    crear_csv.write_csv(carpeta="verificar_logs", nombre_archivo="ataque_smtp_maillog", lista=lista_para_csv, mensaje=mensaje_final, headers_list=headers)

verificar_ataques_smtp_maillog()
