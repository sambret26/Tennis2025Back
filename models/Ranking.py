from datetime import datetime
from database import db

class Ranking(db.Model):
    __tablename__ = 'rankings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fftId = db.Column(db.BigInteger, nullable=False)
    simple = db.Column(db.String)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, fftId, simple):
        self.fftId = fftId
        self.simple = simple

    def toDict(self):
        return {
            'id': self.id,
            'fftId': self.fftId,
            'simple': self.simple
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            fftId=data['fftId'],
            simple=data['simple']
        )

    @classmethod
    def fromFFT(cls, data):
        return cls(
            fftId=data['echelon'],
            simple=data['libelle'].replace(' ','')
        )