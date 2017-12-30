from flask_sqlalchemy import SQLAlchemy

# create a new SQLAlchemy object
db = SQLAlchemy()

# Base model that for other models to inherit from
class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
            onupdate=db.func.current_timestamp())

class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email
    def __repr__(self):
        return '<User %r>' % (self.name)

class Text(Base):
    __tablename__ = 'text'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    lang = db.Column(db.String(2))
    json = db.Column(db.String())
    def __init__(self,nm,ln,jsn):
        self.name =nm
        self.lang =ln
        self.json =jsn
    def __repr__(self):
        return '<Textname: %r>' % self.name

class Dekoded(Base):
    __tablename__ = 'dekoded'
    id = db.Column(db.Integer, primary_key=True)
    json = db.Column(db.String(80))
    text_id = db.Column(db.Integer, db.ForeignKey('text.id'))
    text = db.relationship('Text', backref=db.backref('posts', lazy='dynamic'))
    lang = db.Column(db.String(2))
    def __init__(self, json, lang, text_id):
        self.json = json
        self.lang = lang
        self.text_id = text_id
    def __repr__(self):
        return '<Post %r>' % self.title

class WDictBase(db.Model):
    __abstract__ = True
    word = db.Column(db.String(), unique=True, primary_key=True)
    json = db.Column(db.String())
    def __init__(self, wrd, jsn):
        self.word = wrd
        self.json = jsn
    def __repr__(self):
        return '<%r : %r>' % self.word, self.json

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)  
    db.init_app(app)
    app.config.from_pyfile('config.py')
    with app.app_context():
        db.create_all()

# Sehr fuschig, will die Tabelle eigentlich seriell fur verschiedene Sprachen 
# als einfaches Worterbuch haben. Sollte besser gelost werden...


##############################################################
# THE CODE BELOW IS GENERATED WITH THE utils/generateModels.py
##############################################################
class WDictDEEN(db.Model):
        __tablename__ = "WDictDEEN"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictDEES(db.Model):
        __tablename__ = "WDictDEES"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictDEEO(db.Model):
        __tablename__ = "WDictDEEO"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictDEFR(db.Model):
        __tablename__ = "WDictDEFR"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictDEHE(db.Model):
        __tablename__ = "WDictDEHE"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictDEJP(db.Model):
        __tablename__ = "WDictDEJP"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictDEPL(db.Model):
        __tablename__ = "WDictDEPL"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictDERU(db.Model):
        __tablename__ = "WDictDERU"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictDEXX(db.Model):
        __tablename__ = "WDictDEXX"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictENDE(db.Model):
        __tablename__ = "WDictENDE"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictENES(db.Model):
        __tablename__ = "WDictENES"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictENEO(db.Model):
        __tablename__ = "WDictENEO"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictENFR(db.Model):
        __tablename__ = "WDictENFR"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictENHE(db.Model):
        __tablename__ = "WDictENHE"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictENJP(db.Model):
        __tablename__ = "WDictENJP"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictENPL(db.Model):
        __tablename__ = "WDictENPL"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictENRU(db.Model):
        __tablename__ = "WDictENRU"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictENXX(db.Model):
        __tablename__ = "WDictENXX"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictESDE(db.Model):
        __tablename__ = "WDictESDE"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictESEN(db.Model):
        __tablename__ = "WDictESEN"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictESEO(db.Model):
        __tablename__ = "WDictESEO"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictESFR(db.Model):
        __tablename__ = "WDictESFR"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictESHE(db.Model):
        __tablename__ = "WDictESHE"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictESJP(db.Model):
        __tablename__ = "WDictESJP"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictESPL(db.Model):
        __tablename__ = "WDictESPL"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictESRU(db.Model):
        __tablename__ = "WDictESRU"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictESXX(db.Model):
        __tablename__ = "WDictESXX"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictEODE(db.Model):
        __tablename__ = "WDictEODE"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictEOEN(db.Model):
        __tablename__ = "WDictEOEN"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictEOES(db.Model):
        __tablename__ = "WDictEOES"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictEOFR(db.Model):
        __tablename__ = "WDictEOFR"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictEOHE(db.Model):
        __tablename__ = "WDictEOHE"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictEOJP(db.Model):
        __tablename__ = "WDictEOJP"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictEOPL(db.Model):
        __tablename__ = "WDictEOPL"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictEORU(db.Model):
        __tablename__ = "WDictEORU"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictEOXX(db.Model):
        __tablename__ = "WDictEOXX"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictFRDE(db.Model):
        __tablename__ = "WDictFRDE"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictFREN(db.Model):
        __tablename__ = "WDictFREN"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictFRES(db.Model):
        __tablename__ = "WDictFRES"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictFREO(db.Model):
        __tablename__ = "WDictFREO"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictFRHE(db.Model):
        __tablename__ = "WDictFRHE"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictFRJP(db.Model):
        __tablename__ = "WDictFRJP"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictFRPL(db.Model):
        __tablename__ = "WDictFRPL"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictFRRU(db.Model):
        __tablename__ = "WDictFRRU"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictFRXX(db.Model):
        __tablename__ = "WDictFRXX"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictHEDE(db.Model):
        __tablename__ = "WDictHEDE"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictHEEN(db.Model):
        __tablename__ = "WDictHEEN"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictHEES(db.Model):
        __tablename__ = "WDictHEES"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictHEEO(db.Model):
        __tablename__ = "WDictHEEO"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictHEFR(db.Model):
        __tablename__ = "WDictHEFR"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictHEJP(db.Model):
        __tablename__ = "WDictHEJP"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictHEPL(db.Model):
        __tablename__ = "WDictHEPL"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictHERU(db.Model):
        __tablename__ = "WDictHERU"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictHEXX(db.Model):
        __tablename__ = "WDictHEXX"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictJPDE(db.Model):
        __tablename__ = "WDictJPDE"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictJPEN(db.Model):
        __tablename__ = "WDictJPEN"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictJPES(db.Model):
        __tablename__ = "WDictJPES"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictJPEO(db.Model):
        __tablename__ = "WDictJPEO"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictJPFR(db.Model):
        __tablename__ = "WDictJPFR"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictJPHE(db.Model):
        __tablename__ = "WDictJPHE"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictJPPL(db.Model):
        __tablename__ = "WDictJPPL"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictJPRU(db.Model):
        __tablename__ = "WDictJPRU"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictJPXX(db.Model):
        __tablename__ = "WDictJPXX"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictPLDE(db.Model):
        __tablename__ = "WDictPLDE"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictPLEN(db.Model):
        __tablename__ = "WDictPLEN"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictPLES(db.Model):
        __tablename__ = "WDictPLES"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictPLEO(db.Model):
        __tablename__ = "WDictPLEO"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictPLFR(db.Model):
        __tablename__ = "WDictPLFR"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictPLHE(db.Model):
        __tablename__ = "WDictPLHE"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictPLJP(db.Model):
        __tablename__ = "WDictPLJP"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictPLRU(db.Model):
        __tablename__ = "WDictPLRU"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictPLXX(db.Model):
        __tablename__ = "WDictPLXX"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictRUDE(db.Model):
        __tablename__ = "WDictRUDE"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictRUEN(db.Model):
        __tablename__ = "WDictRUEN"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictRUES(db.Model):
        __tablename__ = "WDictRUES"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictRUEO(db.Model):
        __tablename__ = "WDictRUEO"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictRUFR(db.Model):
        __tablename__ = "WDictRUFR"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictRUHE(db.Model):
        __tablename__ = "WDictRUHE"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictRUJP(db.Model):
        __tablename__ = "WDictRUJP"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictRUPL(db.Model):
        __tablename__ = "WDictRUPL"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'
class WDictRUXX(db.Model):
        __tablename__ = "WDictRUXX"
        word = db.Column(db.String(), unique=True, primary_key=True)
        json = db.Column(db.String())
        def __init__(self, name, jsn):
            self.word = name
            self.json = jsn
        def __repr__(self):
            return '<'+ self.word +' : '+self.json+'>'

##############################################################
# END OF GENERATED CODE ######################################
##############################################################

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)  
    db.init_app(app)
    app.config.from_pyfile('config.py')
    with app.app_context():
        db.create_all()
