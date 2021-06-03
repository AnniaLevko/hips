from flask import Flask
from flask import render_template
import subprocess
import os
import time

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/ver-usuarios')
def ver_usuarios():
    os.system('python3 ./usuarios_conectados.py > ./resultados/usuarios_conectados.txt')
    texto = ''

    with open("./resultados/usuarios_conectados.txt", "r") as f:
        texto = f.readline()
        texto = f.read()

    with open("./resultados/usuarios_conectados.txt", "w") as f:
        f.write(texto)
    
    return render_template("verResultado.html", texto = texto)




app.run(debug=True)