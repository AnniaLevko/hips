#!/usr/bin/python
import psycopg2

# Connect to your postgres DB
conn = psycopg2.connect(user = 'postgres', password='erikannia7', dbname='hips2021')

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

    


crear_tablas()


