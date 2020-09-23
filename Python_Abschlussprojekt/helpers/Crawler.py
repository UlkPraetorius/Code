#-------Crawler.py
#Dieser Code sollte nicht ausgeführt werden (sehr hohe Laufzeit und funtkioniert nicht einwandfrei, weil Z.26-Z.37 manuelle Ausführung verlangen (sonst: falsche Zuordnung der Autoren))
# sondern dient der Nachvollziehbarkeit der Textgewinnung.

#Laden der Pakete
import requests
import re
from bs4 import BeautifulSoup
import pickle

#der Inhalt der Webpage mit der Übersicht aller Romane des Projekts Gutenberg wird geladen
r = requests.get('https://gutenberg.spiegel.de/genre/roman-im-engl-novel--fiction')
html=r.text
#ein Soupobjekt (HTML-Baum) wird initiiert
soup = BeautifulSoup(html)

#t liefert eine Liste aller Links, die auf eine Seite mit Buchtexten verweisen
t=soup.find_all(href=re.compile("/buch"))
#a liefert eine Liste aller Links, die auf eine Seite zu einem Autor verweisen
a=soup.find_all(href=re.compile("/autor"))
#überflüssiges wird abgeschnitten(die Auswahl erfolgte manuell)
t=t[2:]
a=a[28:2623]



#Alle Werke ohne Autorverlinkung (vorher händisch ermittelt) werden aus t gelöscht
#for index in range(len(t)-1):
    #Folgende 2 auskomentierte Zeilen sind unter Vorbehalt ebenfalls auszuführen
    #Achtung nur erster Treffer-> if len(re.findall("Die Million", str(t[index])))==1:
    #nur zweiter Treffer-> if len(re.findall("Schweigen im Walde", str(t[index])))==1: 
    
#    if len(re.findall("Württembergische Volksbücher - Sagen und Geschichten|Tropenarzt im Afrikanischen Busch|Tiere in Ketten|Themidor|Sturmzeichen|S. O. S.|Mensch gegen Mensch|Männer in der Nacht|Justizmord?|Alte Kalendergeschichten|Boëtius von Orlamünde|Das bißchen Erde|Der arme Verschwender|Der Fall Clémenceau|Der schweizerische Robinson|Alte Kalendergeschichten|In Knut Arnebergs Haus|Ich - der Augenzeuge|Der Rettungsball|Der Stegreifritter|Der Verführer|Die Dame mit den Kamelien", str(t[index])))==1:
#        print(index) 
        
        
#alle gefundenen Indexe werden aus t gelöscht (manuell (mit dem größten beginnend))       
#del t[index]


#ein Linkdictionary wird erstellt
linkdict={}
#für jeden Eintrag in t
for i in range(len(a)):
    #werden Autor und link extrahiert
    autor=re.findall("/autor/.+>(.+)</a>",str(a[i]))[0] 
    link=re.findall("href=\"(.+)\"", str(t[i]))[0]
    #wenn es für den Autor bereits einen Eintrag gibt, wird der Link diesem hinzugefügt, andernfalls ein neuer Eintrag erstellt
    if autor in linkdict:
        linkdict[autor].append(link)
    else:
        linkdict[autor]=[link]
		
#---- das entstandene link-Dictionary findet sich in helpers als pickle-Objekt linkdict.p

#Funktion, die bei einem gegebenen Romanlink den ganzen Roman extrahiert
def extrakt_roman(link):
    #der Websitelink der ersten Romanseite wird festgelegt
    dir="https://gutenberg.spiegel.de/"+link
    #der Inhalt der Seite extrahiert
    c=requests.get(dir)
    d=c.text
    #ein Html-Objekt angelegt
    temp=BeautifulSoup(d)
    #die Links zu weiterführenden Kapiteln werden ermittelt
    nav=temp.find_all("ul", {"class": "gbnav"})
    #und als liste gespeichert
    dirs=re.findall("href=\"(/buch/[a-zA-z0-9\-\/]*)\">Kapitel", str(nav))
    #der Text der Seite wird gespeichert
    text=temp.find("div", id="gutenb")
    #und von htmltags befreit
    sauber=re.sub("<[a-zA-Z =\"\/0-9]*>", "", str(text))
    #der erste Eintrag aus der Linkliste wird gelöscht
    if len(dirs)>0:
        del dirs[0]
    #Solange sich noch unbesehene Kapitel in der Linkliste befinden
    while len(dirs)>0:
        #wird wie oben vogegangen, um den Text der Seite zu speichern
        dir="https://gutenberg.spiegel.de/"+dirs[0]
        c=requests.get(dir)
        d=c.text
        temp=BeautifulSoup(d)
        text=temp.find("div", id="gutenb")
        #von tags zu befreien
        gereinigt=re.sub("<[a-zA-Z =\"\/0-9]*>", "", str(text))
        #und dem bisher gespeichertem Text hinzuzufügen
        sauber=sauber+gereinigt
        #ein weiterer Eintrag in der Linkliste wird gelöscht
        del dirs[0]
    #der Roman wird zurückgegeben
    return(sauber)


#initialisiere Text-Dictionary
text_dict={}
#initialisier Zähler
count=1
#für jeden Key in der Linksammlung
for key in linkdict:
    #Gib den Fortschritt aus
    print(str(round((count/len(linkdict))*100,2))+" Prozent erreicht")
    #initialisiere internen count
    linkcount=1
    #für jeden Link im zu einem Key
    for link in linkdict[key]:
        #extrahiere den Text
        temp=extrakt_roman(link)
        #und lege einen neuen Lexikoneintrag damit an, oder
        if linkcount==1:
            text_dict[key]=[temp,]
        #ergänze einen bestehenden
        else:
            text_dict[key].append(temp)
    #erhöhe den Zähler
    count=count+1
    #Falls es zu lange geht, breche nach 1000 Fällen ab
    if count==1000:
          print("1000 Fälle wurden analysiert")
          break  
		  
#---------oben gewonnenes Text-Dictionary konnte leider wegen zu viel Speicherplatzverbrauchs
#nicht mit versendet werden. Kann aber am Prüfungstag vorgeführt werden

print("Textdict erstellt")
