import sqlite3

#import numpy
from data_types import Action, Maniobra

def get_fechas_by_sect(section):
    array_rotondas = []
    connection = sqlite3.connect('maniobras.db')
    cursor = connection.cursor()
    
    consulta = 'SELECT DISTINCT fecha  from Acciones WHERE pos = \''+ section +'\''
    cursor.execute(consulta)

    info = cursor.fetchall()
    for i in info:
        array_rotondas.append(i[0])
    cursor.close()
    connection.close()
    return array_rotondas

def get_by_section(section):
    array_rotondas = []
    connection = sqlite3.connect('maniobras.db')
    cursor = connection.cursor()
    
    consulta = 'SELECT * from Acciones WHERE pos = \''+ section +'\' ORDER BY orden ASC'
    cursor.execute(consulta)

    info = cursor.fetchall()

    array_fechas = get_fechas_by_sect(section)


    for fecha in array_fechas:
        aux = []
        for dato in info:
            if fecha == dato[0]:
                act = Action(dato[2], dato[3],dato[4],dato[5],dato[6],dato[7],dato[8],dato[9],dato[10],dato[11],dato[12],dato[13],dato[14])
                aux.append(act)
        rot = Maniobra(fecha, aux)
        array_rotondas.append(rot)
    cursor.close()
    connection.close()
    return array_rotondas

def validation_percent(verbalizada, action):
    connection = sqlite3.connect('maniobras.db')
    cursor = connection.cursor()
    
    #Cases where the parameters apear
    consulta = 'SELECT COUNT(*) from Acciones WHERE accion = \''+ action +'\' AND verbalizada LIKE \'%' +verbalizada+ '%\''
    cursor.execute(consulta)
    number_cases = (cursor.fetchone())[0]

    #Total rounds
    consulta = 'SELECT COUNT(*) from Maniobras'
    cursor.execute(consulta)
    number_rotondas = (cursor.fetchone())[0]

    cursor.close()
    connection.close()
    #Percent
    percent = number_cases * 100 / number_rotondas
    #If more than 50, is an accurate data
    if percent >= 50 :
        return True
    else:
        return False

def velocidades_marcha(verbalizada, action):
    connection = sqlite3.connect('maniobras.db')
    cursor = connection.cursor()
    #consulta = 'SELECT vel_actual from Acciones WHERE verbalizada LIKE \'%' +marcha+ '%\' AND vel_actual NOT NULL'

    consulta = 'SELECT avg(vel_actual) from Acciones WHERE accion = \''+ action+ '\'AND vel_actual NOT NULL AND verbalizada LIKE \'%' + verbalizada + '%\''

    cursor.execute(consulta)
    info = (cursor.fetchone())[0]
    
    '''velocidades = []
    for i in info : 
        velocidades.append(i[0])

    media = numpy.mean(velocidades)
    '''
    #validation = validation_percent(marcha,section)

    #inf = (info , validation)
    #return media
    cursor.close()
    connection.close()
    return info

def get_cambios():
    connection = sqlite3.connect('maniobras.db')
    cursor = connection.cursor()
    consulta  = 'SELECT * FROM Acciones WHERE verbalizada LIKE \'%primera%\' OR verbalizada LIKE \'%segunda%\'  OR verbalizada LIKE \'%tercera%\'  OR verbalizada LIKE \'%cuarta%\' '

    cursor.execute(consulta)
    info = cursor.fetchall()
    cursor.close()
    connection.close()
    return info

def get_anterior_cambio(cambios):
    array_anteriores = []

    for cambio in cambios:
        fecha = cambio[0]
        orden = cambio[1]
        connection = sqlite3.connect('maniobras.db')
        cursor = connection.cursor()

        consulta = 'SELECT * FROM Acciones WHERE fecha = \'' + fecha + '\' AND orden = ' + str(orden - 1)

        cursor.execute(consulta)

        anterior = cursor.fetchall()
        array_anteriores.append(anterior)

        cursor.close()
        connection.close()

    return array_anteriores
1
def porcentaje_embragar(anteriores):
    counter = 0 
    for anterior in anteriores:
        verba = anterior[0][2]
        if 'embrago' in verba:
            counter = counter + 1
    
    percent = counter * 100 / len(anteriores)

    return percent

def embragar():
    cambs = get_cambios()
    anteriores = get_anterior_cambio(cambs)

    porcentaje = porcentaje_embragar(anteriores)

    return porcentaje


def velocidad_patron_marcha(verbalizada, act):
    verb = ''
    marchas = ['primera', 'segunda', 'tercera', 'cuarta']
    parte = verbalizada.split(' ')
    for marcha in marchas:
        for p in parte:
            if marcha == p:
                verb = marcha
    valid = validation_percent(verb, act)
    if valid:
        vel = velocidades_marcha(verb, act)
        vel = round(vel, 2)
        return vel
    else:
        return None

