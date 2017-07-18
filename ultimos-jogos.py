import re
import requests
from bs4 import BeautifulSoup

team_url = "http://globoesporte.globo.com/futebol/times/flamengo/"

#Perform a get request to the overall URL with the python requests library
request = requests.get(team_url)
#Extract the string body of the response
html = request.content

#Instantiate our BS parser with the HTML and the kind of parser we want to use
soup = BeautifulSoup(html, "html.parser")

jogos = soup.find_all(class_="jogo anterior")

print("%-10s%-30s%s" %("Data", "Competição", "Resultado"))
print("-"*50)
for jogo in jogos[-5:]:
    jogo = jogo.text
    date = jogo[:5]
    date = list(date)
    date[0:2], date[3:] = date[3:] , date[0:2]
    date = "".join(date)
    result = re.findall("[A-Z]{3}\d{1,2}×\d{1,2}[A-Z]{3}", jogo)[0]
    result = re.sub('(\d{1,2}×\d{1,2})', r' \1 ', result)
    competition = re.sub("[^a-z]", "", jogo, flags=re.I)[:-17]
    competition = re.sub('([A-Z]|do)', r' \1', competition)
    competition = competition.replace("Sub","Sub-20")
    print("%-9s%-30s%s" %(date, competition, result))
