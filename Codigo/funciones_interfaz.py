
from PyQt5 import QtCore
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


#------------ Segunda Ventana ------------#

def cargarVideo(path):
    url = QtCore.QUrl.fromLocalFile(path)
    return url


def cortar(path, valorInicio, valorFin):
    if valorInicio == '' and valorFin == '':
        return path
    else:
        valorInicio = int(valorInicio)
        valorFin = int(valorFin)
        nombre_nuevo = path.replace(".mp4", "_cortado.mp4")
        ffmpeg_extract_subclip(path, valorInicio, valorFin, targetname=nombre_nuevo)
        return nombre_nuevo
    