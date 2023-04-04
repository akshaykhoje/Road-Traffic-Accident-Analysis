from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
import re

def my_api(request):
    # Get the parameters from the request
    city = request.GET.get('city')
    region = request.GET.get('region')
    
    # Process the parameters and prepare the response
    result = scrape_google_news_titles(city, region)
    response_data = {'result': result}
    
    # Send the response as JSON
    return JsonResponse(response_data)

def scrape_google_news_titles(city, region):
    query = f'accidents in {city}'
    url = f'https://news.google.com/search?q=road%20accidents%20in%20{city}%20{region}&hl=en-US&gl=US&ceid=US%3Aen'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article', {'class': 'MQsxIb xTewfe R7GTQ keNKEd j7vNaf Cc0Z5d EjqUne'})

    news_titles = []
    for i, article in enumerate(articles):
        title = article.find('a', {'class': 'DY5T1d'}).text
        title = title.lower()  # Convert to lowercase
        title = re.sub(r'[^\w\s]', '', title)  # Remove punctuation
        title = re.sub(r'\d+', '', title)  # Remove numbers
        title = re.sub(r'\s+', ' ', title)  # Remove extra whitespace
        news_titles.append(f"{i+1}. {title}\n")
    
    return ''.join(news_titles)