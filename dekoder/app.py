# app.py or app/__init__.py

# version 0.3 changed by JK 
import json
from sqlalchemy.exc import IntegrityError
from flask import Flask, render_template, request, flash
from flask_cache import Cache
from flask_login import login_required, current_user
from flask_assets import Bundle, Environment
from flask_sqlalchemy import SQLAlchemy, declarative_base
from jsonschema import validate, ValidationError

from .schemas import format_schema
from .models import *

app = Flask(__name__)   
app.config.from_pyfile('config.py')
cache = Cache(app,config={'CACHE_TYPE': 'simple'})
bundles = {
	'home_js': Bundle(
		'bower_components/jquery/dist/jquery.min.js',
		'bower_components/materialize/dist/js/materialize.min.js',
        'bower_components/audiojs/audiojs/audio.min.js',
        'js/dekoder.js',
		output='gen/home.js', filters='jsmin'
	),
	'home_css': Bundle(
		'bower_components/materialize/dist/css/materialize.min.css',
        'css/dekoder.css',
        'css/icon.css',
		output='gen/home.css' ,filters='cssmin'
	),
}

#Available languages
langs=("DE","EN","ES","EO","RU","HE")
langs2dict={"DEXX":WDictDEXX,"DEEN":WDictDEEN,"DEES":WDictDEES,"DEEO":WDictDEEO,"DERU":WDictDERU, "DEHE":WDictDEHE,
            "XXDE":WDictXXDE,"ENDE":WDictENDE,"ESDE":WDictESDE,"EODE":WDictEODE,"RUDE":WDictRUDE, "HEDE":WDictHEDE}
            
text_beginning_len = 30
assets = Environment(app)
assets.register(bundles)

# initialize and create the database
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    ###return render_template("index.html", langs=langs)
    return render_template("format.html", langs=langs)
	

#############FORMAT
# get:  *lets you enter a text with visual preview of the simple markup to convert text to an array of composed of single word units
# post: * saves the entered markup as json with language and name of the text
#       * checks all entered words, if they already exist in the base database and adds them otherwise
@app.route('/format', methods=['GET', 'POST'])
def format():
    if request.method == 'POST':
        try:  
            #check if valid POST
            if not request.json["lang"]:
                return json.dumps({"success":False,'message':"Add language to the submitted text"}), 200, {'ContentType':'application/json'} 
            if not request.json["name"] or request.json["name"]=="":
                return json.dumps({"success":False,'message':"Add name to the submitted text"}), 200, {'ContentType':'application/json'} 
            validate(request.json, format_schema)
            #ass formated text
            text = Text(request.json["name"], request.json["lang"], json.dumps(request.json["json"]))
            db.session.add(text)
            db.session.commit()
            # add all new words to the source langs table
            newW=0 #cnts the number of new words
            #counts up the references of the word or adds a new word to the lang specific dict
            for par in request.json["json"]:
                if request.json["lang"]=="DE": TDict=WDictDEXX;
                else :                         TDict=WDictXXDE;
                for w in par:
                    pureWord=w.strip(" ,.\n").lower()
                    tr=db.session.query(TDict).filter(TDict.word==pureWord).one_or_none()
                    #print(w)
                    if tr==None: 
                        newW+=1
                        w = TDict(pureWord, json.dumps({"refCnt":1,"w":[pureWord], "lang":[]})) #TODO should be generalized by using request.json["lang"]+"XX"
                        db.session.add(w)
                    else:
                        ref=json.loads(tr.json)
                        ref["refCnt"]+=1;
                        tr.json=json.dumps(ref)
            db.session.commit()
            
            return json.dumps({'message':"Formated text was succesfully saved! "+str(newW)+" new Words added..."}), 200, {'ContentType':'application/json'} 
        except ValidationError:
            return json.dumps({'message':"No valid text format submitted..."}), 200, {'ContentType':'application/json'}
        except IntegrityError as e:
            return json.dumps({"success":False,'message':"Formated text with given name already taken. Choose another name..."}), 200, {'ContentType':'application/json'}
        except Exception as e:
            return json.dumps({"success":False,'message':"Other:"+str(e)}), 200, {'ContentType':'application/json'} 

    else:
        return render_template("format.html", langs=langs)

############DEKODE
# shows you all the formated texts and lets you chose a language to dekode them to
@app.route('/dekode')
def dekode():
    texts = Text.query.all()
    for txt in texts: 
        short_txt = getTextBeginning(txt)
        txt.json = short_txt
   
    return render_template("getFormatedTexts.html", t=texts, langs=langs)

# shows you all the languages to dekode a text to
@app.route('/dekode/<string:textname>')
def dekodeText(textname):
    texts = db.session.query(Text).filter(Text.name==textname)
    for txt in texts:
        short_txt = getTextBeginning(txt)
        txt.json = short_txt
        
    return render_template("getFormatedTexts.html", langs=langs, t=texts)

# get:  * shows you the formated text and lets you add a dekodation to each word unit
#       * autocompletes by showing existing translations from former entries in the database
# post: * saves the dekoded text with all the translations entered
@app.route('/dekode/<string:textname>/<string:lang>', methods=['GET', 'POST'])
def dekodeTextLang(textname,lang):
   
    # read original text from database for determinate source language
    txt = db.session.query(Text).filter(Text.name==textname).one()#.filter(Text.name == textname).one()#query(Text).filter(Text.name == textname).first()
    
    
    
    FROMlang = txt.lang
    TOlang = lang
    dictLangKey = FROMlang+TOlang
    TDictDekoded=langs2dict[dictLangKey]
    
    # if POST: save translated words
    if request.method == 'POST':
        for par in request.json["json"]:
            #print ("par: " + str(par))
            for orgWord in par:
                #print ("orgWord: "+orgWord.encode('utf-8') )
                if 'w' in par[orgWord]:
                    if par[orgWord]['w'] != None:
                        dekodedWord = par[orgWord]['w']
                        #print (dekodedWord.encode('utf-8') )
                        # add to language table
                        tr=db.session.query(TDictDekoded).filter(TDictDekoded.word==orgWord).one_or_none()
                        if tr==None: 
                            #print ("Word " + orgWord.encode('utf-8') + " is not found in Table " + dictLangKey )
                            w = TDictDekoded(orgWord, json.dumps({"w":[dekodedWord]}))
                            db.session.add(w)
                        else:
                            pass
                            #print ("Word " + orgWord.encode('utf-8') + " FOUND in Table " + dictLangKey )
                        
                        # update languages list in text Table
                        if FROMlang =="DE": 
                            TDict=WDictDEXX
                        else : 
                            TDict=WDictXXDE
                        tr=db.session.query(TDict).filter(TDict.word==orgWord.strip(" ,.\n").lower()).one_or_none()
                        if tr != None:
                            ref=json.loads(tr.json)
                            if not TOlang in ref["lang"]:
                                ref["lang"].append(TOlang);
                                tr.json=json.dumps(ref)
                            
                        
    
        db.session.commit()
        
     
    # get words from text ( with autocomplete with translated items )
    autotext=[]
    for par in json.loads(txt.json):
        auto = {}
        for t in par:
            #print (t)
            
            tr=db.session.query(TDictDekoded).filter(TDictDekoded.word==t).one_or_none()
            if tr==None: auto[t]={}
            else       : auto[t]=json.loads(tr.json)
        autotext.append(auto)
        
    #print (autotext)
    
    text = {"name":txt.name,"FROMlang":txt.lang,"TOlang":lang,"json":autotext}
    p = { "p":len(text), "pars": [len(par) for par in text] }
    return render_template("dekode.html", langs=langs, t=text, parWArr=str(p))
    
# builds a whole text from json 
def Json2Text(txt):
    res = ""  
    for par in json.loads(txt.json):
        res += ' '.join('%s' %t for t in par)
        
    return res        

# cuts text to text_beginning_len lenght
def getTextBeginning(json):
    txt = Json2Text(json)  
    txt = (txt[:text_beginning_len] + '..') if len(txt) > text_beginning_len else txt
    
    return txt
    
    
    
    
############READ
# lets you read all the dekoded texts to practise your target language ^^

# shows you all dekoded text
@app.route('/read', methods=['GET', 'POST'])
def read():
    dekoded_texts = Text.query.all()
    for txt in dekoded_texts:
        #check if this text is translated TODO
        txt.json = Json2Text(txt)
    return render_template("readText.html",  t=dekoded_texts, langs=langs)
    

#shows you all languages a text is dekoded to
@app.route('/read/<string:textname>', methods=['GET'])
def readText():
    pass

# converts on dekodation of a text into a pdf for print
@app.route('/read/<string:textname>_<string:lang>.pdf', methods=['GET'])
def readTextPDF():
    pass

# shows you a dekoded text in one target language
@app.route('/read/<string:textname>/<string:lang>', methods=['GET'])
def readTextLang(textname,lang):
    # read original text from database 
    org_text = db.session.query(Text).filter(Text.name==textname).one()
    if org_text != None:
        
        dekoded_text = Text(textname, lang, "")
        
        FROMlang = org_text.lang
        TOlang = lang
        dictLangKey = FROMlang+TOlang
        
        TDictDekoded=langs2dict[dictLangKey]
        
        dekodedtext=""
        for par in json.loads(org_text.json):
            for t in par:
                tr=db.session.query(TDictDekoded).filter(TDictDekoded.word==t).one_or_none()
                if tr != None:
                    ref=json.loads(tr.json)
                    for v in ref["w"]:
                        dekodedtext += v + " " 
                    print (dekodedtext.encode('utf-8') )
                
            
        dekoded_text = Text(textname, lang, dekodedtext)
        org_text = Json2Text(org_text)

    return render_template("readTextLang.html",  org_t=org_text, dekoded_t=dekodedtext)
	

app.secret_key = 'super secret key'
if __name__=="__main__":
    app.run(debug=True)