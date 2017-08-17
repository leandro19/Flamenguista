import re
import requests
from bs4 import BeautifulSoup
from colors import bcolors




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

    match = re.search("^F", result)
    goals = re.findall('\d{1,2}',result)
    if match:
        if goals[0] > goals[1]:
            result = bcolors.GREEN + result + bcolors.ENDC
        elif goals[0] < goals[1]:
            result = bcolors.RED + result + bcolors.ENDC
    else:
        if goals[0] < goals[1]:
            result = bcolors.GREEN + result + bcolors.ENDC
        elif goals[0] > goals[1]:
            result = bcolors.RED + result + bcolors.ENDC


    youthGame = re.search("Sub-\d{2}",jogo)
    if youthGame:
        youth = re.findall("Sub-\d{2}",jogo)[0]
    competition = re.sub("[^a-zÀ-ÿ\- ]", "", jogo, flags=re.I)
    competition = re.sub('([A-Z]{3}×.*)', '', competition)
    if youthGame:
        competition = competition.replace("Sub-",youth)
    print("%-9s%-30s%s" %(date, competition, result))
