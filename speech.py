"""For developers - >  the application based on speech_recognition library + PyAudio library. However i won't make the recognition from stream, casue i hadn't found info about wav
U can read here: 
https://realpython.com/python-speech-recognition/#supported-file-types 
https://issue.life/questions/26573556 
"""
#ElimiC0
version = 1.1
#-----------
import threading
import time
import os
import wave
import pyaudio
import speech_recognition as sr
import tkinter as tk
#WHAT YOU CAN CHANGE:
RECORD_SECONDS = 5 #time to record in sec. Each ... seconds your sound will updates. I prefer 5-6 sec
listName = ['миша', 'миш', 'саш', 'саша'] #your name / how the teacher calls u usually. 
colorNotPressed = "green"
colorPressed = "red"
#THAT'S ALL

#FOR PYAUDIO
ctd = 1
CHUNK = 2048
FORMAT = pyaudio.paInt16
RATE = 44100
CHANNELS = 2
WAVE_OUTPUT_FILENAME = "output.wav"
r = sr.Recognizer()
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
#--
def switchingLigths():
	for i in range(25):
		time.sleep(0.2)
		if root["bg"]==colorNotPressed:
			root["bg"] = colorPressed
		else:
			root["bg"] = colorNotPressed
		root.update()
#--	
def changingLigths():
	root["bg"] = colorPressed
	root.update()
	time.sleep(1)
	root["bg"] = colorNotPressed
	root.update()
#--
def playAttention(): 
	switchingLigths() 
#--
def checkSound():
	frames = []
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)
	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()
#--
def findFromList(string):
	for i in listName:
		if string.find(i)!=-1:
			return 1
	return 0
#--
def exitFromProgram():
	root.destroy()
	print("SpeechChecker Version {} is closing.".format(version))
	exit()
#--mainFunction
def mainF():
	while True:
		checkSound()
		sound = sr.AudioFile(WAVE_OUTPUT_FILENAME)
		print("START AUDIO")
		try:
			with sound as source:
				audio = r.record(source)
				stringAudio = r.recognize_google(audio, language = 'ru-RU')
				if findFromList(stringAudio.lower())!=0:
					print(stringAudio)
					playAttention()
		except Exception as e:
			print("The error: " + str(e))
#-----------------------------------
#---tkinter block

root = tk.Tk()
root.geometry("100x100")
b = tk.Button(root,text = "exit",command = exitFromProgram, height = 2, width = 7)
b.pack()
root["bg"] = colorNotPressed
threading.Thread(target = mainF).start()
root.mainloop()
#---tkinter block end
