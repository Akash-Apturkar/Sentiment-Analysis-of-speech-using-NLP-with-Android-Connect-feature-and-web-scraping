import numpy
from nltk.sentiment.vader import SentimentIntensityAnalyzer


for i in numpy.arange(0,0.5,0.01):
    pos_count = 0
    pos_correct = 0

    with open("positive.txt","r") as f:
        for line in f.read().split('\n'):
            sen = SentimentIntensityAnalyzer().polarity_scores(line)
            if sen['compound'] >= i:
                pos_correct += 1
            pos_count +=1


    neg_count = 0
    neg_correct = 0

    with open("negative.txt","r") as f:
        for line in f.read().split('\n'):
            sen = SentimentIntensityAnalyzer().polarity_scores(line)
            if sen['compound'] <= -i:
                neg_correct += 1
            neg_count +=1
    print("\nValue = {} ".format(i))
    print("Positive accuracy = {}% via {} samples".format(pos_correct/pos_count*100.0, pos_count))
    print("Negative accuracy = {}% via {} samples".format(neg_correct/neg_count*100.0, neg_count))
    avj=((pos_correct/pos_count*100.0)+(neg_correct/neg_count*100.0))/2
    print("Average = {} ".format(avj))
