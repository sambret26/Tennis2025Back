from models.PlayerCategories import PlayerCategories
from database import db

class PlayerCategoriesRepository:

    #GETTERS
    @staticmethod
    def getAllPlayerCategories():
        return PlayerCategories.query.all()

    @staticmethod
    def getPlayerCategoryById(playerCategoryId):
        return PlayerCategories.query.get(playerCategoryId)

    @staticmethod
    def getNumberPlayersByCategory(categoryId):
        return PlayerCategories.query.filter_by(categoryId=categoryId).count()
    
    @staticmethod
    def getInscriptionsId():
        inscriptionsId = PlayerCategories.query.with_entities(PlayerCategories.inscriptionId).all()
        return [inscriptionId for (inscriptionId,) in inscriptionsId]

    @staticmethod
    def getPlayersMap():
        return {playerCategory.inscriptionId: playerCategory.playerId for playerCategory in PlayerCategories.query.all()}

    #ADDERS
    @staticmethod
    def addPlayerCategory(playerCategory):
        db.session.add(playerCategory)
        db.session.commit()

    @staticmethod
    def addPlayerCategories(playerCategories):
        db.session.add_all(playerCategories)
        db.session.commit()

    #DELETERS
    @staticmethod
    def deletePlayerCategoryByPlayerIdAndCategoryId(playerId, categoryId):
        PlayerCategories.query.filter_by(playerId=playerId, categoryId=categoryId).delete()
        db.session.commit()

    @staticmethod
    def deleteAllPlayerCategories():
        PlayerCategories.query.delete()
        db.session.commit()