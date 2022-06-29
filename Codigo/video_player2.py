from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QMainWindow, QPushButton,QStyle, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
import sys
from PyQt5.QtCore import Qt, QUrl
from funciones_interfaz import *
from PyQt5 import QtMultimedia, QtWidgets, uic

class Window_Player_2(QWidget):
    def __init__(self):
        super(Window_Player_2,self).__init__()
        
        self.setWindowTitle("Media Player")
        #self.setGeometry(350,100,1100,700)
        self.setMinimumSize(700,500)

        
        self.create_player()
        topLeftPoint = QApplication.desktop().availableGeometry().topLeft()
        self.move(topLeftPoint)

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
        
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        hbox.addWidget(self.playBtn)
        hbox.addWidget(self.inicioLabel)
        hbox.addWidget(self.slider)


        vbox = QVBoxLayout()
        vbox.addWidget(video_widget)
        vbox.addLayout(hbox)


        self.mediaPlayer.setVideoOutput(video_widget)

        self.setLayout(vbox)

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)



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



'''app  = QApplication(sys.argv)
window = Window_Player()
window.resize(640, 480)

window.show()
sys.exit(app.exec_()) '''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window_Player_2()
    sys.exit(app.exec_())

    