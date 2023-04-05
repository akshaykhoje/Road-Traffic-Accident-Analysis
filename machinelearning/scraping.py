import csv
from serpapi import GoogleSearch
import json

data = []
searchlist = [["Pune", "Shivaji Nagar"], ["Pune", "Koregaon Park"], ["Pune", "Kothrud"], ["Hyderabad", "Hitech City"], 
              ["Hyderabad", "Golconda Fort"], ["Hyderabad", "Charminar,"],["Chennai", "Marina Beach"], ["Chennai", "Mylapore"],
              ["Bengaluru", "MG Road"], ["Bengaluru", "Indiranagar"], ["Delhi", "Chandni Chowk"], ["Delhi", "Connaught Place"]]

for ele in searchlist: 
    params = {
        "api_key": "7909b9845684dcb2fdec6cb07075728ad559aebbca8bfa221029b591500fd1aa",        
        "engine": "google",       # serpapi parsing engine
        "q": ele[1] + " " + ele[0] + " " + "accidents",         # search query
        "tbm": "nws"              # news results
    }
    search = GoogleSearch(params)
    pages = search.pagination()
    for page in pages:
        for result in page["news_results"]:
            data.append({"contents" : result['source'] + " " + result['title']})

filename = "scrappeddata.csv"
with open(filename, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=data[0].keys())
    writer.writeheader()
    for row in data:
        writer.writerow(row)