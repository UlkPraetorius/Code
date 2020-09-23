#------------helper: Taggertraining
# diese Datei ist nicht zur Ausführung gedacht sondern dient den Prüfern zur Nachvollziehbarkeit des Taggertrainings



#importiere Pakete
import re
import random
import nltk
import pickle

#Lade Trainingsdaten des Tiger-Corpus(Anmerkung: der Tagger wurde in Windows erstellt. Für Linux, den Dateipfad entsprechend ändern)
#Die Trainingsdaten finden sich auf der Webseite des Tigercorpus'
f=open('corpus//tiger_release_july03.export', 'r')
t=f.read()


#Vorprozessierung der Trainingsdaten
#zunächst aufteilen in die einzelnen Sätze mittels der SatzID #BOS
x=re.split("#BOS",t)
tagged_sents=[]
#jeder der Sätze...
for sents in x[1:]:
    sentlist=[]
    #wird an den Absätzen in Wörter aufgeteilt (Im vorgegebenen Datenformat erhielt jedes Wort eine Linie)
    m=re.split('\n',sents)
    #jede ermittelte Wortlinie
    for lines in m:
        #wird an den Tabs nochmals aufgesplittet und....
        k=re.split('\t+',lines)
        #....wenn es sich um ein Wort handelt werden...
        if len(re.findall("^[a-zA-Z]",k[0]))>0:
            #das Wort (in k[0]) und der Tag(k[1]) als Tupel der Satzliste hinzugefügt
            sentlist.append((k[0],k[1]))
    #wenn es sich bei der Satzliste nicht um eine leere Liste handelt...        
    if sentlist != []:
        #...wird die Tupel-Satzliste der Gesamtsatzliste hinzugefügt
        tagged_sents.append(sentlist)
    
#die ermittelten Sätze werden zufällig geordnet
random.shuffle(tagged_sents)
#es wird ermittelt, wie viel 2/3 der Gesamtmenge der Sätze sind, um...
cutoff=int(2*40000/3)
#in trainings- und Testdaten aufzuteilen
train_sents=tagged_sents[:cutoff]
test_sents=tagged_sents[cutoff:]     

#eine Liste mit getaggten Wörtern (wort,tag) wird erstellt
tagged_words=[]
for sentences in tagged_sents:
    for tagged_word in sentences:
        tagged_words.append(tagged_word)   
		
#ein Dictionary mit den Häufigkeiten aller Tags wird erstellt 
tag_count={}
for word,tag in tagged_words:
    if tag in tag_count:
        tag_count[tag]+=1
    else:
        tag_count[tag]=1
		
		
#Aus dem Dictionary wird der Tag mit dem höchsten Vorkommen ermittelt 
max_val=0
max_key=""
for x in tag_count:
    if tag_count[x]>max_val:
        max_val=tag_count[x]
        max_key=x
    elif tag_count[x]==max_val:
        print("Alternative: "+x+": "+str(tag_count[x]))
		
		
#initiieren des Taggers. Der Defaulttagger tagt jedes Wort mit dem häufigsten Tag
default_tagger = nltk.DefaultTagger(max_key)
#der UnigramTagger ermittelt unigramme und ihren wahrscheinlichsten Tag und nutzt den default_tagger als backoff
t1 = nltk.UnigramTagger(train=train_sents, backoff=default_tagger)
#der BigramTagger ermittelt für Wörter den wahrscheinlichsten Tag in Abhängigkeit ihrer direkten Nachbarschaft und nutzt den 
#UnigramTagger als Backoff
t2 = nltk.BigramTagger(train=train_sents, backoff=t1)

##picklen des Taggers
#Ausführung des unten im Kommentar stehenden Codes sollte nicht geschehen, da es den in diesem Paket bestehenden Tagger überschreibt. Er wurde jedoch einmalig ausgeführt um den 
#trainierten Tagger zu picklen
#pickle.dump( t2, open( "t2.p", "wb" ) )

print("Tagger wurde initiiert")