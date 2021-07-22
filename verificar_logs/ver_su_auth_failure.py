import os
import string
import random
import datetime as dt
import sys
sys.path.append('./herramientas/')
import crear_csv, enviar_mail, escribir_log

def generar_contrasenha_nueva():
    contrasenha_caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasenha = random.sample(contrasenha_caracteres, 8)
    contrasenha = "".join(contrasenha)
    return contrasenha


def ver_su_auth_failure():
    command_to_execute = "sudo cat /var/log/secure | grep -i 'su:auth' | grep -i 'authentication failure'"
    message_file_alerts = os.popen(command_to_execute).read().split("\n")
    message_file_alerts.pop(-1)

    usuarios_contador = {}
    lista_para_csv = []
    cuerpo_mail = ''
    asunto_mail = ''

    # Recorremos cada linea de alerta
    for elementos_linea in message_file_alerts:
        ruser = [word for word in elementos_linea.split() if 'ruser=' in word][0] # Obtenemos el string '[user=condorito]'
        ruser = ruser.split('=')[-1]
        
        # Si ya esta incializado un contador para el usuario en ruser, entonces procedemos, sino, inicializamos
        if ruser in usuarios_contador:
            usuarios_contador[ruser] = usuarios_contador[ruser] + 1 # si existe le sumamos uno al contador de failure en ese usuario
            # Si el contador de failure del usuario supera un limite, es una alarma, procedemos a cambiar la contrasenha
            if usuarios_contador[ruser] == 15:
                #Cambiamos contrasenha
                contrasenha_a_cambiar = generar_contrasenha_nueva()
                
                comando_actualizar_contrasenha = f"sudo echo '{ruser}:{contrasenha_a_cambiar}' | chpasswd"
                os.system(comando_actualizar_contrasenha)

                csv_diccionario = {
                    'usuario': ruser,
                    'motivo': 'Muchas entradas de auth failure por su:auth en /var/log/secure'
                }
                lista_para_csv.append(csv_diccionario)
                escribir_log.escribir_log(alarmas_o_prevencion='prevencion', tipo_alarma='su:auth_ATTACK', ip_o_email=ruser, motivo='Muchas entradas de auth failure por su:auth por el ruser, se cambio la contrasenha')

                cuerpo_mail = cuerpo_mail + '\n' + f"Muchas entradas de auth failure por su:auth por el ruser: {ruser}, se cambio su contrasenha a --> '{contrasenha_a_cambiar}'\n"
        else:
            usuarios_contador[ruser] = 1
        
    #Procedemos a crear el csv para mostrar en la pagina web
    headers = ["Usuario involucrado", "motivo"]
    mensaje ='No se encontro ningun comportamiento extranho en auth de su:auth en /var/log/secure'

    # Si se encuentra comportamiento extranho, escribimos el mensaje del csv y enviamos una alerta(mail) al admin
    if lista_para_csv:
        asunto_mail = 'MASIVOS su:auth failures'
        mensaje = "Se cambio la contrasenha de estos usuarios y se envio al mail del administrador las nuevas contrasenhas."
        enviar_mail.enviar_mail_asunto_body(tipo_alerta='PREVENCION!', asunto= asunto_mail, cuerpo=cuerpo_mail) # Envia el mail al administrador

    # Creamos el csv para mostrar en la web despues.
    crear_csv.write_csv(carpeta="verificar_logs", nombre_archivo="ver_su_auth_failure", lista=lista_para_csv, mensaje=mensaje, headers_list=headers)


ver_su_auth_failure()