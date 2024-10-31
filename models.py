from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Elev(db.Model):
    __tabelname__ = 'Elev'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    fodselsdato = db.Column(db.String(10), nullable=False)
    lokation_id = db.column(db.Integer, db.ForeignKey('lokation.id'))
    lokation = db.relationship('Lokation')

    def __repr__(self):
        return f'Elev {self.navn} og {self.fodselsdato}'

class Lokation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False) #fx stenløse el. hvidovre
    #optional: adresse eller andet relevant info

class Dansehold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stilart = db.Column(db.String(50), nullable=False) #fx Disco, Showdance
    instruktør = db.Column(db.String(100))
    lokation_id = db.Column(db.Integer, db.ForeignKey('lokation.id'))
    lokation = db.relationship('Lokation')

class Danselektion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dato = db.Column(db.Date, nullable=False) #fx en given dato
    dansehold_id = db.Column(db.Integer, db.ForeignKey('dansehold.id'))
    dansehold = db.relationship('Dansehold')
    attendance = db.relationsship('Elev', secondary='attendance') #Fremmøde for hver elev

