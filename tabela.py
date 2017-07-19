import re
import requests
from bs4 import BeautifulSoup
from colors import bcolors




table_url = "http://globoesporte.globo.com/futebol/brasileirao-serie-a/"

#Perform a get request to the overall URL with the python requests library
request = requests.get(table_url)
#Extract the string body of the response
html = request.content

#Instantiate our BS parser with the HTML and the kind of parser we want to use
soup = BeautifulSoup(html, "html.parser")

pontos = soup.find(class_="tabela-pontos").find_all("td", text=re.compile("-\d*|(^\d*[^.]$)"))
stats = []
for ponto in pontos:
    stats += [ponto.text]

print("%-20s%-5s%-5s%-5s%-5s%-5s%-5s%-5s%-5s" %("Classificação", "P", "J", "V", "E", "D", "GP", "GC", "SG"))
print("-"*58)
times = soup.find_all(class_="tabela-times-time-nome")
i = 1
j = 0
for time in times:
    teamStats = stats[j:j+8]
    if time.text != "Flamengo":
        teamTup = (time.text,)
    else:
        teamTup = (bcolors.RED + time.text + bcolors.ENDC,)# + "          ",)

    for stat in teamStats:
        teamTup += (stat,)
    rank = i
    if i<5:
        rank = bcolors.BLUE + str(i) + bcolors.ENDC
    elif i<7:
        rank = bcolors.CYAN + str(i)+bcolors.ENDC
    elif i<13:
        rank = bcolors.GREEN + str(i)+bcolors.ENDC
    elif i>16:
        rank = bcolors.RED + str(i)+bcolors.ENDC
    if time.text == "Flamengo":
        if i<10:
            print(rank,"%-27s%-5s%-5s%-5s%-5s%-5s%-5s%-5s%-4s"%teamTup)
        else: 
            print(rank,"%-26s%-5s%-5s%-5s%-5s%-5s%-5s%-5s%-4s"%teamTup)
    elif i<10:
        print(rank,"%-18s%-5s%-5s%-5s%-5s%-5s%-5s%-5s%-4s"%teamTup)
    else: 
        print(rank,"%-17s%-5s%-5s%-5s%-5s%-5s%-5s%-5s%-4s"%teamTup)
    i +=1
    j += 8
