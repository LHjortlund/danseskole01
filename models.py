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
    lokation_id = db.Column(db.Integer, db.ForeignKey('lokation.id'))
    lokation = db.relationship('Lokation')

    def __repr__(self):
        return f'Elev {self.navn} og {self.fodselsdato}'

class Lokation(db.Model):
    __tablename__ = 'lokation'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False) #fx stenløse el. hvidovre
    #optional: adresse eller andet relevant info


class Instruktor(db.Model):
    __tablename__ = 'instruktor'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefon = db.Column(db.String(100))

    def __str__(self):
        return f'Instruktor {self.navn}'

class Dansehold(db.Model):
    __tablename__ = 'dansehold'
    id = db.Column(db.Integer, primary_key=True)
    stilart = db.Column(db.String(50), nullable=False) #fx Disco, Showdance
    instruktor = db.Column(db.String(100))
    beskrivelse = db.Column(db.String(200))
    lokation_id = db.Column(db.Integer, db.ForeignKey('lokation.id'))
    lokation = db.relationship('Lokation')

    def __repr__(self):
        return f'Dansehold {self.stilart}'

class Danselektion(db.Model):
    __tablename__ = 'danselektion'
    id = db.Column(db.Integer, primary_key=True)
    dato = db.Column(db.String, nullable=False) #fx en given dato
    tidspunkt = db.Column(db.Time, nullable=False) # tidspunkt for danselektion
    dansehold_id = db.Column(db.Integer, db.ForeignKey('dansehold.id')) #tilknytning til danselektioner
    dansehold = db.relationship('Dansehold')
    elev_id = db.Column(db.Integer, db.ForeignKey('elev.id'))
    elev = db.relationship('Elev')
    lokation_id = db.Column(db.Integer, db.ForeignKey('lokation.id')) #tilknytning til lokation
    lokation = db.relationship('Lokation')
    instruktor_id = db.Column(db.Integer, db.ForeignKey('instruktor.id'))  # Instruktør
    instruktor = db.relationship('Instruktor')  # Instruktør for lektionen
    attendance = db.relationship('Elev', secondary='attendance', backref='danselektioner') #Fremmøde for hver elev

    @property
    def iso_dato(self):
        print(f"Type of dato: {type(self.dato)}, Value: {self.dato}")
        if self.dato:
            try:
                # Ensure dato is formatted correctly
                return datetime.fromisoformat(str(self.dato)).isoformat()
            except ValueError:
                # Handle case where dato is not in ISO format
                return None
        return None


# class prøvetime(db.Model):
#     __tablename__ = 'prøvetime'
#     id = db.Column(db.Integer, primary_key=True)
#     dato = db.Column(db.Date, nullable=False)
#     prøvetime_id = db.Column(db.Integer, db.ForeignKey('prøvetime.id'))
#     attendance = db.relationship('Elev', secondary='attendance')
