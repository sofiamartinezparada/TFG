from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QPushButton,QStyle, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
import sys
from PyQt5.QtCore import Qt, QUrl


class Window_Player(QWidget):
    def __init__(self):
        super(Window_Player,self).__init__()
        
        self.setWindowTitle("Media Player")
        #self.setGeometry(350,100,1100,700)
        self.setMinimumSize(900,600)
        self.cutBtn.clicked.connect(self.cutVideo)

        path = get_path()
        self.create_player(path)

        self.show()

    ##IIIIMPORTANT (metodo a incorporar)
    def create_player(self, path):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        #Video widget
        video_widget = QVideoWidget()

        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        video_widget.setMinimumSize(500,300)



        self.playBtn = QPushButton()
        self.playBtn.setEnabled(True)     

        self.inicioLabel = QLabel()

        self.inicioLabel.setText('00.00')


        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)
        

        self.initLabel = QLabel()
        self.initLabel.setText('Cortar desde el segundo: ')
        self.initCut = QLineEdit()
        self.finLabel = QLabel()
        self.finLabel.setText('hasta: ')
        self.finCut = QLineEdit()
        self.expLabel = QLabel()
        self.expLabel.setText('(Formato: xx.xx)')
        self.cutBtn = QPushButton('Cortar')

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        hbox.addWidget(self.playBtn)
        hbox.addWidget(self.inicioLabel)
        hbox.addWidget(self.slider)
        #hbox.addWidget(self.finLabel)

        hbox_2 = QHBoxLayout()
        hbox_2.setContentsMargins(150,0,150,0)
        hbox_2.addWidget(self.initLabel)
        hbox_2.addWidget(self.initCut)
        hbox_2.addWidget(self.finLabel)
        hbox_2.addWidget(self.finCut)
        hbox_2.addWidget(self.expLabel)
        hbox_2.addWidget(self.cutBtn)



        vbox = QVBoxLayout()
        vbox.addWidget(video_widget)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox_2)

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
        

    def get_path(self):
        with open('./Info/path.txt', 'r') as f:
            path = f.read()
            f.close()
        return path

'''app  = QApplication(sys.argv)
window = Window_Player()
window.resize(640, 480)

window.show()
sys.exit(app.exec_()) '''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window_Player()
    sys.exit(app.exec_())