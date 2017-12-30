# app.py or app/__init__.py

# version 0.3 changed by JK 
import json, pprint
from sqlalchemy.exc import IntegrityError
from flask import Flask, render_template, request, flash
from flask_cache import Cache
from flask_login import login_required, current_user
from flask_assets import Bundle, Environment
from flask_sqlalchemy import SQLAlchemy, declarative_base
from jsonschema import validate, ValidationError

from .schemas import format_schema
from .models import *
from .helpers import *

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
langs=("DE","EN","ES","EO","FR","HE","JP","PL","RU")
langs2dict={"DEEN":WDictDEEN,"DEES":WDictDEES,"DEEO":WDictDEEO,"DEFR":WDictDEFR,"DEHE":WDictDEHE,"DEJP":WDictDEJP,"DEPL":WDictDEPL,"DERU":WDictDERU,"DEXX":WDictDEXX,"ENDE":WDictENDE,"ENES":WDictENES,"ENEO":WDictENEO,"ENFR":WDictENFR,"ENHE":WDictENHE,"ENJP":WDictENJP,"ENPL":WDictENPL,"ENRU":WDictENRU,"ENXX":WDictENXX,"ESDE":WDictESDE,"ESEN":WDictESEN,"ESEO":WDictESEO,"ESFR":WDictESFR,"ESHE":WDictESHE,"ESJP":WDictESJP,"ESPL":WDictESPL,"ESRU":WDictESRU,"ESXX":WDictESXX,"EODE":WDictEODE,"EOEN":WDictEOEN,"EOES":WDictEOES,"EOFR":WDictEOFR,"EOHE":WDictEOHE,"EOJP":WDictEOJP,"EOPL":WDictEOPL,"EORU":WDictEORU,"EOXX":WDictEOXX,"FRDE":WDictFRDE,"FREN":WDictFREN,"FRES":WDictFRES,"FREO":WDictFREO,"FRHE":WDictFRHE,"FRJP":WDictFRJP,"FRPL":WDictFRPL,"FRRU":WDictFRRU,"FRXX":WDictFRXX,"HEDE":WDictHEDE,"HEEN":WDictHEEN,"HEES":WDictHEES,"HEEO":WDictHEEO,"HEFR":WDictHEFR,"HEJP":WDictHEJP,"HEPL":WDictHEPL,"HERU":WDictHERU,"HEXX":WDictHEXX,"JPDE":WDictJPDE,"JPEN":WDictJPEN,"JPES":WDictJPES,"JPEO":WDictJPEO,"JPFR":WDictJPFR,"JPHE":WDictJPHE,"JPPL":WDictJPPL,"JPRU":WDictJPRU,"JPXX":WDictJPXX,"PLDE":WDictPLDE,"PLEN":WDictPLEN,"PLES":WDictPLES,"PLEO":WDictPLEO,"PLFR":WDictPLFR,"PLHE":WDictPLHE,"PLJP":WDictPLJP,"PLRU":WDictPLRU,"PLXX":WDictPLXX,"RUDE":WDictRUDE,"RUEN":WDictRUEN,"RUES":WDictRUES,"RUEO":WDictRUEO,"RUFR":WDictRUFR,"RUHE":WDictRUHE,"RUJP":WDictRUJP,"RUPL":WDictRUPL,"RUXX":WDictRUXX,}
          
text_beginning_len = 30
pp = pprint.PrettyPrinter(indent=4)
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
# get:  * lets you enter a text with visual preview of the simple markup to convert text to an array of composed of single word units
# post: * saves the entered markup as json with language and name of the text
#       * checks all entered words, if they already exist in the base database and adds them otherwise
@app.route('/format', methods=['GET', 'POST'])
def format():
    if request.method == 'GET':
        return render_template("format.html", langs=langs)
    
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
                TDict=dict2lang[request.json["lang"]+"XX"];
                for w in par:
                    pureWord=w.strip(striptTags).lower()
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
    txt = db.session.query(Text).filter(Text.name==textname).one()
    
    FROMlang = txt.lang
    TOlang = lang
    dictLangKey = FROMlang+TOlang
    TDictDekoded=langs2dict[dictLangKey]
    
    # get words from text and fetch the autocomplete translations
    # for the items to be translated
    if request.method == 'GET':
        autotext=[]
        for par in json.loads(txt.json):
            auto = {}
            for t in par:
                tr=db.session.query(TDictDekoded).filter(TDictDekoded.word==t).one_or_none()
                if tr==None: auto[t]={}
                else       : auto[t]=json.loads(tr.json)
            autotext.append(auto)
        
        text = {"name":txt.name,"FROMlang":txt.lang,"TOlang":lang,"json":autotext}
        p = { "p":len(text["json"]), "pars": [len(par) for par in text["json"]] }
        return render_template("dekode.html", langs=langs, t=text, parWArr=str(p))

    # if POST: save translated words, to the DICT tables
    if request.method == 'POST':
        for par in request.json["json"]:
            for orgWord in par:
                if 'w' in par[orgWord]:
                    if par[orgWord]['w'] != None:
                        dekodedWord = par[orgWord]['w']
                        # add to language table
                        tr=db.session.query(TDictDekoded).filter(TDictDekoded.word==orgWord).one_or_none()
                        if tr==None: 
                            #as a new word 
                            w = TDictDekoded(orgWord, json.dumps({"w":[dekodedWord],"refCnt":1}))
                            db.session.add(w)
                        else:
                            #or update the old entry
                            ref=json.loads(tr.json)
                            if "refCnt" in ref: ref["refCnt"]+=1;
                            else:               ref["refCnt"]=1;
                            if dekodedWord!="": ref["w"]     = list(set(ref["w"]+[dekodedWord]))
                            tr.json=json.dumps(ref)
                        
                        # update languages list in text Table
                        TDict=dict2lang[FROMlang+"XX"];
                        tr=db.session.query(TDict).filter(TDict.word==orgWord.strip(striptTags).lower()).one_or_none()
                        if tr != None:
                            ref=json.loads(tr.json)
                            if not TOlang in ref["lang"]:
                                ref["lang"].append(TOlang);
                                tr.json=json.dumps(ref)
        dekoded = Dekoded(json.dumps(request.json["json"]))
        db.session.add(dekoded)
        db.session.commit()
        response = app.response_class(response=json.dumps({}),status=200,mimetype='application/json')
        return response
    
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
    return render_template("readText.html", t=dekoded_texts, langs=langs)
    
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
    org_text = db.session.query(Text).filter(Text.name==textname).one_or_none()
    if org_text != None:
        dekoded_text = db.session.query(Dekoded).filter(Dekoded.text_id==org_text.id,Dekoded.lang==lang).one_or_none()
        if dekoded_text != None:
            dekoded=json.loads(dekoded_text.json)
            body=dekoded2body(dekoded)
            foot=dekoded2footer(dekoded)
            return render_template("readTextLang.html",  body=body, foot=foot)
        else: return "NO DEKODED TEXT WITH ID: "+str(org_text.id)
    else: return "NO ORIGINAL TEXT"

	

app.secret_key = 'super secret key'
if __name__=="__main__":
    app.run(debug=True)