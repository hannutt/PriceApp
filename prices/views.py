from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import socket
from .models import Todo
from django.shortcuts import redirect
import feedparser
from datetime import datetime
from datetime import date,time



import psutil
import platform
import random

# Create your views here.
quotes = ['A rose by any other name would smell as sweet.','All that glitters is not gold.',
'Elementary, my dear Watson.','Go ahead, make my day.','Here''s looking at you, kid.','I think therefore I am.']
def indexPage(request):
    page = requests.get('https://www.viikkonumero.fi')
    soup = BeautifulSoup(page.text, 'html.parser')
    weeks = soup.find('span',{'id':'ugenr'})
    quote = random.choice(quotes)

    for week in weeks:
        result = week.text
        FixedResult = result.replace('Viikko',' ')
        #asetetaan index.html-sivun weekPlace kohtaan FixedResult muuttuja tieto.
    return render(request,"index.html",{"weekPlace":FixedResult,"quotePlace":quote})

def FundValues(request):
    valueList = []
    page = requests.get('https://www.seligson.fi/suomi/rahastot/FundValues_FI.html')
    soup = BeautifulSoup(page.text, 'html.parser')
    value = soup.find(class_='rahasto')
    values = value.find_all('tr')
    for value in values:
        result = value.text
        valueList.append(result)
        #lista välitetään sanakirjana fundvalues.html sivulle.
        context = {'valueList':valueList}
        

    return render(request, 'fundValues.html',context)

def showRssPage(request):
     return render(request,'rssreader.html')


def getRss(request):
    feedlist = []
    address = request.POST['address']
    rssfeed = feedparser.parse(address)
    for feed in rssfeed.entries:
           feed.title + ': ' + feed.description
           
           feedlist.append(feed.title)
           feedlist.append(feed.description)
           context = {'feedlist':feedlist}

    return render(request,'rssreader.html',context)

def udpRead(request):
    udpdata = []
    ipadd = '194.34.132.110'
    port = 10110
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    sock.bind((ipadd,port))
    
    while True:
        data, addr = sock.recvfrom(1024)
        udpdata.append(data)
        context = {'udpdata',udpdata}
        return render(request, 'udpReader.html',context)
    
def showToDo(request):
    #listataan todo-modelin sisältö
        today = date.today()
        today_str = today.strftime("%d.%m.%y")
        Todolist = Todo.objects.all()
       
       
       
        #lähetetään todi.html sivulle sekä context dictionary että saman sivun DayPlace
        #kohtaan today_str
        return render(request,'todo.html',context={'Todo':Todolist,'DayPlace':today_str})
    
def saveToDo(request):
    Task = request.POST['task']
    Timelimit= request.POST["time"]
    
    Todo(task = Task, timelimit = Timelimit).save()
    return redirect (showToDo)

#id-num on poistettavan tietokantatietueen id-numero numero saadaan
#parametrina todo.html sivulta rivi 36.
def delToDo(request,idnum):
     Todo.objects.filter(id = idnum).delete()
     
     return render(request,'todo.html')

def editToDo(request,idnum):
     todo = Todo.objects.filter(id=idnum)
     context = {"todo":todo}
     return render(request,'editTodo.html',context)

def editToDoPost(request,idnum):
     editItem = Todo.objects.get(id=idnum)
     editItem.timelimit = request.POST['EditTime']
     editItem.task= request.POST['EditTask']
     editItem.save()
     
     return redirect (showToDo)

#taskien järjestys päivämäärän mukaan laskevassa järjestyksessä
#contextin sisältö on täysin sama kuin showTodo funktiossa, jolloin tälle näkymälle
#ei tarvitse html:n puolella tehdä for-silmukkaa
def orderTodo(request):
     today = date.today()
     today_str = today.strftime("%d.%m.%y")
     Todolist = Todo.objects.all().order_by('timelimit','-timelimit').values()
     context = {'Todo':Todolist}
     return render(request,'todo.html',context={'Todo':Todolist,'DayPlace':today_str})

#lasketaan montako päivää tehtävän deadlineen on.
def TimeLeft(request,idnum):
     #Item = Todo.objects.filter(id=idnum)
     
     today = date.today()
     today_str = today.strftime("%d.%m.%y")
     Todolist = Todo.objects.get(id=idnum)
     datetoday = datetime.strptime(today_str, '%d.%m.%y')
     taskDateTime = datetime.strptime(Todolist.timelimit, '%d.%m.%y')
     result = taskDateTime - datetoday
     title = Todolist.task
    
     return render(request,'todo.html',{"titlePlace":title,"difPlace":result})
     #return render(request,'showTime.html',{"difPlace":result,"titlePlace":title})

def palindromePage(request):
     
     return render(request,'palindrome.html')

def palindromeCheck(request):
     word = request.POST['word']
     word = word.replace(' ','')
     #kirjainten määrän lasku
     wordlng = len(word)
     #muunto merkkijonoksi, muuten return render lause ei hyväksy muuttujaa samassa lauseessa.
     wordStr = str(wordlng)
     if word == word[::-1]:
          result = 'Word is a palindrome'
          return render(request,'palindrome.html',{"answerPlace":result,"lenPlace":"word length is "+wordStr+ " letters"})
     else:
          result = 'Word is not a palindrome'
          return render(request,'palindrome.html',{"answerPlace":result,"lenPlace":"word length is "+wordStr+ " letters"})

def systemCheck(request):
     cpu = psutil.cpu_freq()
     #muunto merkkijonoksi
     cpuStr = str(cpu)
     #korvatataan scpufre teksti tyhjällä
     cpuFinal = cpuStr.replace('scpufreq',' ')
     battery = psutil.sensors_battery()
     batteryStr = str(battery.percent)
     memory = psutil.virtual_memory().total
     memoryFree = psutil.virtual_memory().available
     per = psutil.virtual_memory().percent
     #muuntokaava bytes -> GB
     memory= memory / (1024*1024*1024)
     memoryFree = memoryFree / (1024*1024*1024)
     #pyöristys 2 desimaalin tarkkuuteen
     memory= round(memory,2)
     memoryFree= round(memoryFree,2)
     #muunto merkkijonoksi
     memory = str(memory)
     memoryFree = str(memoryFree)
     per = str(per)

     return render(request,'system.html',{"osName":"OS & version: " +platform.system(),
                                          "osVersion": platform.version,"cpuPlace":"CPU frequencies: "+ cpuFinal,
                                          "btrPlace":"Battery status: "+ batteryStr+" %","memoryPlace":"Total Memory: "+memory+" GB",
                                          "freePlace":"Free memory: "+memoryFree+ " GB",
                                           "perPlace":"Percentage usage "+per+" %",
                                           "proPlace":"Processor: "+ platform.processor()
                                         })   

def udpPage(request):
     hostname = socket.gethostname()
     global ipAddr
     ipAddr = socket.gethostbyname(hostname)
     return render(request,'udpClient.html',{"ipPlace":ipAddr})

def udpClient(request):

          client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
          client.connect((ipAddr,9999))
          msg = request.POST['msg']
          msg_bytes = memoryview(msg.encode('utf-8')).tobytes()
          client.send(msg_bytes).encode('utf-8')

          return render(request,'udpClient.html')

def sendMail(request):
     subject = "Mail from Django App"
     body = request.POST['mailMessage']
     sender_email = "workapptest@yahoo.com"
     receiver_email = request.POST['mailAdd']
     password = "birnclvcfpfqscng"

     message = MIMEMultipart()
     message["From"] = sender_email
     message["To"] = receiver_email
     message["Subject"] = subject

     message.attach(MIMEText(body, "plain"))
     text = message.as_string()
     
     context = ssl.create_default_context()

     with smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465, context=context) as server:
     
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email,text)
        note = 'Mail sent!'
        return render(request,'udpclient.html',{"mailPlace":note})
'''
def udpReceiver(request):
     hostname = socket.gethostname()
     ipAddr2 = socket.gethostbyname(hostname)
     server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
     server.bind((ipAddr2,9999))
     server.listen()


     client,addr = server.accept()
     msg = (client.recv(1024).decode('utf-8'))

     return render(request,'udpRec.html',{"message":msg})
'''

def alarmClockPage(request):
    
     return render(request,'AlarmClock.html')
#

          

          


    
     




     
    

'''
def readUdp(request):
    
    ipadd = request.POST['IPAddress']
    port = request.POST['PortNum']

    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    sock.bind((ipadd,port))
    
    while True:
        data, addr = sock.recvfrom(1024)
        udpdata.append(data)
        context = {'udpdata',udpdata}
        return render(request, 'udpReader.html',context)
        '''