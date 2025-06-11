from models.Ranking import Ranking
from database import db

class RankingRepository:

    #GETTERS
    @staticmethod
    def getAllRankings():
        return Ranking.query.all()

    @staticmethod
    def getRankingById(rankingId):
        return Ranking.query.get(rankingId)

    @staticmethod
    def getRankingBySimple(rankingSimple):
        return Ranking.query.filter_by(simple=rankingSimple).first()

    @staticmethod
    def getRankingMapSimple():
        return {r.fftId: r for r in Ranking.query.all() if r.simple is not None}

    #ADDERS
    @staticmethod
    def addRanking(ranking):
        db.session.add(ranking)
        db.session.commit()

    @staticmethod
    def addRankings(rankings):
        db.session.add_all(rankings)
        db.session.commit()

    #DELETERS
    @staticmethod
    def deleteAllRankings():
        Ranking.query.delete()
        db.session.commit()