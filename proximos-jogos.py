import re
import requests
from bs4 import BeautifulSoup
from pytz import timezone
from datetime import datetime
from datetime import timedelta


team_url = "http://globoesporte.globo.com/futebol/times/flamengo/"

#Perform a get request to the overall URL with the python requests library
request = requests.get(team_url)
#Extract the string body of the response
html = request.content

#Instantiate our BS parser with the HTML and the kind of parser we want to use
soup = BeautifulSoup(html, "html.parser")

jogos = soup.find_all(class_= re.compile("jogo [pv]"))

print("%-10s%-10s%-30s%s" %("Data", "Tempo","Competição", "Jogo"))
print("-"*60)
for jogo in jogos[:5]:
    jogo = jogo.text
    jogo = re.sub('\n', "", jogo)
    date = jogo[:5]
    gameday = date
    today = date[0].lower()
    if today.isalpha():
        if today == 'a':
            date = (datetime.now() + timedelta(days=1)).strftime("%d/%m")
            gameday = "Amanhã"
        if today == 'h':
            date = datetime.now().strftime("%d/%m")
            gameday = "Hoje"
    if not(gameday.isalpha()):
        gameday = list(gameday)
        gameday[0:2], gameday[3:] = gameday[3:] , gameday[0:2]
        gameday = "".join(gameday)

    timeExist = re.findall('\d{1,2}:\d{1,2}', jogo)
    if timeExist:
        time = re.findall('\d{1,2}:\d{1,2}', jogo)[0]
        #Get local time as opposed to Rio time
        fmt = "%d/%m %H:%M %Y"
        game_time = datetime.strptime((date+" "+time+" "+ str(datetime.now().year)), fmt)
        edt = timezone('US/Eastern')
        rio_timezone = timezone('Brazil/East')
        brazil_dt = rio_timezone.localize(game_time, is_dst=None)
        eastern_dt = brazil_dt.astimezone(edt)
        time = eastern_dt.strftime("%H:%M")
    else:
        time = ""

    game = re.findall("[A-Z]{3}\d*×\d*[A-Z]{3}", jogo)[0]
    youthGame = re.search("Sub-\d*",jogo)
    if youthGame:
        youth = re.findall("Sub-\d{1,2}",jogo)[0]
    match = re.search("(\d{1,2}×\d{1,2})", game)
    if match:
        game = re.sub('(\d{1,2}×\d{1,2})', r' \1 ', game)
        competition = re.sub("[^a-zÀ-ÿ\- ]", "", jogo, flags=re.I)
        competition = re.sub('([A-Z]{3}\d*.*)', "", competition)
        competition = re.sub(" *× *", "", competition)
    else: 
        competition = re.sub("[^a-zÀ-ÿ\- ]", "", jogo, flags=re.I)
        competition = re.sub('([A-Z]{3}×.*)', "", competition)
    competition = re.sub("amanhã|hoje","",competition)
    penalties = re.search("\(\d *× *\d\)",jogo)
    if penalties:
        pScore = re.findall("\(\d *× *\d\)",jogo)[0]
        pScore = re.sub(" ","",pScore)
        game = re.sub("×", pScore, game)
    if youthGame:
        competition = competition.replace("Sub-",youth)
    if match:
        print("%-10s%-9s%-28s%s" %(gameday, time, competition, game))
    else:
        print("%-10s%-9s%-30s%s" %(gameday, time, competition, game))
