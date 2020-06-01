from bs4 import BeautifulSoup
import requests
from textblob import TextBlob

out_str = ""
def web_scrape(term,out_str):
    url = 'https://www.google.com/search?hl=en&q={0}&source=lnms&tbm=nws'.format(term)
    
    
    headers = {"Accept-Language": "en-US, en;q=0.5"}

    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.text, 'html')
    print(soup)
    headline_results = soup.find_all('div', {'class': "BNeawe s3v9rd AP7Wnd"})
    print(headline_results)


    for text in headline_results:
        blob = TextBlob(text.get_text())
        if blob.detect_language() == 'de':
            Englishstr = blob.translate(from_lang='de',to="en")
            out_str= out_str + str(Englishstr)
        else:
            out_str= out_str + str(blob)
    return out_str
        
        


print(web_scrape('Chaplin,Charlie',out_str))