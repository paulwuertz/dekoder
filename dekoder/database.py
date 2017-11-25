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
langs=("DE","EN","ES","EO","RU")
langs2dict={"DEXX":WDictDEXX,"DEEN":WDictDEEN,"DEES":WDictDEES,"DEEO":WDictDEEO,"DERU":WDictDERU,
            "XXDE":WDictXXDE,"ENDE":WDictENDE,"ESDE":WDictESDE,"EODE":WDictEODE,"RUDE":WDictRUDE}

def insertWord(word, lang_from="XX", lang_to="XX", translation=""):
    if lang_to==lang_from: 
        print("WORD IN DICT FROM LANG X TO LANG X, RETURN WITHOUT DB WORK")
        return 0 
    #get the right table
    TDict=langs2dict[lang_from+lang_to]
    #clean the word, from dirt
    pureWord=word.strip(" ,.?!;-_()\n").lower()
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

def insertFormatedText(name,lang,text):
    txt=session.query(Text).filter(Text.name==name).one_or_none()
    if txt!=None: 
        print("Text '",name,"' already added")
        return
    textJson = str2formatedText(text)
    t = Text(name, lang, json.dumps(textJson))
    session.add(t)

    sum=0
    for par in textJson:
        for w in par:
            if lang=="DE": sum+=insertWord(w,"DE","XX")
            else         : sum+=insertWord(w,lang,"DE")
            #print(w.strip(" ,.?!;-_()\n").lower())
    session.commit()
    print("Inserted Text",name,"- which added",sum,"new words to",lang)

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
                insertFormatedText(p[-1]+" - "+file.replace(".txt",""),p[-2],text)