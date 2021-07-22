#!/usr/bin/python
import os

from dotenv import load_dotenv
import psycopg2

load_dotenv()
BD_PASSWORD = os.getenv('BD_PASSWORD')
BD_USER = os.getenv('BD_USER')
# Connect to your postgres DB
conn = psycopg2.connect(user = BD_USER, password=BD_PASSWORD, dbname='hips2021')

# Open a cursor to perform database operations
cur = conn.cursor()

def crear_tablas():

    command_tabla_md5sum = (
        
        "CREATE TABLE IF NOT EXISTS file ("
        "   file_id serial,"
        "   file_name character varying(64), "
        "   md5sum character varying(64)"
        ");"
    )
    cur.execute(command_tabla_md5sum)
    conn.commit()

    command_tabla_user = (
        
        "CREATE TABLE IF NOT EXISTS users ("
        "   id serial primary key,"
        "   username character varying(24) UNIQUE,"
        "   password character varying(100)"
        ");"
    )
    cur.execute(command_tabla_user)
    conn.commit()

    


crear_tablas()


