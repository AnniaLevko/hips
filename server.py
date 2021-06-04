from flask import Flask
from flask import render_template
import subprocess
import os
import time
import csv
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/<program_name>')
def dar_resultado(program_name):
    titulo = str(program_name).replace("_", " ").capitalize() # Convertimos a string el nombre del programa, remplazamos el _ por <espacio> y ponemos mayuscula la primera letra

    subprocess.run(["python3", f"{program_name}.py"]) # Corremos el programita en el cual guarda en un <program_name>.txt y .csv su resultado

    #Abrimos el archivo para leer que tiene el nombre del programa que se ejecuta anteriormente ej: <program_name>.txt
    with open(f"./resultados/{program_name}.txt", "r") as file:
        resultado = file.readlines() # Guardamos cada linea del txt en en una lista

    with open(f"./resultados/{program_name}.csv", newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter = ',')
        
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows)
        
    # Renderizamos el template verResultado.html con el texto (resultado de la funcion) y su titulo (nombre del programa que se ejecuto)
    return render_template("verResultado.html", texto = list_of_rows, titulo = titulo)




## RUTAS DE PRUEBA

@app.route('/prueba')
def prueba():
    return render_template("prueba.html")

@app.route('/prueba2')
def prueba2():
    return render_template("prueba2.html")



# Encendemos el modo debug para no tener que apagar el server a cada rato
app.run(debug=True)