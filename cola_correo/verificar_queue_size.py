import os

import sys
sys.path.append('./herramientas/')
import crear_csv, enviar_mail, escribir_log

def get_queue_size():
    command = "mailq"
    resultado = os.popen(command).read()
    
    mensaje_final = ''


    if "queue is empty" in resultado:
        print("La cola de mail esta vacia")
        mensaje_final = 'La cola esta vacia'
    else:
        resultado = resultado.splitlines()

    mail_queue = resultado.splitlines()
    
    print(mail_queue)
    if len(mail_queue) > 100:
        escribir_log.escribir_log(alarmas_o_prevencion='alarmas', tipo_alarma='COLA_MAIL', motivo='Se detecto muchos mails en la cola')
        enviar_mail.enviar_mail_asunto_body(tipo_alerta='ALERTA!', asunto='MAIL QUEUE', cuerpo=f'se encontraron {len(mail_queue)} mails en la cola')

    if len(mail_queue) > 0 and len(mail_queue) <= 100:
        mensaje_final = 'no se encontraron muchos mails en la cola'
    else:
        mensaje_final = 'Se encontraron muchos mails en la cola, se escribio un registro en alarmas.log y se aviso al administrador'
    
    crear_csv.write_csv(carpeta='cola_correo', nombre_archivo='verificar_queue_size', headers_list=["Mensaje final"], lista={}, mensaje= mensaje_final)

    
get_queue_size()