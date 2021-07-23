import os
import sys
sys.path.append('./herramientas/')
import crear_csv, enviar_mail, escribir_log


# Verificamos en todos los usuarios si tienen tareas ejecutandose como cron
def verificar_cronjobs():
    usuarios_infos = os.popen("sudo cat /etc/passwd").read().split('\n') #obtenemos lista de usuario:x:0:0:grupo: etc
    usuarios_infos.pop(-1)

    lista_para_csv = []
    cuerpo_mail = ''
    
    # Recorremos cada informacion de un usuario
    for usuario_info in usuarios_infos:
        usuario = usuario_info.split(':')[0] # Obtenemos el usuario
        
        tareas_cron = [] 
        # Verificamos si el usuario tiene tareas en cron
        try:
            tareas_cron = os.popen(f"sudo crontab -l -u {usuario}").read().split('\n')
            tareas_cron.pop(-1)
        except Exception:
            pass
        
        # Si el usuario tiene tareas_cron entonces recorremos cada tarea
        if tareas_cron:
            for tarea_cron in tareas_cron:
                file_script =  tarea_cron.split()[-1] # Obtenemos solo el archivo que se esta ejecutando como cron
                tarea_obj = {
                    'Usuario': usuario,
                    'archivo': file_script
                }
                lista_para_csv.append(tarea_obj)
                escribir_log.escribir_log(alarmas_o_prevencion='alarmas', tipo_alarma='CRONJOB', ip_o_email=file_script, motivo=f'Se encontro que el usuario {usuario} ejecuta el archivo como cron')
                cuerpo_mail = cuerpo_mail + f"\n Se encontro que el usuario {usuario} esta ejecutando el archivo {file_script} como cron."

    mensaje_final = "No se encontro niguna tarea como cron."
    if lista_para_csv:
        mensaje_final = "Se notifico al administrador por email sobre los archivos ejecutandose como cron."
        enviar_mail.enviar_mail_asunto_body(
            asunto='CRONJOBS',
            tipo_alerta='ALERTA!',
            cuerpo = cuerpo_mail
        )
    
    crear_csv.write_csv(
        carpeta='verificar_procesos',
        nombre_archivo='cronjob',
        headers_list=["Usuario Involucrado", "Archivo como cron"],
        lista=lista_para_csv,
        mensaje=mensaje_final
    )

 
verificar_cronjobs()