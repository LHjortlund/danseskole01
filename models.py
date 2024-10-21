from app import db

class Elev(db.Model):
    __tabelname__ = 'Elev'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    fodselsdato = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'Elev {self.navn} og {self.fodselsdato}'



class Lektion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    elev_id = db.Column(db.Integer, db.ForeignKey('elev.id'), nullable=False)
    elev = db.relationship('Elev', backref=db.backref('lektioner', lazy=True))
