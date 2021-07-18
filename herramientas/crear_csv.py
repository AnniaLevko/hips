

def write_csv(carpeta, nombre_archivo, headers_list ,lista, mensaje):
    f = open(f"./resultados/{carpeta}/{nombre_archivo}.csv", "w")
    for index, header in enumerate(headers_list):
        if index ==0:
            f.write(f"{header},")
        else:
            f.write(f",{header}")
    f.write("\n")

    for diccionario in lista:
        f.write("\n")
        for index, x in enumerate(diccionario):
            if index == 0: 
                f.write(f"{diccionario[x]},")
            else:
                f.write(f",{diccionario[x]}")
        
    f.write(f"\n\n{mensaje}")
    f.close()

def append_csv(carpeta, nombre_archivo, headers_list ,lista, mensaje):
    f = open(f"./resultados/{carpeta}/{nombre_archivo}.csv", "a")
    for index, header in enumerate(headers_list):
        if index ==0:s
            f.write(f"{header},")
        else:
            f.write(f",{header}")
    f.write("\n")

    for diccionario in lista:
        f.write("\n")
        for index, x in enumerate(diccionario):
            if index == 0: 
                f.write(f"{diccionario[x]},")
            else:
                f.write(f",{diccionario[x]}")
        
    f.write(f"\n\n{mensaje}")
    f.close()




# para probar nada mas
# objeto1 = {
#             'PID': 21608,
#             '%MEM': 7.8,
#             '%CPU': 32.6, 
#             'EXECUTION_TIME': 294.87, 
#             'motivo': 'usa mucha memoria'
#         }
# objeto2 =  {
#             'PID': 23644,
#             '%MEM': 5.9,
#             '%CPU': 5.2,
#             'EXECUTION_TIME': 291.73, 
#             'motivo': 'usa mucha memoria'
#         }
# lista = [ objeto1, objeto2]
        
# headers = ["PID a matar", "%MEM", "%CPU", "Tiempo de ejecucion", "motivo del kill"]
# carpeta = "verificar_procesos"
# nombre_csv = "prueba"
# mensaje = "se mataron los procesos.."

# write_csv(carpeta, nombre_csv, headers, lista, mensaje)