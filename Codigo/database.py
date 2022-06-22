import sqlite3
import os
import shutil

def create_database():
    if os.path.exists('rotondas.db'):
        connection = sqlite3.connect('rotondas.db')
        cursor = connection.cursor()
        cursor.execute('DROP TABLE Acciones;')
        cursor.execute('DROP TABLE Rotondas;')
        connection.commit()
        cursor.close()
        connection.close()
    connection = sqlite3.connect('rotondas.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Rotondas
                (fecha Date NOT NULL,
                PRIMARY KEY (Fecha))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Acciones
                (fecha Date,  orden INT, verbalizada TEXT, percepcion TEXT, accion TEXT, distancia_ceda_m INT, vel_actual FLOAT, limite_api INT, limite_visto INT,
                pos TEXT, distancia_coche INT, distancia_ceda INT, tr_zi INT, tr_zc INT, tr_zd INT, coche_izq INT, coche_der INT,
                FOREIGN KEY (fecha) REFERENCES Rotondas(fecha),
                Constraint PK_Acciones Primary Key (fecha, orden))''')
    cursor.close()

def final_query (path):
    # last read byte is our truncation point, move back to it.
    f = open(path , 'rb+')
    f.seek(-1, os.SEEK_END)
    f.truncate()  
    f.close()
    f = open(path , 'a')
    f.write(';')
    f.close()

def execute_query(path):
    with open(path) as f:
        info = f.read()
        f.close()
    connection = sqlite3.connect('rotondas.db' ,timeout = 100)
    cursor = connection.cursor()
    cursor.execute(info)
    connection.commit()
    cursor.close()

def make_queries(rotondas):
    #If the update folder exists, erase all the data from it
    if os.path.exists('QUERIES/'):
        shutil.rmtree('QUERIES/')
    os.mkdir('QUERIES/')

    insert_rotonda = 'INSERT INTO Rotondas (fecha) VALUES'
    f = open('QUERIES/rotondas.sql' , 'a')
    f.write(insert_rotonda)
    f.close()

    insert_action = 'INSERT INTO Acciones (fecha, orden, verbalizada, percepcion, accion, distancia_ceda_m, vel_actual, limite_api,pos, distancia_coche, tr_zi, tr_zc, tr_zd, coche_izq, coche_der) VALUES'
    f = open('QUERIES/acciones.sql' , 'a')
    f.write(insert_action)
    f.close()
    for rotonda in rotondas:
        rot = '\n(\'' + str(rotonda.fecha) + '\'),'
        f = open('QUERIES/rotondas.sql' , 'a')
        f.write(rot)
        f.close()
        actions = rotonda.actions
        orden = 0
        for action in actions:
            fecha ='\n(\'' + str(rotonda.fecha) + '\', '
            ord  = str(orden) + ','
            verbalizada = '\'' + str(action.verbalizada) + '\', '
            percepcion = '\'' + str(action.percepcion) + '\', '
            accion = '\'' + str(action.accion) + '\', '
            distancia_ceda_m = str(action.distancia_ceda_m) + ', '
            vel_actual = str(action.vel_actual) + ', '
            limite_api = str(action.limite_api) + ', '
            pos =  '\'' + str(action.pos) + '\', '
            distancia_coche = str(action.distancia_coche) + ', '
            tr_zi = str(action.tr_zi) + ', '
            tr_zc = str(action.tr_zc) + ','
            tr_zd = str(action.tr_zd) + ','
            coche_izq = str(action.coche_izq) + ','
            coche_der = str(action.coche_der) + '),'
            
            act = fecha + ord +  verbalizada +percepcion + accion + distancia_ceda_m + vel_actual +limite_api + pos + distancia_coche + tr_zi + tr_zc + tr_zd + coche_izq + coche_der
            act = act.replace('None', 'null')
            act = act.replace(',  ,', ', null,')
            f = open('QUERIES/acciones.sql' , 'a')
            f.write(act)
            f.close()
            orden  = orden +  1
    final_query('QUERIES/rotondas.sql')
    final_query('QUERIES/acciones.sql')

    execute_query('QUERIES/rotondas.sql')
    execute_query('QUERIES/acciones.sql')