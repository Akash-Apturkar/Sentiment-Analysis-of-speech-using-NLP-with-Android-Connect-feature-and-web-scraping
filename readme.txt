----Sentiment Analysis of speech using NLP with Android-Connect feature using Kivy with Python----
**************************************************************************************************
@ authors :
Akash Apturkar
Arush Oli
Swadesh Reddy Siddenki
Vikram Reddy
Amrut Anand

-----------------------
Steps for installing :-
-----------------------
The following modules need to be installed using pip in the command prompt before running the main code:


pip install SpeechRecognition

pip install PyAudio

pip install gTTS


pip install playsound

pip install nltk
--then in python terminal run:
>>> import nltk
>>> nltk.download()
--then select all and download

pip install collections

pip install nameparser

pip install requests

pip install bs4

pip install textblob

pip install boto3

----------------------------------------------
----Setup for Boto3 connection with AWS S3----
----------------------------------------------
in command prompt:

1.pip install awscli
2.aws configure
	aws_access_key_id = YOUR_ACCESS_KEY_ID
	aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
	region = YOUR_PREFERRED_REGION

----------
EXECUTION:
----------
1.run the Main_code.py file
2.select mode by saying either : "Speech mode" or "Remote mode" or "Opinion mode"
3.Enter voice input
