from flask import Flask
from flask import render_template
import subprocess
import os
import time

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/<program_name>')
def dar_resultado(program_name):
    resultado = []
    titulo = str(program_name).replace("_", " ").capitalize() # Convertimos a string el nombre del programa, remplazamos el _ por <espacio> y ponemos mayuscula la primera letra

    subprocess.run(["python3", f"{program_name}.py"]) # Corremos el programita en el cual guarda en un <program_name>.txt su resultado

    #Abrimos el archivo para leer que tiene el nombre del programa que se ejecuta anteriormente ej: <program_name>.txt
    with open(f"./resultados/{program_name}.txt", "r") as file:
        resultado = file.readlines() # Guardamos cada linea del txt en en una lista

    # Renderizamos el template verResultado.html con el texto (resultado de la funcion) y su titulo (nombre del programa que se ejecuto)
    return render_template("verResultado.html", texto = resultado, titulo = titulo)




app.run(debug=True)