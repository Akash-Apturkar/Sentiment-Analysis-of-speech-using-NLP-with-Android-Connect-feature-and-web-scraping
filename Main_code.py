#For i/o, general operations
import string
import os 
from collections import Counter
#For plotting graph
import matplotlib.pyplot as plt

#Imports required for tokenization & tagging of the input string 
import nltk
from nltk.corpus import stopwords
from nltk.corpus import treebank
from nltk import ne_chunk, pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# We are using SentimentIntensityAnalyzer().polarity_scores() to get the polarity
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# required to extract human names from text
from nameparser.parser import HumanName

#For speech processing
import speech_recognition as sr
import playsound # To play mp3 files
from gtts import gTTS # Google text to speech

#For web scraping operations
from bs4 import BeautifulSoup
import requests
from textblob import TextBlob

# For AWS S3 connection
import boto3


def speak(voice_op): # this function will convert the text passed as argument into an mp3 file and play it

    tts = gTTS(text=voice_op, lang="en",slow=False) # Define an instance for the gTTS module.
    filename = "voice.mp3"

    tts.save(filename) # here, the mp3 file is saved as 'voice.mp3'
    playsound.playsound(filename) # this will play out the file
    os.remove(filename) # this will delete the file
    
    
def get_audio(): # This function will be called to convert speech into a text string
    r = sr.Recognizer()# here, we create an instance for the SpeechRecognition module
    with sr.Microphone() as source:
        audio = r.listen(source, timeout=100)# Take the speech input through the microphone.
        #It will wait for 100sec to receive an input, otherwise it will throw an error
        said = ""
# Now, we use exception handling
        try:
            said = r.recognize_google(audio)# Use google speech recognition to convert the voice input to text
            #and save it as 'said'
            said = said.replace("Mr","Mr.")
        

        except Exception: 
            speak("Didn't get that please try again")
   
    return said # the function will return 'said' which is a string

#Function used for web scraping google news results for 'term' will 
#return all headlines as a string in 'out_str'
out_str = ""
def web_scrape(term,out_str):
    url = 'https://www.google.com/search?hl=en&q={0}&source=lnms&tbm=nws'.format(term)
    
    
    headers = {"Accept-Language": "en-US, en;q=0.5"}

    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.text, 'html')
    headline_results = soup.find_all('div', {'class': "BNeawe s3v9rd AP7Wnd"})


    for text in headline_results:
        blob = TextBlob(text.get_text())
        if blob.detect_language() == 'de':
            Englishstr = blob.translate(from_lang='de',to="en")
            out_str= out_str + str(Englishstr)
        else:
            out_str= out_str + str(blob)
    return out_str

#Will extract name entities from text & return a list 'person_names'
def get_human_names(text):
    
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos)
    person_list = []
    person = []
    name = ""
    
    for subtree in sentt.subtrees():
        if subtree.label()  == 'PERSON':
            for leaf in subtree.leaves():
                person.append(leaf[0])
            if len(person) > 1: #avoid grabbing lone surnames
                for part in person:
                    name += part + ' '
                if name[:-1] not in person_list:
                    person_list.append(name[:-1])
                name = ''
            person = []

    return (person_list)

#Function to analyse the web scraping result
def online_opinion_analyse(text,name):
    scores = SentimentIntensityAnalyzer().polarity_scores(text)
    print("\nSentiment analysis result for online news about {}: ".format(name))
    print(scores)
    print("\nOnline opinion of {} is ".format(name))
    speak("Online opinion analysis result for online news about {} is ".format(name))
    if scores['compound'] < -0.01:
        print("Negative")
        speak("Negative")
    elif scores['compound'] > 0.05:
        print("Positive")
        speak("Positive")
    else:
        print("Neutral")
        speak("Neutral")

#Function for sentiment analysis of speech converted to text
def sentiment_analyse(text):
    speak("Running sentiment analysis on the speech")
    
    words = word_tokenize(text, "english")
    print("Output after tokenization: ")
    print(words)


    pos = pos_tag(words)
    print("\nOutput after parts of speech tagging: ")
    print(pos)

    name_entities = ne_chunk(pos)
    print("\nOutput after name entities tagging: ")
    print(name_entities)
    

    # Lemmatization - From plural to single + Base form of a word 
    lemmatized_words = []
    for word in words:
        word = WordNetLemmatizer().lemmatize(word)
        lemmatized_words.append(word)

    emotion_list = []
    
    with open('emotions.txt', 'r') as file:
        for line in file:
            clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
            word, emotion = clear_line.split(':')
        

            if word in lemmatized_words:
                emotion_list.append(emotion)
    
    print("\nList of emotions found in the speech :")
    print(emotion_list)
    w = Counter(emotion_list)
    print("\nEmotion counter: ")
    print(w)
    
    fig, ax1 = plt.subplots()
    ax1.bar(w.keys(), w.values())
    fig.autofmt_xdate()
    
    plt.show()
    plt.savefig('graph.png')



    scores = SentimentIntensityAnalyzer().polarity_scores(text)
    print("Sentiment analysis result: ")
    print(scores)
    print("\nOverall Sentiment : ")
    speak("Overall Sentiment is ")
    if scores['compound'] < -0.01:
        print("Negative")
        speak("Negative")
    elif scores['compound'] > 0.05:
        print("Positive")
        speak("Positive")
    else:
        print("Neutral")
        speak("Neutral")
    
    name_entities.draw()

# Main execution starts here:-----------------------------------------

print("Select mode:\n1.Speech mode\n2.Remote mode\n3.Opinion mode")
speak("Welcome to sentiment analyzer. Please select mode")

user_speech = get_audio()

if "opinion" in user_speech.lower():
    print("Opinion mode selected")
    speak("Opinion mode selected. State the topic")
    user_speech = get_audio()
    print("Your input: {}".format(user_speech))
    speak("Running Online opinion analysis of {}".format(user_speech))
    text = web_scrape(user_speech,out_str)
    print(text)
    online_opinion_analyse(text,user_speech)


if "speech" in user_speech.lower():
    print("Speech mode selected")
    speak("Speech mode selected. Begin speaking")
    
    user_speech = get_audio()
    print("Your input: {}".format(user_speech))
    
    sentiment_analyse(user_speech)

    names = get_human_names(user_speech)
    
    print ("\nName entities detected in the speech are :")
    speak("Name entities detected in the speech are ")
    for name in names: 
        last_first = HumanName(name).last + ',' + HumanName(name).first
        print(last_first)
        speak(last_first)
    for name in names: 
        last_first = HumanName(name).last + ',' + HumanName(name).first
        print("Running Online opinion analysis of {}".format(last_first))
        speak("Running Online opinion analysis of {}".format(last_first))
        text = web_scrape(last_first,out_str)
        print(text)
        online_opinion_analyse(text,last_first)

if "remote" in user_speech.lower():
    print("Remote mode selected")
    speak("Remote mode selected. Fetching audio file from Amazon S3")
    s3 = boto3.client('s3')
    s3.download_file('voicerecorder12', 'my.wav', 'my.wav')

    r = sr.Recognizer()
    with sr.AudioFile("my.wav") as source:
        audio = r.record(source)
        user_speech = r.recognize_google(audio)
        user_speech = user_speech.replace("Mr","Mr.")
    print("Your input: {}".format(user_speech))
    
    sentiment_analyse(user_speech)

    names = get_human_names(user_speech)
    
    print ("\nName entities detected in the speech are :")
    speak("Name entities detected in the speech are ")
    for name in names: 
        last_first = HumanName(name).last + ',' + HumanName(name).first
        print(last_first)
        speak(last_first)
    for name in names: 
        last_first = HumanName(name).last + ',' + HumanName(name).first
        print("Running Online opinion analysis of {}".format(last_first))
        speak("Running Online opinion analysis of {}".format(last_first))
        text = web_scrape(last_first,out_str)
        print(text)
        online_opinion_analyse(text,last_first)
