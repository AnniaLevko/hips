import os
import datetime


# Escribe un registro de una alerta o prevencion
# en /var/log/hips/alarmas.log o /var/log/hips/prevencion.log
# donde el parametro alarma_o_prevencion debe contener el string 'alarmas' o 'prevencion'
# se escribe en el formato fecha_hora :: tipo_alarma :: ip_email   motivo

def escribir_log(alarmas_o_prevencion, tipo_alarma, motivo, ip_o_email = ''):
    fecha_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    lo_escrito = f'{fecha_hora} :: {tipo_alarma} :: {ip_o_email} \t{motivo}'

    if alarmas_o_prevencion == 'alarmas' or alarmas_o_prevencion == 'prevencion':
        os.system(f"sudo echo '{lo_escrito}' >> /var/log/hips/{alarmas_o_prevencion}.log")
    else:
        print("alarmas_o_prevencion tiene que tener el valor de 'alarmas' o 'prevencion' ")

# escribir_log(alarmas_o_prevencion='alarmas', tipo_alarma='SMTP ATTACK', ip_o_email='erikwasmosy98@gmail.com', motivo='se registro muchos mails de parte del email')