import os



def get_queue_size():
    command = "mailq"
    resultado = os.popen(command).read()
    if "queue is empty" in resultado:
        print("La cola de mail esta vacia")
        # resultado = []
    else:
        resultado = resultado.splitlines()

    mail_queue = resultado.splitlines()
    
    print(mail_queue)
    if len(mail_queue) > 100:
        print("Muchos mails")


get_queue_size()