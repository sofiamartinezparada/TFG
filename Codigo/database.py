import sqlite3
import os
import shutil

basedir = os.path.dirname(__file__)



def create_database():
    if os.path.exists(os.path.join(basedir,'../maniobras.db')):
        connection = sqlite3.connect(os.path.join(basedir,'../maniobras.db'))
        cursor = connection.cursor()
        cursor.execute('DROP TABLE Acciones;')
        cursor.execute('DROP TABLE Maniobras;')
        connection.commit()
        cursor.close()
        connection.close()
    connection = sqlite3.connect(os.path.join(basedir,'../maniobras.db'))
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Maniobras
                (fecha Date NOT NULL,
				tipo int NOT NULL,
                id int NOT NULL,
				info int,
                PRIMARY KEY (Fecha, tipo, id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Acciones
                (fecha Date, maniobra_tipo INT,maniobra_id INT, orden INT, verbalizada TEXT, percepcion TEXT, accion TEXT, distancia_ceda_m INT, vel_actual FLOAT, limite_api INT, limite_visto INT,
                pos TEXT, distancia_coche INT, distancia_ceda INT, tr_zi INT, tr_zc INT, tr_zd INT, coche_izq INT, coche_der INT,
                FOREIGN KEY (maniobra_tipo, maniobra_id) REFERENCES Maniobras(tipo, id),
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
    connection = sqlite3.connect(os.path.join(basedir,'../maniobras.db') ,timeout = 100)
    cursor = connection.cursor()
    cursor.execute(info)
    connection.commit()
    cursor.close()

def make_queries(rotondas):
    #If the update folder exists, erase all the data from it
    if os.path.exists('QUERIES/'):
        shutil.rmtree('QUERIES/')
    os.mkdir('QUERIES/')

    insert_rotonda = 'INSERT INTO Maniobras (fecha, tipo, id, info) VALUES'
    f = open('QUERIES/maniobras.sql' , 'a')
    f.write(insert_rotonda)
    f.close()

    insert_action = 'INSERT INTO Acciones (fecha, maniobra_tipo, maniobra_id, orden, verbalizada, percepcion, accion, distancia_ceda_m, vel_actual, limite_api,pos, distancia_coche, tr_zi, tr_zc, tr_zd, coche_izq, coche_der) VALUES'
    f = open('QUERIES/acciones.sql' , 'a')
    f.write(insert_action)
    f.close()
    for rotonda in rotondas:
        rot_fecha = '\n(\'' + str(rotonda.fecha) + '\','
        rot_tipo = str(rotonda.tipo) + ','
        rot_id= str(rotonda.id) + ','
        rot_info = str(rotonda.info) + '),'
        rot = rot_fecha + rot_tipo + rot_id + rot_info
        f = open('QUERIES/maniobras.sql' , 'a')
        f.write(rot)
        f.close()
        actions = rotonda.actions
        orden = 0
        for action in actions:
            fecha ='\n(\'' + str(rotonda.fecha) + '\', '
            maniobra_tipo  = str(rotonda.tipo) + ','
            maniobra_id  = str(rotonda.id) + ','
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
            
            act = fecha + maniobra_tipo + maniobra_id + ord +  verbalizada +percepcion + accion + distancia_ceda_m + vel_actual +limite_api + pos + distancia_coche + tr_zi + tr_zc + tr_zd + coche_izq + coche_der
            act = act.replace('None', 'null')
            act = act.replace(',  ,', ', null,')
            f = open('QUERIES/acciones.sql' , 'a')
            f.write(act)
            f.close()
            orden  = orden +  1
    final_query('QUERIES/maniobras.sql')
    final_query('QUERIES/acciones.sql')

    execute_query('QUERIES/maniobras.sql')
    execute_query('QUERIES/acciones.sql')