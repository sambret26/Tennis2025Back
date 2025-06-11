from datetime import datetime
from database import db

class Convocation(db.Model):
    __tablename__ = 'convocations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    convocationId = db.Column(db.String, nullable=False, unique=True)
    crmId = db.Column(db.BigInteger, nullable=False)
    matchId = db.Column(db.BigInteger, nullable=False)
    state = db.Column(db.String)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, convocationId, crmId, matchId, state):
        self.convocationId = convocationId
        self.crmId = crmId
        self.matchId = matchId
        self.state = state

    def toDict(self):
        return {
            'id': self.id,
            'convocationId': self.convocationId,
            'crmId': self.crmId,
            'matchId': self.matchId,
            'state': self.state
        }

    @classmethod
    def fromFFT(cls, data):
        return cls(
            convocationId=data['conId'],
            crmId=data['crmId'],
            matchId=data['matId'],
            state=data['statutConvocationCode']
        )