#---------------------------------------------
#Autorerkennung.py
#---------------------------------------------
#Ein Programm, das nach Ausführung über die Kommandozeile einen Pfad zu einem Text erfragt, der mit einer -ebenfalls über die Kommandozeile selbst festlegbaren oder zufälligen Auswahl 
#an Autoren verglichen werden kann. (Für eine gute Treffgenauigkeit empfiehlt sich eine Auswahl von 5-8 Autoren)
#Im via author_dict = pickle.load( open( "author_dict.p", "rb" ) importierbaren Dictionary befinden sich 736 Autorsignaturen, die aus der deutschen Version von Projekt Gutenberg 
#extrahiert wurden. Der Code für die Ermittlung dieser Autorsignaturen findet sich zur Nachvollziehbarkeit in Crawler.py und Dict_initiator.py sowie ein dictioanry mit allen 
# extrahierten Texten (text_dict.p) im Ordner helpers.
#(Anmerkung zur Textquelle: Das in der Aufgabenstellung vorgeschlagene gutenberg.org hat wegen eines Rechtsstreits seine Dienste für alle deutsche IPs gesperrt, weshalb auf das deutsche Projekt ausgewichen wurde) 
#Zusätzlich zu den in der Aufgabenstellung vorgeschlagenen Signaturparametern DWL, DSL, DSS, HLR und TTR wird von der Kommandozeile abgefragt, ob man außerdem die 
#DLR(Ratio der nur zweimal vorkommenden Wörter), TLR(Ratio der 3 Mal vorkommenden Wörter) oder POS-Ratio(Vorkommen der einzelnen Wortarten) als Parameter mit einbeziehen möchte
# Für das bestimmen der POS-Tags wird der vortrainierte POS-Tagger via tagger=pickle.load(open("t2.p","rb")) geladen. Der Code für das Training des POS-Taggers findet sich in Tagger.py 
#im Ordner helpers.
#


import os
#import sys
import re
import pickle
#import nltk
#import requests
#from bs4 import BeautifulSoup
import random





#---------------------------------------------------------------------------------------------------
# Hilfsmittelfunktionen
#---------------------------------------------------------------------------------------------------

#funktion, die einen Text entgegennimmt und eine Wortliste zurückgibt
def get_words(text):
    #trennt Text an Leer- oder Satzzeichen
    temp=re.split("[,.!?]? ",text)
    #gibt Wortliste zurück
    return(temp)
	
#Funktion, die einen Text entgegennimmt und eine Satzliste zurückgibt
def get_sents(text):
    #Trennt Text an Punkt, Fragezeichen oder Ausrufezeichen
    temp=re.split("[!?.] ",text)
    #Gibt Satzliste zurück
    return(temp)
	
#Funktion, die einen Text entgegennimmt und die Anzahl der Satzteile zurückgibt	
def get_sent_parts(sentence):
    #Trennt Text an Komma, Semikolon oder Doppelpunkt
    temp=re.split("[,;:]", sentence)
    #Gibt Satzteilanzahl zurück
    return(len(temp))
	
	
#Funktion, die eine Wortliste entgegennimmt und ein Wörterbuch mit Worthäufigkeiten zurückgibt
def word_count(wordlist):
    #initiiere Wort-Dictionary
    worddict={}
    #für jedes Wort in der Wortliste...
    for i in wordlist:
        #wenn das Wort bereits im Wort-Dictionary angelegt ist, erhöhe den Zähler um 1
        if i.lower() in worddict:
            worddict[i.lower()]+=1
        #andernfalls lege einen neuen Eintrag dafür an (mit Zähler auf 1)
        else:
            worddict[i.lower()]=1
    #Gib das Wörterbuch mit Wortanzahlen zurück
    return(worddict)

#--------------------------------------------------------------------------------
#Funktionen zur Ermittlung der Signaturparameter	
#--------------------------------------------------------------------------------
	
#Funktion, die eine Wortliste entgegennimmt und die durschnittliche Wortlänge daraus berechnet
def get_DWL(wordlist):
    #initiiere Summe der Wortlängen
    temp_sum=0
    #iteriere durch die Wortliste
    for i in wordlist:
        #Addiere jede Wortlänge auf die Gesamtwortlänge
        temp_sum+=len(i)
    #Gib die Gesamtwortlänge geteilt durch die Wortanzahl zurück
    return(temp_sum/len(wordlist))
	
	
#Funktion, die eine Satzliste entgegennimmt und die durschnittliche Satzlänge ermittelt        
def get_DSL(sent_list):
    #Ermittle für jeden Satz i die Anzahl der Wörter und speichere diese in einer Liste
    num_words=[len(get_words(i)) for i in sent_list]
    #Gib die Gesamtsumme aller Wörter geteilt durch die Satzanzahl zurück
    return(sum(num_words)/len(sent_list))	
	
#Funktion, die eine Satzliste entgegennimmt und die durchschnittliche Satzteilmenge zurückgibt
def get_DSS(sent_list):
    #Ermittle für jeden Satz die Satzteile und speichere alles in einer Liste
    num_parts=[get_sent_parts(i) for i in sent_list]
    #Gib die Summe der Satzteile durch die Gesamtzahl der Sätze zurück
    return(sum(num_parts)/len(sent_list))


#Funktion, das worddict und die Wortliste eines Textes entgegennimmt und die Type-Token-Ratio ermittelt
def get_TTR(worddict,wordlist):
    #gib die Anzahl Types (Anzahl der Einträge im Lexikon) durch die Anzahl der Token(Anzahl der Einträge in der Wortliste)zurück
    return(len(worddict)/len(wordlist))

#Funktion, die ein Wortdict und optional die Information, welche Vorkommenshäufigkeit n (default=1) gesucht wird entgegen
#nimmt und das Verhältnis zwischen Hapaxen und Gesamtmenge der Types zurückgibt
def get_HLR(worddict, n=1):
    #initiiere Zähler
    j=0
    #für jeden Eintrag im Wörterbuch
    for i in worddict:
        #wird überprüft, ob es sich um ein Hapax handelt
        if worddict[i]==n:
            #und, falls zutreffend, der Zähler erhöht
            j+=1
    #zurückgegeben wird die Anzahl der Hapaxe geteilt durch die Anzahl der Token        
    return(j/len(worddict))
	
#Funktion, die die Wortliste eines Textes entgegen nimmt und die relative Häufigkeit der vorkommenden Wortformen ermittelt
def count_tags(word_list):
    #tagge die Wörter der Wortliste
    tagged=tagger.tag(word_list)
    #initiiere Postag-Liste
    Pos_tags={"ADJA":0, "ADJD":0, "ADV":0, "APPR":0, "APPRART":0, "APPO":0, "APZR":0, "ART":0, "CARD":0, "FM":0, "ITJ":0, "KOUI":0, "KOUS":0, "KON":0, "KOKOM":0, "NN":0,"NNE":0, "NE":0, "HSV":0, "PDS":0, "PDAT":0, "PIS":0, "PIAT":0, "PIDAT":0, "PPER":0, "PPOSS":0, "PPOSAT":0, "PRELS":0, "PRELAT":0, "PRF":0, "PROAV":0, "PWS":0, "PWAT":0, "PWAV":0, "PAV":0, "PTKZU":0, "PTKVZ":0, "PTKANT":0, "PTKA":0,"PTKNEG":0, "SGML":0, "SPELL":0, "TRUNC":0, "VVFIN":0, "VVIMP":0, "VVINF":0, "VVIZU":0, "VVPP":0, "VAFIN":0, "VAIMP":0, "VAINF":0, "VAPP":0, "VMFIN":0, "VMINF":0, "VMPP":0, "XY":0}
    #zähle die Tags
    for word,tag in tagged:
        Pos_tags[tag]+=1
    #speichere die relative Häufigkeit jedes Pos-Tags in einer Liste
    norm_vec=[round(Pos_tags[key]/len(word_list),2) for key in Pos_tags]
       #Gib die postag-Liste zurück
    return(norm_vec)	
	
#------------------------------------------------------------------------------------------------------
#Funktionen zur Ermittlung der Autorähnlichkeit
#------------------------------------------------------------------------------------------------------

#Funktion, die für einen Text die Signatur ermittelt 
#Standardmäßig werden hierbei DWL TTR, HLR, DSL und DSS ermittelt
#Optional kann auch die dislegomenon-ratio(DLR=True), trislegomenon-ratio(TLR=True), die Vorkommenshäufigkeiten 
#der Wortarten (POS=True), oder die Vorkommenshäufigkeiten der Satzzeichen (signs=True) mitermittelt werden

def get_signature(text,DLR=False, TLR=False, POS=False):
    #Tokenisiere den Text
    textwords=get_words(text)
    #Teile den Text in Sätze auf
    textsents=get_sents(text)
    #Erstelle das Wortdictionary
    textdict=word_count(textwords)
    #Ermittle die Defaultsignatur mit DWL, TTR, HLR, DSL und DSS
    signature=[round(get_DWL(textwords),2), round(get_TTR(textdict, textwords),2), round(get_HLR(textdict),2), round(get_DSL(textsents),2), round(get_DSS(textsents),2)]
    #wenn so gemünscht ermittle die DLR
    if DLR==True:
        signature.append(round(get_HLR(textdict, n=2),2))
    #Wenn angegeben, ermittle TLR und hänge sie an die Signatureliste an
    if TLR==True:
        signature.append(round(get_HLR(textdict, n=3),2))
    #Wenn angegeben, ermittle POS-Verhältnisse und hänge sie an die Signatur an
    if POS==True:
        for i in count_tags(textwords):
            signature.append(i)
    #gib die Signatur zurück
    return(signature)

	
#Vergleiche zwei Signaturen (als Eingabe) und ermittle die Autorähnlichkeit
def get_author_similarity(sigI, sigII, DLR=False, TLR=False, POS=False):
    #lege die Gewichtungen fest
    weights=[5,5,5,5,150]
    #ergänze weights hinsichtlich der optionalen Angaben
    if DLR==True:
        weights.append(50)
    if TLR==True:
        weights.append(50)
    if POS==True:
        for i in range(56):
            weights.append(0.5)
    #Berechne das Ähnlichkeitsmaß
    dif=sum([abs(sigI[i]-sigII[i])*weights[i] for i in range(len(sigI))])
    #Gib das Ähnlichkeitsmaß zurück
    return(round(dif,2))
	
	
def find_author(text,DLR=False, TLR=False, POS=False):
    
    #ermittle Signatur für eingegebenen Text
    b=get_signature(text, DLR=DLR, TLR=TLR, POS=POS)
    #initiiere Dictionary und Liste
    dif_dict={}
    dif_list=[]
    #loope durch das Autoren-Dictionary
    for i in authordict:
        #und ermittle die Autorsignatur in Abhängigkeit der optionalen Angaben
        authorsig=authordict[i][:5]
        if DLR==True:
            authorsig.append(authordict[i][5])
        if TLR==True:
            authorsig.append(authordict[i][6])
        if POS==True:
            for index in range(7,63):
                authorsig.append(authordict[i][index])
        #ermittle das Ähnlichkeitsmaß
        p=get_author_similarity(b, authorsig,DLR=DLR, TLR=TLR, POS=POS)
        #speichere das Ähnlichkeitmaß als key im Dictionary mit dem Autornamen als Value und einzeln in der dif_liste
        if str(p) not in dif_dict:
            dif_dict[str(p)]=i
            dif_list.append(p)
    #ermittle den Autor, mit dem niedrigsten Ähnlichkeitsmaß, indem der kleinste Wert der dif_liste ins dic_dict eingesetzt wird
    author=dif_dict[str(min(dif_list))]
    #Gib Autor zurück
    return(author)
            
##----------------------------------------------------------------------------------------------------            
#Hauptprogramm
#------------------------------------------------------------------------------------------------------
def check_input(string):
	legal=["y","n"]
	if string in legal:
		return(True)
	else:
		return(False)
#lade Signatur		
author_dict = pickle.load( open( "author_dict.p", "rb" ) )
#Initiiere Keyliste
keylist=[]

#Erfrage Pfad des untersuchten Textes
path=input("Bitte gib den Pfad deines Textes an ")

#Überprüfe, ob Pfad existiert, wenn nicht frage erneut danach
while os.path.isfile(path) != True:
	path=input("File existiert nicht. Bitte gib einen korrekten Pfad an. ")
	
#Öffne Datei

c=open(path, "r")
text=c.read()

#Frage optionale Paramater ab	
#Frage ob dl als Parameter aufgenommen werden soll	
dl=input("Willst du Dislegomenonratio mit untersuchen?(y/n) ")
#frage erneut bei falscher Eingabe
while check_input(dl) != True:
	dl=input("Bitte gib y oder n an ")

#werte y und n in Boolsche Variablen aus
if dl=="y":
	DLR=True
else:
	DLR=False

#Frage ob tl als Parameter aufgenommen werden soll	
tl=input("Willst du Trislegomenonratio mit untersuchen?(y/n) ")
#frage erneut bei falscher Eingabe
while check_input(tl) != True:
	tl=input("Bitte gib y oder n an ")

#werte y und n in Boolsche Variablen aus
if tl=="y":
	TLR=True
else:
	TLR=False
	
#Frage ob POS als Parameter aufgenommen werden soll		
pos=input("Willst du POS-Tag-Ratio mit untersuchen?(y/n) ")
#frage erneut bei falscher Eingabe
while check_input(pos) != True:
	pos=input("Bitte gib y oder n an ")
#Werte y und n in Boolsche Variablen aus und lade den Tagger falls gewünscht
if pos=="y":
	tagger=pickle.load(open("t2.p","rb"))
	POS=True
else:
	POS=False

#Frage die Auswahl der Vergleichsautoren ab	
zufaellig=input("Möchtest du eine zufällige Autorauswahl?(y/n) ")
#bei inkorrekter Eingabe frage erneut
while check_input(zufaellig) != True:
	zufaellig=input("Bitte gib y oder n an ")
#wenn zufällig, frage wie viele Autoren als Vergleichsautoren gewählt werden sollen und extrahiere sie aus einer randomisierten Liste aller Schlüssel des Autorendictionaries
if zufaellig=="y":
	size=int(input("Wie viele Autoren möchtest du vergleichen?(2-736) "))
	keylist=[key for key in author_dict]
	random.shuffle(keylist)
	keylist=keylist[:size]
#wenn nicht zufällig
if zufaellig=="n":
	#initiiere counter, um Abfrage bei zu vielen inkorrekten Eingaben abzubrechen
	count=0
	#frage Autor ab
	auswahl=input("Welchen Autor willst du vergleichen? ")
	
	#Überprüfe, ob Autor verfügbar
	if auswahl in author_dict:
		#und füge ihn der key-liste hinzu
		keylist.append(auswahl)
	#Falls nicht verfügbar, teile dies mit und erhöhe den counter um 1
	else:
		print("Autor nicht verfügbar")
		count=count+1
	#Frage weitere Autoren ab
	while input("Weiterer Autor?(y/n) ")=="y" and count<10:
		auswahl=input("Welchen Autor willst du vergleichen? ")
	
		if auswahl in author_dict:
			keylist.append(auswahl)
		else:
			print("Autor nicht verfügbar")
			count=count+1
#Wenn die Autorenliste zu klein ist, lasse sie um eine zufällige Anzahl ergänzen 			
if len(keylist)<2:			
	size=int(input("Aktuell sind/ist "+str(len(keylist))+" Autor(en) auf deiner Liste. Um wie viele zufällige Autoren möchtest du sie ergänzen?(2-"+str(len(author_dict)-len(keylist))+") "))
	#überprüfe, die Größenangabe der Ergänzungen
	while size<1:
		size=int(input("Angabe zu niedrig. Bitte wähle eine größere Zahl an Ergänzungen "))
	while size>len(author_dict)-1:
		size=int(input("Angabe zu hoch. Bitte wähle eine kleinere Zahl an Ergänzungen "))
	#erstelle eine (neue) keyliste
	keys=[key for key in author_dict]
	random.shuffle(keys)
	#initiiere count um den Loop abzubrechen, wenn size erreich ist
	count=0
	#iteriere durch die keys und füge keys, die noch nicht in der Keyliste sind hinzu, bis size erreich wurde
	for key in keys:
		if count==size:
			break
		if key not in keylist:
			keylist.append(key)
			count=count+1
			
#Initiiere das gewünschte Autordictionary

authordict={}
for key in keylist:
    authordict[key]=author_dict[key]

author=find_author(text,DLR=DLR, TLR=TLR, POS=POS)	
	
print("Der gesuchte Autor ist "+author)	




#--------------------------------------------------------------------------------------------------------------------------------------------------------

#Anwendungsbeispiel: (Vergleich des test.txt (Effi Briest von Theodor Fontane) mit einer zufälligen Auswahl an zwei Autoren + Theodor Fontane)
#python Autorerkennung.py
#Bitte gib den Pfad deines Textes an test.txt
#Willst du Dislegomenonratio mit untersuchen?(y/n) y
#Willst du Trislegomenonratio mit untersuchen?(y/n) y
#Willst du POS-Tag-Ratio mit untersuchen?(y/n) y
#Möchtest du eine zufällige Autorauswahl?(y/n) n
#Welchen Autor willst du vergleichen? Theodor Fontane
#Weiterer Autor?(y/n) n
#Aktuell sind 1 Autoren auf deiner Liste. Um wie viele zufällige Autoren möchtest du sie ergänzen?(2-735) 5
#Der gesuchte Autor ist Theodor Fontane



	