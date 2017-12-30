import json, sys, os, re
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import *

engine = create_engine('sqlite:///app.db', echo=False)
Session = sessionmaker(bind=engine)
Session = sessionmaker()
Session.configure(bind=engine)  # once engine is available
session = Session()

#Available languages
stripTags=" ,.-_?!;()\n"
langs=("DE","EN","ES","EO","RU")
langs2dict={"DEEN":WDictDEEN,"DEES":WDictDEES,"DEEO":WDictDEEO,"DEFR":WDictDEFR,"DEHE":WDictDEHE,"DEJP":WDictDEJP,"DEPL":WDictDEPL,"DERU":WDictDERU,"DEXX":WDictDEXX,"ENDE":WDictENDE,"ENES":WDictENES,"ENEO":WDictENEO,"ENFR":WDictENFR,"ENHE":WDictENHE,"ENJP":WDictENJP,"ENPL":WDictENPL,"ENRU":WDictENRU,"ENXX":WDictENXX,"ESDE":WDictESDE,"ESEN":WDictESEN,"ESEO":WDictESEO,"ESFR":WDictESFR,"ESHE":WDictESHE,"ESJP":WDictESJP,"ESPL":WDictESPL,"ESRU":WDictESRU,"ESXX":WDictESXX,"EODE":WDictEODE,"EOEN":WDictEOEN,"EOES":WDictEOES,"EOFR":WDictEOFR,"EOHE":WDictEOHE,"EOJP":WDictEOJP,"EOPL":WDictEOPL,"EORU":WDictEORU,"EOXX":WDictEOXX,"FRDE":WDictFRDE,"FREN":WDictFREN,"FRES":WDictFRES,"FREO":WDictFREO,"FRHE":WDictFRHE,"FRJP":WDictFRJP,"FRPL":WDictFRPL,"FRRU":WDictFRRU,"FRXX":WDictFRXX,"HEDE":WDictHEDE,"HEEN":WDictHEEN,"HEES":WDictHEES,"HEEO":WDictHEEO,"HEFR":WDictHEFR,"HEJP":WDictHEJP,"HEPL":WDictHEPL,"HERU":WDictHERU,"HEXX":WDictHEXX,"JPDE":WDictJPDE,"JPEN":WDictJPEN,"JPES":WDictJPES,"JPEO":WDictJPEO,"JPFR":WDictJPFR,"JPHE":WDictJPHE,"JPPL":WDictJPPL,"JPRU":WDictJPRU,"JPXX":WDictJPXX,"PLDE":WDictPLDE,"PLEN":WDictPLEN,"PLES":WDictPLES,"PLEO":WDictPLEO,"PLFR":WDictPLFR,"PLHE":WDictPLHE,"PLJP":WDictPLJP,"PLRU":WDictPLRU,"PLXX":WDictPLXX,"RUDE":WDictRUDE,"RUEN":WDictRUEN,"RUES":WDictRUES,"RUEO":WDictRUEO,"RUFR":WDictRUFR,"RUHE":WDictRUHE,"RUJP":WDictRUJP,"RUPL":WDictRUPL,"RUXX":WDictRUXX,}

def insertWord(word, lang_from="XX", lang_to="XX", translation=""):
    if lang_to==lang_from: 
        print("WORD IN DICT FROM LANG X TO LANG X, RETURN WITHOUT DB WORK")
        return 0 
    #get the right table
    TDict=langs2dict[lang_from+lang_to]
    #clean the word, from dirt
    pureWord=word.strip(stripTags).lower()
    #check if its in there
    tr=session.query(TDict).filter(TDict.word==pureWord).one_or_none()
    #add new or update old
    if tr==None: 
        w = TDict(pureWord, json.dumps({"refCnt":1,"w":[]})) #TODO should be generalized by using request.json["lang"]+"XX"
        session.add(w)
        return 1
    else:
        ref=json.loads(tr.json)
        ref["refCnt"]+=1;
        tr.json=json.dumps(ref)
        return 0

def getFirstWord(word,langFROM,langTO):
    Dict=langs2dict[langFROM+langTO]
    word=word.strip(stripTags).lower()
    w=session.query(Dict).filter(Dict.word==word).one_or_none()
    if w==None: 
        return ""
    else:
        words=json.loads(w.json)
        if "w" in words and len(words["w"])>0:
            return words["w"][0]
        else: return ""

def insertText(name,lang,text):
    txt=session.query(Text).filter(Text.name==name).one_or_none()
    if txt!=None: 
        print("Text '",name,"' already added")
        return
    #Adds formated Text
    textJson = str2formatedText(text)
    t = Text(name, lang, json.dumps(textJson))
    session.add(t)

    #Adds dekoded Text
    if(lang!="DE"): testDekode(t,textJson,lang)

    #Adds new words from the example texts
    sum=0
    for par in textJson:
        for w in par:
            if lang=="DE": sum+=insertWord(w,"DE","XX")
            else         : sum+=insertWord(w,lang,"DE")
    session.commit()
    print("Inserted Text",name,"- which added",sum,"new words to",lang)
    return t

def testDekode(txt,text,lang):
    autotext=[]
    abs=sum=0
    for par in text:
        auto = {}
        for t in par:
            auto[t]={"w":getFirstWord(t,lang,"DE")}
            if auto[t]!="": sum+=1
            abs+=1
        autotext.append(auto)

    t = Dekoded(json.dumps(autotext),"DE",txt.id)
    session.add(t)
    session.commit()
    print("Inserted Dekoded Text for",txt.name,"- which autodekoded",sum,"/",abs,"=",(100*sum)//abs, "%")

def insertDekodedText():
    pass

def getParagraphs(text):
    return [p for p in re.split("\n\n",re.sub(r"\n\n\n+", "\n\n", text)) if p!=None and p.replace(" ","")!='']
def getWords(text):
    return [[w for w in re.split("(  )|\n",re.sub(r"   +", "  ", p)) if w!=None and w.replace(" ","")!=''] for p in getParagraphs(text)]
def str2formatedText(text):
    return [[w for w in re.split("(  )|\n",re.sub(r" +", "  ", p)) if w!=None and w.replace(" ","")!=''] for p in getParagraphs(text)]

if __name__=="__main__":
    for root, dirs, files in os.walk("../static1000/txt"):
        for file in files:
            if file.endswith(".txt"):
                p=root.split("/")
                f=os.path.join(root, file)
                text=open(f).read()
                t=insertText(p[-1]+" - "+file.replace(".txt",""),p[-2],text)