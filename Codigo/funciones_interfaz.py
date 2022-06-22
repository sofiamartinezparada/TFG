
from PyQt5 import QtCore
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip
import os

#------------ Segunda Ventana ------------#

def cargarVideo(path):
    url = QtCore.QUrl.fromLocalFile(path)
    return url

'''
from moviepy.video.io.VideoFileClip import VideoFileClip

input_video_path = 'myPath/vid1.mp4'
output_video_path = 'myPath/output/vid1.mp4'

with VideoFileClip(input_video_path) as video:
    new = video.subclip(t1, t2)
    new.write_videofile(output_video_path, audio_codec='aac')
'''


def cortar(path, valorInicio, valorFin):
    if valorInicio == '' and valorFin == '':
        return path
    else:
        valorInicio =  transformSec(valorInicio)
        valorFin = transformSec(valorFin)
        print(valorInicio)
        print(valorFin)
        with VideoFileClip(path) as video:
            new = video.subclip(valorInicio, valorFin)
            nombre_nuevo = path.replace(".mp4", "_cortado.mp4")
            new.write_videofile(nombre_nuevo, audio_codec='aac')
        
        return nombre_nuevo

def transformSec(valor):
    absa = valor.split('.')
    numero = int(absa[0])*60 + int(absa[1])
    return  numero

def get_path():
    with open('./Info/path.txt', 'r') as f:
        path = f.read()
        f.close()
    return path

def delete_path():
    os.remove('./Info/path.txt')

def write_path(path):
    with open('./Info/path.txt', 'w') as f:
        f.write(path)
        f.close()