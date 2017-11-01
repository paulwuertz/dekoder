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

class Dekoded(Base):
    id = db.Column(db.Integer, primary_key=True)
    json = db.Column(db.String(80))
    text_id = db.Column(db.Integer, db.ForeignKey('text.id'))
    text = db.relationship('Text',
        backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, json):
        self.date = datetime.utcnow()
        self.json = category

    def __repr__(self):
        return '<Post %r>' % self.title


class Text(Base):
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


class WDictBase(db.Model):
    __abstract__ = True
    word = db.Column(db.String(), unique=True, primary_key=True)
    json = db.Column(db.String())

    def __init__(self, wrd, jsn):
        self.word = wrd
        self.json = jsn

    def __repr__(self):
        return '<%r : %r>' % self.word, self.json

# Sehr fuschig, will die Tabelle eigentlich seriell fur verschiedene Sprachen 
# als einfaches Worterbuch haben. Sollte besser gelost werden...
#
class WDictDEXX(db.Model):
    __tablename__ = "WDictDEXX"
    word = db.Column(db.String(), unique=True, primary_key=True)
    json = db.Column(db.String())
    def __init__(self, name, jsn):
        self.word = name
        self.json = jsn
    def __repr__(self):
        return '<%r : %r>' % self.word, self.json
class WDictDEAR(db.Model):
    __tablename__ = "WDictDEAR"
    word = db.Column(db.String(), unique=True, primary_key=True)
    json = db.Column(db.String())
    def __init__(self, name, jsn):
        self.word = name
        self.json = jsn
class WDictDEEN(db.Model):
    __tablename__ = "WDictDEEN"
    word = db.Column(db.String(), unique=True, primary_key=True)
    json = db.Column(db.String())
    def __init__(self, name, jsn):
        self.word = name
        self.json = jsn
class WDictDEES(db.Model):
    __tablename__ = "WDictDEES"
    word = db.Column(db.String(), unique=True, primary_key=True)
    json = db.Column(db.String())
    def __init__(self, name, jsn):
        self.word = name
        self.json = jsn
class WDictDEEO(db.Model):
    __tablename__ = "WDictDEEO"
    word = db.Column(db.String(), unique=True, primary_key=True)
    json = db.Column(db.String())
    def __init__(self, name, jsn):
        self.word = name
        self.json = jsn
class WDictDEFR(db.Model):
    __tablename__ = "WDictDEFR"
    word = db.Column(db.String(), unique=True, primary_key=True)
    json = db.Column(db.String())
    def __init__(self, name, jsn):
        self.word = name
        self.json = jsn
class WDictDEJP(db.Model):
    __tablename__ = "WDictDEJP"
    word = db.Column(db.String(), unique=True, primary_key=True)
    json = db.Column(db.String())
    def __init__(self, name, jsn):
        self.word = name
        self.json = jsn
class WDictDEPL(db.Model):
    __tablename__ = "WDictDEPL"
    word = db.Column(db.String(), unique=True, primary_key=True)
    json = db.Column(db.String())
    def __init__(self, name, jsn):
        self.word = name
        self.json = jsn
class WDictDERU(db.Model):
    __tablename__ = "WDictDERU"
    word = db.Column(db.String(), unique=True, primary_key=True)
    json = db.Column(db.String())
    def __init__(self, name, jsn):
        self.word = name
        self.json = jsn
class WDictDEZH(db.Model):
    __tablename__ = "WDictDEZH"
    word = db.Column(db.String(), unique=True, primary_key=True)
    json = db.Column(db.String())
    def __init__(self, name, jsn):
        self.word = name
        self.json = jsn
