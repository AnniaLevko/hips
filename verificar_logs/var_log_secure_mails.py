import os
import string
import random
import sys
sys.path.append('./herramientas/')
import crear_csv

def generar_contrasenha_nueva():
    contrasenha_caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasenha = random.sample(contrasenha_caracteres, 8)
    contrasenha = "".join(contrasenha)
    return contrasenha

def verificar_log_secure_mail():
    command_to_execute = "sudo cat /var/log/secure |grep -i 'smtp:auth' | grep -i 'authentication failure'"
    secure_file_content = os.popen(command_to_execute).read().split("\n")
    secure_file_content.pop(-1)

    usuarios_contador = {}
    lista_para_csv = []
    

    for linea in secure_file_content:
        linea = linea.split() # Separamos la linea en espacios
        usuario = linea[-1]# Obtenemos el nombre de usuario involucrado en el auth failure en formato user=<nombre_usuario>
        usuario = usuario.split('=')[-1] # Obtenemos solo el nombre de usuario

        # Verificamos que el usuario ya existe en nuestro diccionario
        if usuario in usuarios_contador:
            usuarios_contador[usuario] = usuarios_contador[usuario] + 1 # si existe le sumamos uno al contador de failure en ese usuario

            # Si el contador de failure del usuario supera un limite, es una alarma, procedemos a cambiar la contrasenha
            if usuarios_contador[usuario] == 50:
                #Cambiamos contrasenha
                contrasenha_a_cambiar = generar_contrasenha_nueva()
                print("contrasenha:",contrasenha_a_cambiar)
                comando_actualizar_contrasenha = f"sudo echo '{usuario}:{contrasenha_a_cambiar}' | chpasswd"
                os.system(comando_actualizar_contrasenha)
                print("contrasenha cambiada para el usuario:", usuario)

                csv_diccionario = {
                    'usuario': usuario,
                    'motivo': 'Muchas entradas de auth failure de stmp en el archivo /var/log/secure'
                }
                lista_para_csv.append(csv_diccionario)

        else:
            usuarios_contador[usuario] = 1 # Si no existe, agregamos al usuario en el diccionario e inicializamos su contador en 1
        
    headers = ["Usuario involucrado", "motivo"]
    mensaje ='No se encontro ningun comportamiento extranho en auth de smtp'
    if lista_para_csv:
        mensaje = "Se cambio la contrasenha de estos usuarios y se envio al mail del administrador la nueva contrasenha."

    crear_csv.write_csv(carpeta="verificar_logs", nombre_archivo="var_log_secure_mails", lista=lista_para_csv, mensaje=mensaje, headers_list=headers)
        
        



# generar_contrasenha_nueva()
verificar_log_secure_mail()

