from read_excel_files import main_read
from database import make_queries, create_database
from funciones_interfaz import *
import os
from patrones import velocidades_marcha, embragar
from PyQt5 import QtMultimedia, QtWidgets, uic
import sys


info  = main_read()

create_database()
make_queries(info)

'''
deceleracion_tercera = velocidades_marcha('tercera', 'Aprox')
print(deceleracion_tercera)

deceleracion_segunda = velocidades_marcha('segunda', 'Aprox')
print(deceleracion_segunda)

deceleracion_primera = velocidades_marcha('primera', 'Dentro')
print(deceleracion_primera)

aceleracion_segunda = velocidades_marcha('segunda', 'Dentro')
print(aceleracion_segunda)

por_embrague = embragar()
print(por_embrague)'''


#------------ Variables Globales ------------#
path = ' '  #ruta del archivo de video

#INTERFAZ
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()

        #Iniciamos la primera ventana
        uic.loadUi('./Interfaz/pantalla_principal.ui',self)      
        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.label_warning.setVisible(False)


        #Controladores de botones
        ## Botón seleccionar video local
        self.btnLocal.clicked.connect(self.insertarVideoLocal)

        ## Botón siguiente (de 1ª a 2ª ventana)
        self.btnSiguiente1.setEnabled(False)
        self.btnSiguiente1.clicked.connect(self.cambiarSegundaVentana)

    
        # Inserta un vídeo desde una ruta local
    def insertarVideoLocal(self):
        a = self.openDialogBox()
        global path
        path = os.path.abspath(str(a[0]))
        self.ruta.setText(path)
        if path.endswith('.mp4'):
            self.label_warning.setVisible(False)
            self.btnSiguiente1.setEnabled(True)
        else:
            self.label_warning.setVisible(True)


    # Abrir cuadro de diálogo
    def openDialogBox(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        return filename


    #Cambiar a segunda pantalla
    def cambiarSegundaVentana(self):
        #Cargamos la segunda ventana
        uic.loadUi('./Interfaz/segundapantalla.ui', self)
        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        #Inicializamos el widget del video
        self.mediaPlayer = QtMultimedia.QMediaPlayer(self)
        self.mediaPlayer.setVideoOutput(self.widget)

        #Cargamos el video seleccionado en la ventana anterior
        url = cargarVideo(path)
        self.mediaPlayer.setMedia(QtMultimedia.QMediaContent(url))
        self.mediaPlayer.play()


        #Boton siguiente
        #self.btnSiguiente2.clicked.connect(self.cambiarTerceraVentana)
    #------------ Funciones Botones Segunda Ventana ------------#



#Método main de la aplicación
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())