import os
from principal import cur, conn
import sys
sys.path.append('./herramientas/')
import crear_csv, enviar_mail, bloquear_ip, escribir_log



passwd_dir = "/etc/passwd"
shadow_dir = "/etc/shadow"
directorios = [passwd_dir, shadow_dir]
def comparar_md5sum(dirs):
    lista_csv=[]
    hubo_modificacion = False
    files = [] # guardamos en una lista de diccionarios los md5sum actuales del sistema
    cuerpo_mail= ''
    # Obtenemos los md5sum actuales del sistema y guardamos en una lista
    for dir in dirs:
        command = f"md5sum {dir}" #+ " | awk '{print $1}'"
        file_with_md5sum = os.popen(command).read().split() # Guardamos en una lista el nombre del archivo y su md5sum
        
        if file_with_md5sum:
            file = {
                "file_name" : file_with_md5sum[1],
                "md5sum" : file_with_md5sum[0]
            }
            files.append(file)
    # print(files) 

    # Comparamos los md5sum actuales con los md5sum de la base de datos.
    for file in files:
        
        # Buscamos en la base de datos el md5sum guardado
        cur.execute(f"SELECT * FROM file WHERE file_name='{file['file_name']}'")
        query = cur.fetchall() # Guardamos en query lo que retorno el comando de BD
        print(query)

        # comparacion si los md5sum siguen iguales o no
        if file['md5sum'] == query[0][2]: # query[0][2] el [0] porque query es una lista de un elemento, y el [2] porque es una tupla de 3 elementos y en la posicion 2 esta el md5sum que se guardo en la BD
            print("No hubo modificacion en", file['file_name'])
            file['se modifico'] = 'NO'
        else:
            hubo_modificacion = True
            file['se modifico'] = 'SI'
            print("Hubo modificacion! en", file['file_name'])
            md5sum_tmp = file['md5sum']
            file_name_tmp = file['file_name']
            cur.execute(f"UPDATE file SET md5sum = '{md5sum_tmp}' WHERE file_name = '{file_name_tmp}'; ")
            conn.commit()
            escribir_log.escribir_log(alarmas_o_prevencion='alarmas', tipo_alarma='md5sum_distinto',ip_o_email=file['file_name'], motivo='Se encontro que el archivo mencionado tuvo modificaciones')
            cuerpo_mail = cuerpo_mail + f"\nEl archivo {file['file_name']} tuvo modificaciones, se paso a actualizar el md5sum en la base de datos.\n"
        lista_csv.append(file)

    
    if hubo_modificacion:
        enviar_mail.enviar_mail_asunto_body(tipo_alerta='ALERTA!', asunto='CAMBIOS MD5SUM', cuerpo=cuerpo_mail)

    crear_csv.write_csv(
        carpeta='base_de_datos', 
        nombre_archivo='verificar_archivos_binarios', 
        headers_list=['Nombre de Archivo', 'md5sum', 'se modifico?'], 
        lista=lista_csv,
        mensaje='Si el md5sum se modifico se alerto al administrador por mail y tambien se escribio un registro en alarmas.log'
    )
comparar_md5sum(directorios)   
