class Rotonda:
    def __init__(self, fecha, actions):
        self.fecha = fecha
        self.actions = actions

'''class Maniobra:
    def __init__(self, fecha, id, tipo, info):
        self.fecha = fecha
        self.id = id
        self.tipo = tipo
        self.info = info'''

class Action:
    def __init__(self, verbalizada, percepcion, accion, distancia_ceda_m, vel_actual, limite_api, pos, distancia_coche, tr_zi, tr_zc, tr_zd, coche_izq, coche_der):
        self.verbalizada = verbalizada
        self.percepcion = percepcion
        self.accion = accion
        self.distancia_ceda_m = distancia_ceda_m
        self.vel_actual = vel_actual
        self.limite_api = limite_api
        self.pos = pos
        self.distancia_coche = distancia_coche
        self.tr_zi = tr_zi
        self.tr_zc = tr_zc
        self.tr_zd = tr_zd
        self.coche_izq = coche_izq
        self.coche_der = coche_der
