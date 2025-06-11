from models.Profil import Profil

class ProfilRepository:

    #GETTERS
    @staticmethod
    def getAllProfils():
        return Profil.query.all()

    @staticmethod
    def getProfilByValue(value):
        return Profil.query.filter_by(value=value).first()