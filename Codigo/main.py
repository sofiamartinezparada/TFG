from read_excel_files import main_read
from database import make_queries, create_database
from funciones_interfaz import *
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication
import sys
from video_player import Window_Player


info  = main_read()

create_database()
make_queries(info)


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
        path = os.path.abspath(str(a[0]))
        self.ruta.setText(path)
        if path.endswith('.mp4'):
            
            write_path(path)
            existe = self.comprobar_si_existe_en_excel()
            if existe == False:
                self.label_warning.setVisible(False)
                self.btnSiguiente1.setEnabled(True)

        else:
            self.label_warning.setVisible(True)



    # Abrir cuadro de diálogo
    def openDialogBox(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        return filename

    #comprobar si maniobra ya existe en el excel
    def comprobar_si_existe_en_excel(self):
        path = get_path().split('/')
        absa1 = len(path)
        absa = path[absa1-1]
        rot = absa.split('.')[1].replace('ROT','Rot')
        fech = absa.split('____')[0].replace('_','-')
        nombre = rot + ' ' + fech

        excelpath = './Info/Rotondas supervisadas v7.xlsx'
        excel_file = xl.load_workbook(excelpath)
        sheets = excel_file.sheetnames

        if nombre in sheets:
            self.label_warning.setText('Video ya analizado, seleccione otro.')
            self.label_warning.setVisible(True)
            return True
        else:
            return False


    #Cambiar a segunda pantalla
    def cambiarSegundaVentana(self):
        self.setVisible(False)
        self.segunda_ventana = QApplication(sys.argv)
        self.wp= Window_Player()
        #self.wp.__init__()
        self.wp.show()

        #Boton siguiente
        #self.btnSiguiente2.clicked.connect(self.cambiarTerceraVentana)
    #------------ Funciones Botones Segunda Ventana ------------#



#Método main de la aplicación
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())