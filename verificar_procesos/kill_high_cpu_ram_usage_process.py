import os
import sys
sys.path.append('./herramientas/')
import crear_csv 



def get_proceso_por_mem_o_cpu(mem_o_cpu=""):
    if mem_o_cpu == "mem" or mem_o_cpu == "cpu":
        PROCESOS_CON_MAS_CPU_O_MEM_CMD = f"ps -eo pid,%mem,%cpu --sort=-%{mem_o_cpu} | head -n 20 " # Devuelve los 20 procesos que mas cpu o memoria esta en uso.
        procesos_mas_memoria = os.popen(PROCESOS_CON_MAS_CPU_O_MEM_CMD).read().split("\n")
        procesos_mas_memoria.pop(-1)
        procesos_mas_memoria.pop(0)
        for index, proceso in enumerate(procesos_mas_memoria):
            tmp = proceso.split()

            nuevo_objeto = {
                "PID": int(tmp[0]),
                "%MEM": float(tmp[1]),
                "%CPU": float(tmp[2])
            }
            
            ver_tiempo_ejecutando_cmd = f"ps -p {nuevo_objeto['PID']} -o etime" # Comando para tener el tiempo de ejecucion del proceso en HH:MM:SS
            
            # Obtenemos el tiempo de ejecucion del proceso
            tiempo_ejecutandose = os.popen(ver_tiempo_ejecutando_cmd).read().split("\n")[1].strip().split(":") # Damos formato al retorno

            if len(tiempo_ejecutandose) < 3: # si no tiene hora, solo minutos y segundos
                tiempo_ejecutandose = float(tiempo_ejecutandose[0]) + float(tiempo_ejecutandose[1])/60.0 
            else:
                tiempo_ejecutandose = float(tiempo_ejecutandose[0]) * 60 + float(tiempo_ejecutandose[1]) + float(tiempo_ejecutandose[2])/60.0 
            
            nuevo_objeto["EXECUTION_TIME"] = round(tiempo_ejecutandose,2 ) # agregamos al objeto el tiempo de ejecucion
            procesos_mas_memoria[index] = nuevo_objeto

        return procesos_mas_memoria
    else:
        print("ERROR: el argumento debe ser 'mem' para memoria o 'cpu' para uso del procesador.")
        mensaje = {
            "mensaje": "error"
        }
        return mensaje



def verificar_procesos_cpu_ram():
    procesos_mas_memoria = get_proceso_por_mem_o_cpu("mem")
    procesos_mas_cpu = get_proceso_por_mem_o_cpu("cpu")
    procesos_a_matar = []

    # Revisamos el uso de las memorias
    for proceso in procesos_mas_memoria:
        
        if proceso["%MEM"] > 4.1:
            print(f"el PID {proceso['PID']} esta consumiendo mucha memoria")

            if proceso["EXECUTION_TIME"] > 5.0:
                print(f"el PID {proceso['PID']} se esta ejecutandose por mucho tiempo")
                print("Se agregara a la lista para matar")
                proceso["motivo"] = "usa mucha memoria"
                procesos_a_matar.append(proceso)       
    # Revisamos el uso de los cpu
    for proceso in procesos_mas_cpu:
    
        if proceso["%CPU"] > 4.1:
            print(f"el PID {proceso['PID']} esta consumiendo mucha procesador")

            if proceso["EXECUTION_TIME"] > 5.0:
                print(f"el PID {proceso['PID']} se esta ejecutandose por mucho tiempo")
                print("Se agregara a la lista para matar")
                proceso["motivo"] = "usa mucha cpu"
                procesos_a_matar.append(proceso)

    #Escribimos el archivo csv
    mensaje = "Procesos matados..."
    headers = ["PID a matar","%MEM","%CPU","Tiempo de ejecucion","motivo"]
    carpeta = "verificar_procesos"
    nombre_csv = "kill_high_cpu_ram_usage_process"

    crear_csv.write_csv(mensaje= mensaje, headers_list=headers,lista=procesos_a_matar, carpeta=carpeta,nombre_archivo=nombre_csv)
    # f = open("./resultados/verificar_procesos/kill_high_cpu_ram_usage_process.csv", "w")

    # if len(procesos_a_matar) >= 1:
    #     f.write("PID a matar,%MEM,%CPU,Tiempo de ejecucion,motivo\n") # Escribimos los headers del csv
    #     for index, proceso in enumerate(procesos_a_matar):
    #         f.write(f"{proceso['PID']},{proceso['%MEM']}%,{proceso['%CPU']}%,{proceso['EXECUTION_TIME']}min, {proceso['motivo']}\n")
    #     f.write("\n\nProcesos matados...")
    # f.close()


        


    



verificar_procesos_cpu_ram()