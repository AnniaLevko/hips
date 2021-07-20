import os

# Agrega a la lista negra de emails recipientes
def bloquear_email(email):
    try:
        comando_para_agregar_en_lista_negra = f"sudo echo '{email} REJECT' >> /etc/postfix/sender_access"
        os.system(comando_para_agregar_en_lista_negra) # Agregamos el email a la lista negra
        
        os.system("sudo postmap hash:/etc/postfix/sender_access") # creamos la base de datos con el comando postmap
    except Exception:
        print("hubo un problema en cargar un email en la lista negra")
