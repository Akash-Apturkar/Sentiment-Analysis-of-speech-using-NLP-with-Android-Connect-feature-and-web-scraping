# Function to download audio files from AWS S3 & cinvert to text
import speech_recognition as sr
import boto3
s3 = boto3.client('s3')
    

s3.download_file('voicerecorder12', 'my.wav', 'my.wav')

r = sr.Recognizer()
with sr.AudioFile("my.wav") as source:
    audio = r.record(source)
    s = r.recognize_google(audio)
print("Text: "+s)
