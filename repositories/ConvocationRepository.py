from models.Convocation import Convocation
from database import db

class ConvocationRepository:

    #GETTERS
    @staticmethod
    def getConvocationsMap():
        return {c.convocationId: c for c in Convocation.query.all()}

    #ADDERS
    @staticmethod
    def addConvocations(convocations):
        db.session.add_all(convocations)
        db.session.commit()

    #SETTERS
    @staticmethod
    def updateConvocationStatus(convocationId, status):
        Competition.query.filter_by(convocationId=convocationId).update({status: status})
        db.session.commit()