from models.Grid import Grid
from database import db

class GridRepository:

    #GETTERS
    @staticmethod
    def getAllGrids():
        return Grid.query.order_by(Grid.categoryId).order_by(Grid.fftId).all()

    @staticmethod
    def getGridsMap():
        grids = Grid.query.all()
        return {grid.id: grid.code for grid in grids}

    @staticmethod
    def getGridsFFTMap():
        grids = Grid.query.all()
        return {grid.fftId: grid.code for grid in grids}

    @staticmethod
    def getNextGridsMap():
        grids = Grid.query.all()
        return {str(grid.fftId): grid.nextGridId for grid in grids}

    #ADDERS
    @staticmethod
    def addGrids(grids):
        db.session.add_all(grids)
        db.session.commit()

    #DELETERS
    @staticmethod
    def deleteAllGrids():
        Grid.query.delete()
        db.session.commit()

    @staticmethod
    def deleteAllGridsByCategory(categoryId):
        Grid.query.filter_by(categoryId=categoryId).delete()
        db.session.commit()