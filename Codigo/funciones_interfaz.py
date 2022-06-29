
from PyQt5 import QtCore
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment
from pydub.utils import make_chunks
import speech_recognition as sr
import os


#------------ Segunda Ventana ------------#

def cargarVideo(path):
    url = QtCore.QUrl.fromLocalFile(path)
    return url


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

def nombre_maniobra(path):
    spliteado = path.split('/')
    last = spliteado[len(spliteado)-1]
    last = last.replace('.mp4','')
    return last

#------------ Funciones Tercera Ventana ------------#

# Aisla el audio
def aislarAudio():
    path = get_path()
    video_extraer_audio = VideoFileClip(path)
    #2021_07_06____11_25____1_Subjetiva.ROT 1.mp4
    name = nombre_maniobra(path)
    new_path = './Info/' + name
    if not os.path.isdir(new_path):
        os.mkdir(new_path)
    

    audio_path = new_path + '/audio_aislado.wav'
    video_extraer_audio.audio.write_audiofile(audio_path)
    audioFile = sr.AudioFile(audio_path)
    return audio_path
#Chunkea el audio
def chunkeador(audio_path):
    sound_file = AudioSegment.from_wav(audio_path)
    #silencio = split_on_silence(sound_file, min_silence_len=500, silence_thresh=-40 )
    chunks_path = audio_path.replace('/audio_aislado.wav', '/chunks')
    audio_chunks = make_chunks(sound_file, 20000)
    if not os.path.isdir(chunks_path):
        os.mkdir(chunks_path)

    for i, chunk in enumerate(audio_chunks):
        absa = os.path.join(chunks_path , f"chunk{i}.wav")
        chunk.export(absa, format="wav")
    
    delete_path()
    write_path(chunks_path)
    return (i+1)

#Transcribe el audio a texto mediante libreria Speech recognizer
def transcribir(numero_de_chunks):
    reconocedor = sr.Recognizer()
    texto_devolver = ''
    actual_path = get_path()
    for i in range(numero_de_chunks):
        path_chunk = actual_path + "/chunk" + str(i) + ".wav"
        with sr.AudioFile(path_chunk) as source:
            audio_data = reconocedor.record(source)
            text = reconocedor.recognize_google(audio_data, language = "es-ES",  show_all=True)
            
            if (str(text) != "[]"):
                textaux = reconocedor.recognize_google(audio_data, language = "es-ES")
                print("chunk numero:" , i)
                print(str(textaux))
                print("---------")
                texto_devolver = texto_devolver+ " " + str(textaux)
    
    texto_path = actual_path.replace('/chunks','/texto_transcripto.txt')
    actual_path = actual_path.replace(' ', '\ ')
    instruccion = 'rm -r ' +actual_path
    os.system(instruccion)
        
    with open(texto_path, 'w') as f:
        f.write(texto_devolver)
        f.close()
    return texto_devolver

