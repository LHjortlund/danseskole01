from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy.orm import backref

db = SQLAlchemy()

# Many-to-Many tabel til at forbinde elever og dansehold (HoldDeltager)
hold_deltager = db.Table('hold_deltager',
                         db.Column('dansehold_id', db.Integer, db.ForeignKey('dansehold.id'), primary_key=True),
                         db.Column('elev_id', db.Integer, db.ForeignKey('elev.id'), primary_key=True)
)

#Elev-klassen represents en elev in the system
class Elev(db.Model):
    __tablename__ = 'elev'
    id = db.Column(db.Integer, primary_key=True)
    fornavn = db.Column(db.String(100), nullable=False)
    efternavn = db.Column(db.String(100), nullable=False)
    fodselsdato = db.Column(db.String(10), nullable=False)
    mobil = db.Column(db.Integer, nullable=False)

    #Relation til dansehold via HoldDeltager-tabellen
    dansehold = db.relationship('Dansehold', secondary=hold_deltager, back_populates="elever")

    def __repr__(self):
        return f'Elev {self.fornavn} {self.efternavn}'

#Instruktor class repræsenterer en instruktør i systemet
class Instruktor(db.Model):
    __tablename__ = 'instruktor'
    id = db.Column(db.Integer, primary_key=True)
    fornavn = db.Column(db.String(100), nullable=False)
    efternavn = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefon = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f'Instruktor {self.fornavn}'

#Stilarr-klassen repræsenterer en dansestil i systemet
class Stilart(db.Model):
    __tablename__ = 'stilart'
    id = db.Column(db.Integer, primary_key=True)
    stilart = db.Column(db.String(100), nullable=False)
    beskrivelse = db.Column(db.String(100), nullable=False)

class Lokation(db.Model):
    __tablename__ = 'lokation'
    id = db.Column(db.Integer, primary_key=True)
    adresse = db.Column(db.String(100), nullable=False)

class Dansehold(db.Model):
    __tablename__ = 'dansehold'
    id = db.Column(db.Integer, primary_key=True)
    startdato = db.Column(db.Date, nullable=False)
    antal_gange = db.Column(db.Integer, nullable=False)
    tidspunkt = db.Column(db.Time, nullable=False)
    lokation_id = db.Column(db.Integer, db.ForeignKey('lokation.id'), nullable=False)
    beskrivelse = db.Column(db.String(255), nullable=True) #Tillader tomt felt
    instruktor_id = db.Column(db.Integer, db.ForeignKey('instruktor.id'), nullable=False)
    stilart_id = db.Column(db.Integer, db.ForeignKey('stilart.id'), nullable=False)

    # Relationer til dansehold
    instruktor = db.relationship('Instruktor', backref='dansehold')
    stilart = db.relationship('Stilart', backref='dansehold')
    lokation = db.relationship('Lokation', backref='dansehold')
    elever = db.relationship('Elev', secondary=hold_deltager, back_populates="dansehold")


# Registering-klassen repræsenterer en registrering af en elevs deltagelse på en specifik dato
class Registering(db.Model):
    __tablename__ = 'registering'
    id = db.Column(db.Integer, primary_key=True)
    dato = db.Column(db.Date, nullable=False)

    dansehold_id = db.Column(db.Integer, db.ForeignKey('dansehold.id'), nullable=False)
    elev_id = db.Column(db.Integer, db.ForeignKey('elev.id'), nullable=False)

    # Relationer til dansehold og elev
    dansehold = db.relationship('Dansehold', backref=backref('registreringer', cascade='all, delete-orphan'))
    elev = db.relationship('Elev', backref=backref('registreringer', cascade='all, delete-orphan'))

# class Danselektion(db.Model):
#     __tablename__ = 'danselektion'
#     id = db.Column(db.Integer, primary_key=True)
#     dato = db.Column(db.String, nullable=False) #fx en given dato
#     tidspunkt = db.Column(db.Time, nullable=False) # tidspunkt for danselektion
#     dansehold_id = db.Column(db.Integer, db.ForeignKey('dansehold.id')) #tilknytning til danselektioner
#     dansehold = db.relationship('Dansehold')
#     elev_id = db.Column(db.Integer, db.ForeignKey('elev.id'))
#     elev = db.relationship('Elev')
#     lokation_id = db.Column(db.Integer, db.ForeignKey('lokation.id')) #tilknytning til lokation
#     lokation = db.relationship('Lokation')
#     instruktor_id = db.Column(db.Integer, db.ForeignKey('instruktor.id'))  # Instruktør
#     instruktor = db.relationship('Instruktor')  # Instruktør for lektionen
#     attendance = db.relationship('Elev', secondary='attendance', backref='danselektioner') #Fremmøde for hver elev
#
#     @property
#     def iso_dato(self):
#         # Check type og værdi af dato
#         print(f"Type of dato: {type(self.dato)}, Value: {self.dato}")
#
#         if isinstance(self.dato, str):
#             try:
#                 # Konverterer datoen fra string til ISO format
#                 return datetime.fromisoformat(self.dato).isoformat()
#             except ValueError:
#                 print("Datoen er ikke i gyldigt ISO-format.")
#                 return None
#         else:
#             print("Dato er ikke en streng.")
#             return None


# class prøvetime(db.Model):
#     __tablename__ = 'prøvetime'
#     id = db.Column(db.Integer, primary_key=True)
#     dato = db.Column(db.Date, nullable=False)
#     prøvetime_id = db.Column(db.Integer, db.ForeignKey('prøvetime.id'))
#     attendance = db.relationship('Elev', secondary='attendance')
