import json,sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

sys.path.insert(0, "../dekoder/dekoder")
sys.path.insert(0, "dest")
from models import *

langs2dict={"DEXX":WDictDEXX,"DEEN":WDictDEEN,"DEES":WDictDEES,"DEEO":WDictDEEO,"DERU":WDictDERU,
            "XXDE":WDictXXDE,"ENDE":WDictENDE,"ESDE":WDictESDE,"EODE":WDictEODE,"RUDE":WDictRUDE}

engine = create_engine('sqlite:///dekoder/app.db', echo=False)

Session = sessionmaker(bind=engine)
Session = sessionmaker()
Session.configure(bind=engine)  # once engine is available
session = Session()


def addWDict(wrd,trans,lang):
    TDict=langs2dict[lang]
    tr=session.query(TDict).filter(TDict.word==wrd).one_or_none()
    #add new or update old
    if tr==None: 
        word = langs2dict[lang](wrd, json.dumps({"w":trans,"refCnt":0}))
        session.add(word)

def addCSV(lang,file):
    last=""
    wrd=0
    for pair in open(file).readlines():
        if not "\t" in pair: print(pair,"notab!!!");continue
        word,transString= pair.strip("\n").split("\t",1)
        word=word.strip(" .?!;-_()\n").lower()
        if last==word: 
            #print(last,":",pair) 
            continue
        translations = [s.strip(" .?!;-_()\n").lower() for s in transString.split(",")]
        if len(translations)>0 and translations!=[""]:
            addWDict(word,translations,lang)
            last=word
            wrd+=1
    session.commit()
    return wrd

print("Added",addCSV("RUDE","static1000/dest/rude.txt"),"russian words to db")
print("Added",addCSV("ESDE","static1000/dest/esde.txt"),"spanish words to db")
print("Added",addCSV("EODE","static1000/dest/eode.txt"),"esperanto words to db")