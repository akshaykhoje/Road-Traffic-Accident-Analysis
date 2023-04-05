from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
from serpapi import GoogleSearch
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
import joblib
import pickle
import re
nltk.download('stopwords')
port_stem=PorterStemmer()


def my_api(request):
    city = request.GET.get('city')
    region = request.GET.get('region')
    
    result = get_news(city, region)

    response_data = {
        'result': result['result'],
        'plot1': result['plot1'],
        'plot2': result['plot2']
    }
    
    return JsonResponse(response_data)

def stemming(contents):
    stemmed_content=re.sub('[^a-zA-Z]',' ',contents)
    stemmed_content=stemmed_content.lower()
    stemmed_content=stemmed_content.split()
    stemmed_content=[port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
    return stemmed_content

def get_news(city, region):
    vectorizer=TfidfVectorizer()
    model = joblib.load('/Users/hmk/Desktop/integrated/api/news/model.model')
    with open('/Users/hmk/Desktop/integrated/api/news/vectorizer.pickle', 'rb') as f:
        vectorizer = pickle.load(f)
    params = {
        "api_key": "7909b9845684dcb2fdec6cb07075728ad559aebbca8bfa221029b591500fd1aa",
        "engine": "google",
        "q": f"{city} {region} accidents",
        "tbm": "nws"
    }

    search = GoogleSearch(params)
    pages = search.pagination()

    auth_sources = {"The Times of India", "The Indian Express", "Hindustan Times"}
    auth_high = set()
    auth_medium = set()
    auth_low = set()
    non_auth_high = set()
    non_auth_medium = set()
    non_auth_low = set()

    news_counts = {}

    for page in pages:
        print(f"Current page: {page['serpapi_pagination']['current']}")

        for result in page["news_results"]:
            title = result["title"]
            s = [result["source"] + " " + result["title"]]
            print(s)
            df = pd.DataFrame(s, columns =['contents'])
            df['contents']=df['contents'].apply(stemming)
            X = df['contents'].values
            del df
            s = ""
            for val in X[0]:
                s += val
                s += " "
            X = vectorizer.transform([s])
            prediction=model.predict(X)
            print(prediction)
            if result["source"] in auth_sources:
                auth = True
                if "killed" in title.lower() or "died" in title.lower():
                    auth_high.add(title)
                elif "injured" in title.lower():
                    auth_medium.add(title)
                else:
                    auth_low.add(title)
            else:
                auth = False
                if "killed" in title.lower() or "died" in title.lower():
                    non_auth_high.add(title)
                elif "injured" in title.lower():
                    non_auth_medium.add(title)
                else:
                    non_auth_low.add(title)

            # Count the number of times the news appears in each set
            if title in news_counts:
                if auth:
                    news_counts[title]["auth"] += 1
                else:
                    news_counts[title]["non_auth"] += 1
            else:
                if auth:
                    news_counts[title] = {"auth": 1, "non_auth": 0}
                else:
                    news_counts[title] = {"auth": 0, "non_auth": 1}

    output_dict = {
        "result": [
            {
                "link": result["link"],
                "title": result["title"],
                "date": result["date"],
                "source": result["source"]
            } for result in page["news_results"]
        ],
        "plot1": {
            "high": len(auth_high) + len(non_auth_high),
            "medium": len(auth_medium) + len(non_auth_medium),
            "low": len(auth_low) + len(non_auth_low)
        },
        "plot2": {
            "authentic": len(auth_high) + len(auth_medium) + len(auth_low),
            "nonauthentic": len(non_auth_high) + len(non_auth_medium) + len(non_auth_low)
        }
    }

    return output_dict
