from datetime import datetime
from database import db

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playerId = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    player = db.relationship('Player', back_populates='payments')

    def __init__(self, playerId, amount, date):
        self.playerId = playerId
        self.amount = amount
        self.date = date

    def toDict(self):
        return {
            'id': self.id,
            'playerId': self.playerId,
            'amount': self.amount,
            'date': self.date
        }

    def toDictForPlayer(self):
        return {
            'amount': self.amount,
            'date': self.date
        }

    def toDictForList(self):
        return {
            'playerFullName': self.player.toNameDict().get('fullName'),
            'amount': self.amount,
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            playerId=data['playerId'],
            amount=data['amount'],
            date=data['date']
        )