from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy.orm import backref

db = SQLAlchemy()


# Many-to-Many tabel til at forbinde elever og danselektioner
attendance = db.Table('attendance',
    db.Column('elev_id', db.Integer, db.ForeignKey('elev.id')),
    db.Column('danselektion_id', db.Integer, db.ForeignKey('danselektion.id'))
)


class Elev(db.Model):
    __tablename__ = 'elev'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    fodselsdato = db.Column(db.String(10), nullable=False)
    lokation_id = db.column(db.Integer, db.ForeignKey('lokation.id'))
    lokation = db.relationship('Lokation')

    def __repr__(self):
        return f'Elev {self.navn} og {self.fodselsdato}'

class Lokation(db.Model):
    __tablename__ = 'lokation'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False) #fx stenløse el. hvidovre
    #optional: adresse eller andet relevant info

class Dansehold(db.Model):
    __tablename__ = 'dansehold'
    id = db.Column(db.Integer, primary_key=True)
    stilart = db.Column(db.String(50), nullable=False) #fx Disco, Showdance
    instruktør = db.Column(db.String(100))
    lokation_id = db.Column(db.Integer, db.ForeignKey('lokation.id'))
    lokation = db.relationship('Lokation')

class Danselektion(db.Model):
    __tablename__ = 'danselektion'
    id = db.Column(db.Integer, primary_key=True)
    dato = db.Column(db.Date, nullable=False) #fx en given dato
    dansehold_id = db.Column(db.Integer, db.ForeignKey('dansehold.id'))
    dansehold = db.relationship('Dansehold')
    attendance = db.relationsship('Elev', secondary='attendance', backref='danselektioner') #Fremmøde for hver elev

