#------------Dictinitiator
# Diese Datei ist nicht zum Ausführen gedacht. Sie soll die Ermittlung des Signaturendictionarys author_dict veranschaulichen
# sie nutzt einige Komponenten des Hauptprogramms


##laden der Pakete
import re
import pickle
import nltk

#laden des Text-Lexikons
#Achtung Pfade nach Windoskonventionen. Müssen in Linux nochmals verändert werden
text_dict = pickle.load( open( "text_dict.p", "rb" ) )
tagger=pickle.load(open("./../t2.p","rb"))



#Z.19-Z.131 sind Bestandteile des Hauptprogramms. Sie finden sich auch in Autorerkennung.py
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

def get_sent_parts(sentence):
    #Trennt Text an Komma, Semikolon oder Doppelpunkt
    temp=re.split("[,;:]", sentence)
    #Gibt Satzteilliste zurück
    return(len(temp))
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
	
	
###Neuer Code
	
#initiiere Autordictionary
author_dict={}
#initiiere count
count=0
#für jeden Eintrag im Text-Dictionary werden alle Texte zu einem zusammengefügt und die Autorsignatur ermittelt. Diese wird im Autordict gespeichert. Außerdem 
#wird ein Zähler erhöht und abgebrochen, wenn dieser zu hoch ist. 
for key in text_dict:
	
    count=count+1
	#gib den Fortschritt aus
    print("Fortschritt: "+str(count)+" von "+str(len(text_dict)))
    texte=""
    for text in text_dict[key]:
        texte=texte+text
    author_dict[key]=get_signature(texte,DLR=True, TLR=True, POS=True )
	
#das gewonnene Autorendictionary findet sich als pickle-Objekt author_dict.p im Ordner des Abschlussprojekts

print("Das Autorenlexikon wurde erstellt")
