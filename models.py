from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.event import listens_for

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

# Event listener, der automatisk opretter Fremmøde, når en Registering oprettes
@listens_for(Registering, 'after_insert')
def opret_fremmoede_automatisk(mapper, connection, target):
    # Opret en Fremmøde-post, når en Registering oprettes
    nyt_fremmoede = Fremmøde(
        dato=target.dato,
        elev_id=target.elev_id,
        dansehold_id=target.dansehold_id,
        registering_id=target.id  # Reference til den oprettede registrering
    )
    # Brug en ny session til at tilføje Fremmøde
    from app import db
    with db.session.begin(subtransactions=True):
        db.session.add(nyt_fremmoede)

#Registrering af fremmøde, gør det muligt at gemme fremmøde for hver dato, elev og dansehold
class Fremmøde(db.Model):
    __tablename__ = 'fremmoede'
    id = db.Column(db.Integer, primary_key=True)
    dato = db.Column(db.Date, nullable=False)

    #Fremmed nøgler
    elev_id = db.Column(db.Integer, db.ForeignKey('elev.id'), nullable=False)
    dansehold_id = db.Column(db.Integer, db.ForeignKey('dansehold.id'), nullable=False)
    registering_id = db.Column(db.Integer, db.ForeignKey('registering.id'), nullable=True)

    #Relationer
    elev = db.relationship('Elev', backref=backref('fremmoeder', cascade='all, delete-orphan'))
    dansehold = db.relationship('Dansehold', backref=backref('fremmoeder', cascade='all, delete-orphan'))
    registering = db.relationship('Registering', backref=backref('fremmoeder', cascade='all, delete-orphan'))
