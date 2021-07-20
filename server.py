from flask import Flask
from flask import render_template, redirect, url_for, send_from_directory
import subprocess
import os
import time
import csv
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

import sys
sys.path.append('./base_de_datos/')
from principal import cur



class LoginForm(FlaskForm):
    email = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label="Log In") 


app = Flask(__name__)
app.secret_key = "hamburgesa-y-comida-china"
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://root:erikannia7@localhost/hips2021"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(24), unique = True)
    password = db.Column(db.String(100))

# db.create_all()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    
@app.route("/", methods=['Get'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for("tools"))
    else:
        return redirect(url_for("login"))


@app.route('/tools')
@login_required
def tools():
    cur.execute("select * from users")
    print(cur.fetchall())
    return render_template('tools.html')


@app.route('/<folder>/<program_name>')
@login_required
def dar_resultado(folder, program_name):
    titulo = str(program_name).replace("_", " ").capitalize() # Convertimos a string el nombre del programa, remplazamos el _ por <espacio> y ponemos mayuscula la primera letra

    subprocess.run(["python3", f"./{folder}/{program_name}.py"]) # Corremos el programita en el cual guarda en un <program_name>.txt y .csv su resultado

    # Leemos el csv para obtener las lineas y enviar al html
    with open(f"./resultados/{folder}/{program_name}.csv", newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter = ',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        
        
    # Renderizamos el template verResultado.html con el texto (resultado de la funcion) y su titulo (nombre del programa que se ejecuto)
    return render_template("verResultado.html", texto = list_of_rows, titulo = titulo)


@app.route("/login", methods = ["GET", "POST"])
def login():
    login_form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for("tools"))

    if login_form.validate_on_submit():
        usernamexd = login_form.email.data
        password = login_form.password.data

        # Buscamos el usuario en la base de datos
        user_obj = User.query.filter_by(username=usernamexd).first()
        if user_obj is None:
            return render_template("denied.html", form=login_form)
        if check_password_hash(user_obj.password, password):
            print("coincidio")
            login_user(user_obj)
            return redirect(url_for("tools"))
        else:
            print("error")
            return render_template("denied.html", form=login_form)
        print(login_form.email.data)
    
    return render_template('login.html', form=login_form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))




## RUTAS DE PRUEBA

@app.route('/prueba')
def prueba():
    return render_template("prueba.html")

@app.route('/prueba2')
def prueba2():
    return render_template("prueba2.html")



# Encendemos el modo debug para no tener que apagar el server a cada rato
app.run(debug=True)