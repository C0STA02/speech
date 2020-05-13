"""For developers - >  the application based on speech_recognition library + PyAudio library. However i won't make the recognition from stream, casue i hadn't found info about wav
U can read here: 
https://realpython.com/python-speech-recognition/#supported-file-types 
https://issue.life/questions/26573556 
"""
#ElimiC0
version = 1.0
#-----------
import time
import os
import wave
import pyaudio
import speech_recognition as sr
import pygame
import tkinter as tk
#WHAT YOU CAN CHANGE:
RECORD_SECONDS = 5 #time to record in sec. Each ... seconds your sound will updates. I prefer 5-6 sec
listName = ['миша', 'михаил', 'лежнин', 'миш', 'мишка'] #your name / how the teacher calls u usually. 
colorNotPressed = "green"
colorPressed = "red"
#THAT'S ALL

#FOR PYAUDIO
CHUNK = 2048
FORMAT = pyaudio.paInt16
RATE = 44100
CHANNELS = 2
WAVE_OUTPUT_FILENAME = "output.wav"
r = sr.Recognizer()
p = pyaudio.PyAudio()
#--

def switchingLigths():
	for i in range(25):
		time.sleep(0.2)
		if root["bg"]==colorNotPressed:
			root["bg"] = colorPressed
		else:
			root["bg"] = colorNotPressed
		root.update()
		
def changingLigths():
	root["bg"] = colorPressed
	root.update()
	time.sleep(1)
	root["bg"] = colorNotPressed
	root.update()
def playSound(): 
	switchingLigths() 


def checkSound():
	stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
	frames = []
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)
	stream.stop_stream()
	stream.close()
	p.terminate()
	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()
	print("CHECK ENDED")
#--
def findFromList(string):
	for i in listName:
		if string.find(i)!=-1:
			return 1
	return 0

#---------------------------------------------
print("SpeechChecker Version {} is working.".format(version))

#---tkinter block
root = tk.Tk()
e = tk.Entry(root, width=20)
root["bg"] = colorNotPressed
root.mainloop()
#---tkinter block end

while True:
	checkSound()
	sound = sr.AudioFile('output.wav')
	print("START AUDIO")
	try:
		with sound as source:
			audio = r.record(source)
			stringAudio = r.recognize_google(audio, language = 'ru-RU')
		if findFromList(stringAudio.lower())!=0:
			print(stringAudio)
			playSound()
	except Exception as e:
		print("The error: " + str(e))
