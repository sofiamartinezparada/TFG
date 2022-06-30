from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QMainWindow, QPushButton,QStyle, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
import sys
from PyQt5.QtCore import Qt, QUrl
from funciones_interfaz import *
from PyQt5 import QtMultimedia, QtWidgets, uic
from video_player2 import Window_Player_2



class Window_Player(QWidget):
    def __init__(self):
        super(Window_Player,self).__init__()
        
        self.setWindowTitle("Media Player")
        #self.setGeometry(350,100,1100,700)
        self.setMinimumSize(900,600)

        
        self.create_player()

        #self.show()

    ##IIIIMPORTANT (metodo a incorporar)
    def create_player(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        #Video widget
        video_widget = QVideoWidget()
        path = get_path()
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        video_widget.setMinimumSize(500,300)


        #horizontal 1
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(True)     
        self.inicioLabel = QLabel()
        self.inicioLabel.setText('00.00')
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)
        
        #horizontal 2
        self.initLabel = QLabel()
        self.initLabel.setText('Cortar desde el segundo: ')
        self.initCut = QLineEdit()
        self.finLabel = QLabel()
        self.finLabel.setText('hasta: ')
        self.finCut = QLineEdit()
        self.expLabel = QLabel()
        self.expLabel.setText('(Formato: xx.xx)')
        self.cutBtn = QPushButton('Cortar')
        self.cutBtn.setEnabled(False)

        self.initCut.textChanged.connect(self.onChanged)
        self.finCut.textChanged.connect(self.onChanged)

        #horizontal 3
        self.loadLabel = QLabel()
        self.loadLabel.setVisible(False)
        self.loadLabel.setText('Espere un momento mientras se genera el video cortado...')
        self.readyBtn = QPushButton('Listo')

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        hbox.addWidget(self.playBtn)
        hbox.addWidget(self.inicioLabel)
        hbox.addWidget(self.slider)

        hbox_2 = QHBoxLayout()
        hbox_2.setContentsMargins(150,0,150,0)
        hbox_2.addWidget(self.initLabel)
        hbox_2.addWidget(self.initCut)
        hbox_2.addWidget(self.finLabel)
        hbox_2.addWidget(self.finCut)
        hbox_2.addWidget(self.expLabel)
        hbox_2.addWidget(self.cutBtn)

        
        hbox_3 = QHBoxLayout()
        hbox_3.setContentsMargins(400,20,50,20)
        hbox_3.addWidget(self.loadLabel)
        hbox_3.addWidget(self.readyBtn)


        vbox = QVBoxLayout()
        vbox.addWidget(video_widget)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox_2)
        vbox.addLayout(hbox_3)

        self.mediaPlayer.setVideoOutput(video_widget)

        self.setLayout(vbox)

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.cutBtn.clicked.connect(self.cutVideo)
        self.readyBtn.clicked.connect(self.next_window)


    def onChanged(self):
        inT = self.initCut.text()
        fiT = self.finCut.text()
        if (inT != ''):
            if (fiT != ''):
                self.cutBtn.setEnabled(True)


    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else: 
            self.mediaPlayer.play()

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

        else: 
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.slider.setValue(position)
        pos = position / 100000 

        self.inicioLabel.setText("0{:.2f}".format(pos))

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def cutVideo (self):
        self.horiz3()
        path = get_path()
        valorIn = self.initCut.text()
        valorF  = self.finCut.text()
        path_new = cortar(path, valorIn, valorF)
        delete_path()
        write_path(path_new)
        self.readyBtn.setEnabled(True)
        self.loadLabel.setVisible(False)
        
    def horiz3 (self):
        self.loadLabel.setVisible(True)
        self.readyBtn.setEnabled(False)

    def next_window(self):
        self.abrirPlayer()
        self.video_audio_texto()
        self.manejo_tercera_ventana()

    def abrirPlayer(self):
        self.ventana_video = QApplication(sys.argv)
        self.wp2= Window_Player_2()
        self.wp2.show()

        '''uic.loadUi('./Interfaz/tercerapantalla.ui', self)
        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())'''

    def video_audio_texto(self):
        audio_path = aislarAudio()
        num_generado = chunkeador(audio_path)
        texto = transcribir(num_generado)
        
        self.setVisible(False)
        #abrir ventana textos
        self.window = QtWidgets.QMainWindow()
        self.window = uic.loadUi('./Interfaz/tercerapantalla.ui')
        qtRectangle = self.frameGeometry()
        bottonright = QApplication.desktop().availableGeometry().bottomRight()
        qtRectangle.moveCenter(bottonright)
        self.window.move(qtRectangle.bottomRight())
        self.window.txt_transcripcion.setText(texto)
        self.window.txt_transcripcion.textChanged.connect(self.textoCambiado)
        self.window.tableWidget.setColumnWidth(0,200)
        self.window.tableWidget.setColumnWidth(1,70)
        self.window.tableWidget.setColumnWidth(2,70)
        self.window.tableWidget.setColumnWidth(8,30)
        self.window.tableWidget.setColumnWidth(9,30)
        self.window.tableWidget.setColumnWidth(10,30)
        self.window.insertar_fila.setEnabled(False)
        self.window.guardar.setEnabled(False)
        
        self.window.show()

    def cambiado(self):
        inT = self.window.fila_edit.text()
        fiT = self.window.verbalizada_edit.text()
        if (inT != ''):
            if (fiT != ''):
                self.window.insertar_fila.setEnabled(True)
    
    def manejo_tercera_ventana(self):
        self.window.obtener.clicked.connect(self.excel)
        self.window.insertar_fila.clicked.connect(self.insert_row)
        self.window.ver_codigos.clicked.connect(self.verCodigos)
        #GUARDAR
        #self.window.guardar.clicked.connect(self.verCodigos)
        

    def textoCambiado(self):
        path = get_path()
        path = path.replace('/chunks','')
        path = path + '/texto_transcripto.txt'
        texto = self.window.txt_transcripcion.toPlainText()
        with open(path, 'w') as f:
            f.write(texto)
            f.close()

    def excel(self):
        texto = self.window.txt_transcripcion.toPlainText()
        texto = pln(texto)
        #ver escrito
        path = get_path()
        path = path.replace('/chunks','')
        path = path + '/texto_transcripto.txt'
        with open(path, 'w') as f:
            f.write(texto)
            f.close()
        self.loaddata()
        self.window.fila_edit.textChanged.connect(self.cambiado)
        self.window.verbalizada_edit.textChanged.connect(self.cambiado)
        self.window.guardar.setEnabled(True)

    def loaddata(self):
        row = 0
        texto = self.window.txt_transcripcion.toPlainText()

        verbalizadas = dividir_texto(texto)
        self.window.tableWidget.setRowCount(len(verbalizadas)-1)
        for i in range (len(verbalizadas) -1):
            verbalizada = verbalizadas[i]
            self.window.tableWidget.setItem(row,0, QtWidgets.QTableWidgetItem(verbalizada[0]))
            self.window.tableWidget.setItem(row,2, QtWidgets.QTableWidgetItem(verbalizada[1]))
            row = row +1

    def insert_row(self):
        data = self.read_data_table()
        self.window.tableWidget.setRowCount(len(data)+1)
        fila = int(self.window.fila_edit.text())
        verbalizada = self.window.verbalizada_edit.text()
        verbalizada = pln(verbalizada)
        act = comprobar_verbalizada(verbalizada)
        self.window.tableWidget.setItem(fila-1,0, QtWidgets.QTableWidgetItem(verbalizada))
        for col in range(1,13):
            self.window.tableWidget.setItem(fila-1,col, QtWidgets.QTableWidgetItem(''))
        if act != None:
            self.window.tableWidget.setItem(fila-1,2, QtWidgets.QTableWidgetItem(act))

        for i in range (fila, len(data)+1):
            fila_act = data[i-1]
            for col in range (0, 13):
                self.window.tableWidget.setItem(i,col, QtWidgets.QTableWidgetItem(fila_act[col]))

    def read_data_table(self):
        data = []
        rowCount = self.window.tableWidget.rowCount()
        columnCount = self.window.tableWidget.columnCount()
        for row in range(rowCount):
            info_fila = []
            for column in range (0,columnCount):
                widgetItem = self.window.tableWidget.item(row,column)
                if widgetItem != None:
                    text_widget = widgetItem.text()
                else:
                    text_widget = ''
                info_fila.append(text_widget)
            data.append(info_fila)
        return data

    def verCodigos(self):
        self.absa = QtWidgets.QMainWindow()
        self.absa = uic.loadUi('./Interfaz/anexo.ui')
        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.absa.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window_Player()
    sys.exit(app.exec_())

    