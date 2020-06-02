from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.graph import MeshLinePlot
from kivy.clock import Clock
from threading import Thread
import threading
import audioop
import pyaudio
import wave
import speech_recognition as sr
import boto3
from playsound import playsound
from textblob import TextBlob as blob
import sample


def get_microphone_level():
    chunk = 1024 * 2  # number of samples per chuck
    FORMAT = pyaudio.paInt16  # bytes per second
    CHANNELS = 1  # for channel to access microphone mono audio
    RATE = 44100  # sample per second
    p = pyaudio.PyAudio()  # creating main class

    s = p.open(format=FORMAT,
               channels=CHANNELS,
               rate=RATE,
               input=True,
               frames_per_buffer=chunk)  # object of main class
    global levels
    while True:
        data = s.read(chunk)
        mx = audioop.rms(data, 2)  # measuring the power of audio signal fragment,width
        if len(levels) >= 100:
            levels = []
        levels.append(mx)


def voice_text():
    harvad = sr.AudioFile('my.wav')  # reading the file
    r = sr.Recognizer()
    with harvad as source:
        audio = r.record(source)  # records the data from entire file into audio data
    val = r.recognize_google(audio)  # here the voice converted to text
    with open('my.txt', 'w') as r:
        r.write(val)  # writing the text to file


def update():
    s3 = boto3.client('s3')  # client representing amazon sample storage service
    s3.upload_file('my.wav', 'voicerecorder12', 'my.wav')  # uploading file
    s3.upload_file('my.txt', 'voicerecorder12', 'my.txt')
    s3.upload_file('sentiment.txt', 'voicerecorder12', 'sentiment.txt')


def play_back():
    playsound('my.wav')  # playsound is a library to play the audiofile


def sentiment():
    with open('my.txt') as t:
        a = t.read()
    tb = blob(a)  # textblob is a string which works like natural language processing
    c = str(tb.sentiment)  # here we are extracting sentiment from the string
    with open('sentiment.txt', 'w') as s:
        s.write(c)


class Logic(BoxLayout):
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 44100
    frames = []

    def __init__(self, **kwargs):
        self.isrecording = False  # to control start and stop
        super(Logic, self).__init__(**kwargs)  # The function returns a temporary object that allows reference to a
        # parent class
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])  # plotting and its color

    def start(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.sample_format, channels=self.channels, rate=self.fs,
                                  frames_per_buffer=self.chunk, input=True)
        self.isrecording = True
        t = threading.Thread(target=self.record)  # here the thread is running the target
        t.start()
        self.ids.graph.add_plot(self.plot)  # To access the input in your external method
        Clock.schedule_interval(self.get_value, 0.001)  # this calls back get_value every 0.001 sec

    def stop(self):
        self.isrecording = False
        self.filename = 'my.wav'
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        voice_text()
        sentiment()
        Clock.unschedule(self.get_value)  # unschedule

    def voice_play(self):
        play_back()

    def playback(self):
        sample.voice_play()  # plays the voice with sentiment

    def record(self):
        while self.isrecording:
            data = self.stream.read(self.chunk)  # takes the value from line 84
            self.frames.append(data)

    def get_value(self, dt):
        self.plot.points = [(i, j / 5) for i, j in enumerate(levels)]  # enumerate method adds a counter to an iterable
        # and returns it in a form of enumerate object


class RealTimeMicrophone(App):
    def build(self):
        return Builder.load_file("look.kv")


if __name__ == "__main__":
    levels = []  # store levels of microphone
    get_level_thread = Thread(target=get_microphone_level)
    get_level_thread.daemon = True  # used because where letting the thread die in the middle of its work without
    # losing or corrupting data
    get_level_thread.start()
    RealTimeMicrophone().run()
    update()
