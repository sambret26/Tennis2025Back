from datetime import datetime

from database import db

class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fftId = db.Column(db.BigInteger, unique=True, index=True)
    lastName = db.Column(db.String, nullable=False, index=True)
    firstName = db.Column(db.String, nullable=False, index=True)
    rankingId = db.Column(db.Integer, db.ForeignKey("rankings.id"), index=True)
    club = db.Column(db.String)
    phoneNumber = db.Column(db.String)
    email = db.Column(db.String)
    toDelete = db.Column(db.Boolean, default=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    ranking = db.relationship('Ranking')#, back_populates='players')

    categories = db.relationship("Category",
                                secondary="player_categories",
                                lazy="joined")
    payments = db.relationship("Payment", back_populates="player", lazy="joined")
    availabilities = db.relationship("PlayerAvailability", back_populates="player", lazy="joined")
    availabilitiesComments = db.relationship("PlayerAvailabilityComment", back_populates="player", lazy="joined")
    reductions = db.relationship("Reduction", back_populates="player", lazy="joined")
    balance = db.relationship("PlayerBalance", back_populates="player", uselist=False)

    def __init__(self, id=None, fftId=None, lastName=None, firstName=None, 
            rankingId=None, club=None, phoneNumber=None, email=None, toDelete=False):
        self.id = id
        self.fftId = fftId
        self.lastName = lastName
        self.firstName = firstName
        self.rankingId = rankingId
        self.club = club
        self.phoneNumber = phoneNumber
        self.email = email
        self.toDelete = toDelete

    def toDictForDB(self):
        return {
            "id": self.id,
            "lastName": self.lastName,
            "firstName": self.firstName,
            "fftId": self.fftId,
            "rankingId": self.rankingId,
            "club": self.club,
            "phoneNumber": self.phoneNumber,
            "email": self.email,
            "toDelete": self.toDelete
        }

    def toDictForInfos(self):
        return {
            "phoneNumber": self.phoneNumber,
            "email": self.email,
        }

    def toDict(self):
        dictionary = self.toDictForDB()
        dictionary["fullName"] = self.getFullName()
        dictionary["ranking"] = self.ranking.toDict() if self.ranking else None
        dictionary["categories"] = [category.code for category in self.categories]
        dictionary["balance"] = self.balance.toDictForPlayer() if self.balance else None
        dictionary["payments"] = [payment.toDictForPlayer() for payment in self.payments] if self.payments else []
        dictionary["reductions"] = [reduction.toDictForPlayer() for reduction in self.reductions] if self.reductions else []
        return dictionary

    def toMiniDict(self):
        return {
            "id": self.id,
            "fullName": self.getFullName(),
            "ranking": self.ranking.simple if self.ranking else None,
            "phoneNumber": self.phoneNumber,
            "email": self.email,
            "club": self.club
        }

    def toNameDict(self):
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "fullName": self.getFullName()
        }

    def getFullName(self):
        return f"{self.lastName.upper()} {self.firstName.title()}"

    def getFullNameWithRanking(self):
        return f"{self.getFullName()} ({self.ranking.simple})"

    def isDifferent(self, player):
        return self.lastName != player.lastName or self.firstName != player.firstName or \
         self.club != player.club or self.rankingId != player.rankingId or \
         self.phoneNumber != player.phoneNumber or self.email != player.email

    @classmethod
    def fromJson(cls, data):
        return cls(
            fftId=data['fftId'],
            lastName=data['lastName'],
            firstName=data['firstName'],
            rankingId=data['rankingId'],
            club=data['club'],
            phoneNumber=data['phoneNumber'],
            email=data['email']
        )

    @classmethod
    def fromFFT(cls, data):
        return cls(
            fftId=data['jouId'],
            firstName=data['prenom'].title(),
            lastName=data['nom'].title(),
            club=data['clubLibelle'],
            phoneNumber=data['numTel'],
            email=data['mail']
        )

    @classmethod
    def fromFFT2(cls, data):
        return cls(
            fftId=data['joueur2Id'],
            firstName=data['joueur2Prenom'].title(),
            lastName=data['joueur2Nom'].title(),
            club=data['clubJoueur2']
        )