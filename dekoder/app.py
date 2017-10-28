# app.py or app/__init__.py
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
		output='gen/home.js', filters='jsmin'
	),
	'home_css': Bundle(
		'bower_components/materialize/dist/css/materialize.min.css',
		'icon.css',
		output='gen/home.css' ,filters='cssmin'
	),
}

#Available languages
langs=("AR","DE","EN","ES","EO","FR","JP","PL","RU","ZH")
assets = Environment(app)
assets.register(bundles)

# initialize and create the database
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
	return render_template("index.html", langs=langs)

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

            # add all new words to the source langs table
            newW=0 #cnts the number of new words
            #counts up the references of the word or adds a new word to the lang specific dict
            for par in request.json["json"]:
                for w in par:
                    tr=db.session.query(WDictDEXX).filter(WDictDEXX.word==w.strip(" ,.\n").lower()).one_or_none()
                    if tr==None: 
                        newW+=1
                        w = WDict(w, json.dumps({"refCnt":1,"w":[]}),request.json["lang"],"")
                        db.session.add(w)
                    else:
                        ref=json.loads(tr.json)
                        ref["refCnt"]+=1;
                        tr.json=json.dumps(ref)
            db.session.commit()
            #response
            return json.dumps({'message':"Formated text was succesfully saved! "+str(newW)+" new Words added..."}), 200, {'ContentType':'application/json'} 
        except ValidationError:
            return json.dumps({'message':"No valid text format submitted..."}), 200, {'ContentType':'application/json'}
        except IntegrityError as e:
            return json.dumps({"success":False,'message':"Formated text with given name already taken. Choose another name..."+str(e)}), 200, {'ContentType':'application/json'}
        except Exception as e:
            return json.dumps({"success":False,'message':str(e)}), 200, {'ContentType':'application/json'} 

    else:
        return render_template("format.html", langs=langs)

############DEKODE
# shows you all the formated texts and lets you chose a language to dekode them to
@app.route('/dekode')
def dekode():
    texts = Text.query.all()
    return render_template("getFormatedTexts.html", t=texts, langs=langs)

# shows you all the languages to dekode a text to
@app.route('/dekode/<string:textname>')
def dekodeText(textname):
    return render_template("getFormatedTexts.html", langs=langs, t=t)

# get:  * shows you the formated text and lets you add a dekodation to each word unit
#       * autocompletes by showing existing translations from former entries in the database
# post: * saves the dekoded text with all the translations entered
@app.route('/dekode/<string:textname>/<string:lang>', methods=['GET', 'POST'])
def dekodeTextLang(textname,lang):
    txt = db.session.query(Text).filter(Text.name==textname).one()#.filter(Text.name == textname).one()#query(Text).filter(Text.name == textname).first()
    autotext=[]
    for par in json.loads(txt.json):
        auto = {}
        for t in par:
            tr=db.session.query(WDict).filter(WDict.word==t.strip(" ,.\n").lower()).one_or_none()
            if tr==None: auto[t]={}
            else       : auto[t]=json.loads(tr.json)
        autotext.append(auto)
    
    text = {"name":txt.name,"FROMlang":txt.lang,"TOlang":lang,"json":autotext}
    p = { "p":len(text), "pars": [len(par) for par in text] }
    return render_template("dekode.html", langs=langs, t=text, parWArr=str(p))

############READ
# lets you read all the dekoded texts to practise your target language ^^

# shows you all dekoded text
@app.route('/read', methods=['GET', 'POST'])
def read():
    pass

#shows you all languages a text is dekoded to
@app.route('/read/<string:textname>', methods=['GET'])
def readTextPDF():
    pass

# converts on dekodation of a text into a pdf for print
@app.route('/read/<string:textname>_<string:lang>.pdf', methods=['GET'])
def readText():
    pass

# shows you a dekoded text in one target language
@app.route('/read/<string:textname>/<string:lang>', methods=['GET'])
def readTextLang():
	pass

app.secret_key = 'super secret key'
if __name__=="__main__":
    app.run(debug=True)

#t=[{"This":{"w":"","e":""},"is":{"w":"","e":""},"a dummy text.":{"w":"","e":""},"In the same manner":{"w":"","e":""},"as":{"w":"","e":""},"seen":{"w":"","e":""},"here":{"w":"","e":""},"you":{"w":"","e":""},"have to":{"w":"","e":""},"preformat":{"w":"","e":""},"your text.":{"w":"","e":""},"You":{"w":"","e":""},"can":{"w":"","e":""},"enter":{"w":"","e":""},"word units":{"w":"","e":""},"by seperating":{"w":"","e":""},"each":{"w":"","e":""},"by":{"w":"","e":""},"a double whitespace.":{"w":"","e":""}, "On the right":{"w":"","e":""},"can see":{"w":"","e":""},"the preview,":{"w":"","e":""},"where":{"w":"","e":""},"each word unit":{"w":"","e":""},"is seperated":{"w":"","e":""},"a black stroke":{"w":"","e":""},"from":{"w":"","e":""},"one another. ":{"w":"","e":""}},{"":{"w":"","e":""}},{"Also":{"w":"","e":""},"by":{"w":"","e":""},"using":{"w":"","e":""},"two newlines":{"w":"","e":""},"there will be":{"w":"","e":""},"a paragraph.":{"w":"","e":""}},{"":{"w":"","e":""}},{"This is":{"w":"","e":""},"the first":{"w":"","e":""},"of two stages":{"w":"","e":""},"to dekode":{"w":"","e":""},"a text. The second":{"w":"","e":""},"will be":{"w":"","e":""},"to add":{"w":"","e":""},"translations":{"w":"","e":""},"for":{"w":"","e":""},"the word units":{"w":"","e":""},"and":{"w":"","e":""},"if":{"w":"","e":""},"necessary":{"w":"","e":""},"explainations.":{"w":"","e":""}},{"":{"w":"","e":""}},{"You":{"w":"","e":""},"can":{"w":"","e":""},"use":{"w":"","e":""},"the button":{"w":"","e":""},"above":{"w":"","e":""},"to split":{"w":"","e":""},"all":{"w":"","e":""},"words":{"w":"","e":""},"from":{"w":"","e":""},"your text":{"w":"","e":""},"and":{"w":"","e":""},"only":{"w":"","e":""},"regroup":{"w":"","e":""},"the multi-word-units.":{"w":"","e":""}},{"":{"w":"","e":""}}]
