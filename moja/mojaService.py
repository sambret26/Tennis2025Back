from moja import mojaRequests

from models.Category import Category
from models.Court import Court
from models.Grid import Grid
from models.Ranking import Ranking
from models.Match import Match
from constants import constants

from repositories.CategoryRepository import CategoryRepository
from repositories.CourtRepository import CourtRepository
from repositories.GridRepository import GridRepository
from repositories.SettingRepository import SettingRepository
from repositories.RankingRepository import RankingRepository
from repositories.PlayerRepository import PlayerRepository
from repositories.PlayerAvailabilityCommentRepository import PlayerAvailabilityCommentRepository
from repositories.PlayerBalanceRepository import PlayerBalanceRepository
from repositories.PlayerAvailabilityRepository import PlayerAvailabilityRepository
from repositories.PaymentRepository import PaymentRepository
from repositories.PlayerCategoriesRepository import PlayerCategoriesRepository
from repositories.ReductionRepository import ReductionRepository
from repositories.TransactionRepository import TransactionRepository
from repositories.MatchRepository import MatchRepository
from repositories.CompetitionRepository import CompetitionRepository
from repositories.UrlRepository import UrlRepository
from repositories.TeamRepository import TeamRepository

from logger.logger import log, BATCH

categoryRepository = CategoryRepository()
courtRepository = CourtRepository()
gridRepository = GridRepository()
settingRepository = SettingRepository()
rankingRepository = RankingRepository()
playerRepository = PlayerRepository()
playerAvailabilityCommentRepository = PlayerAvailabilityCommentRepository()
playerBalanceRepository = PlayerBalanceRepository()
playerAvailabilityRepository = PlayerAvailabilityRepository()
paymentRepository = PaymentRepository()
playerCategoriesRepository = PlayerCategoriesRepository()
reductionRepository = ReductionRepository()
transactionRepository = TransactionRepository()
matchRepository = MatchRepository()
competitionRepository = CompetitionRepository()
urlRepository = UrlRepository()
teamRepository = TeamRepository()

def getCategoryDataUrl(categoryId):
    categoryUrl = urlRepository.getUrlByLabel("CategoryData")
    return categoryUrl.replace("CATEGORY_ID", str(categoryId))

def getCompetitionsDataUrl():
    return urlRepository.getUrlByLabel("Competition")

def getCategoryInfos(categoryId):
    return mojaRequests.sendGetRequest(getCategoryDataUrl(categoryId))

def getGridDataUrl(gridTableId):
    gridUrl = urlRepository.getUrlByLabel("GridData")
    return gridUrl.replace("GRID_ID", str(gridTableId))

def getGridDataUrlPoule(gridFftId):
    gridUrl = urlRepository.getUrlByLabel("GridDataPoule") #TODO
    return gridUrl.replace("GRID_ID", str(gridFftId))

def getPlayersUrl(homologationId):
    playersUrl = urlRepository.getUrlByLabel("Players")
    return playersUrl.replace("HOMOLOGATION_ID", str(homologationId))

def getTeamsUrl(homologationId):
    teamsUrl = urlRepository.getUrlByLabel("Teams")
    return teamsUrl.replace("HOMOLOGATION_ID", str(homologationId))

def getResultUrl(matchId):
    resultUrl = urlRepository.getUrlByLabel("Results")
    return resultUrl.replace("MATCH_ID", str(matchId))

def getConvocationsUrl(categoryFftId):
    resultUrl = urlRepository.getUrlByLabel("Convocations")
    return resultUrl.replace("CATEGORY_ID", str(categoryFftId))

def getCourtsUrl():
    return urlRepository.getUrlByLabel("Courts")

def getRankingsUrl():
    return urlRepository.getUrlByLabel("Rankings")

def getCompetitions():
    return mojaRequests.sendGetRequest(getCompetitionsDataUrl())

def getCourtsInformations():
    homologationId = competitionRepository.getHomologationId()
    courtsUrl = getCourtsUrl()
    data = {
        "queryInput": {
            "criteria": {
                "date": "2025-01-01T12:00",
                "homologationsChoisiesIdList": [
                    homologationId
                ]
            }
        }
    }
    return mojaRequests.sendPostRequestWithHeaders(courtsUrl, data)

def updateCourts():
    courtsInformations = getCourtsInformations()
    if courtsInformations is None:
        return None
    updateCourtsInDB(courtsInformations['list'])
    return 200

def updateRankings():
    rankingsInformations = getRankingsInfos()
    if rankingsInformations is None:
        return None
    updateRankingsInDB(rankingsInformations)

def updateRankingsInDB(rankings):
    rankingsToAdd = []
    for ranking in rankings:
        rankingsToAdd.append(Ranking.fromFFT(ranking))
    if rankingsToAdd:
        playerRepository.deleteAllPlayers()
        rankingRepository.deleteAllRankings()
        rankingRepository.addRankings(rankingsToAdd)

#TODO : Update instead of delete and add
def updateCourtsInDB(courts):
    courtsToAdd = []
    for court in courts:
        courtsToAdd.append(Court.fromFFT(court))
    if courtsToAdd:
        courtRepository.deleteAllCourts()
        courtRepository.addCourts(courtsToAdd)

#TODO : Update instead of delete and add
def updateCategories():
    #TODO categoriesPrices = settingRepository.getCategoriesPrices()
    homologationId = competitionRepository.getHomologationId()
    categoriesUrl = urlRepository.getUrlByLabel("Category")\
        .replace("HOMOLOGATION_ID", str(homologationId)) #TODO
    categories = mojaRequests.sendGetRequest(categoriesUrl)
    if categories is None:
        return None
    categoriesToAdd = []
    for category in categories:
        newCategory = Category.fromFFT(category)
        #TODO check amount
        # if "(C)" in newCategory.label:
        #     newCategory.amount = 0
        #     newCategory.code = newCategory.code.replace("S", "C")
        # elif newCategory.code.startswith("D"):
        #     newCategory.amount = categoriesPrices['doublePrice']
        # else :
        #     newCategory.amount = categoriesPrices['simplePrice']
        categoriesToAdd.append(newCategory)
    if categoriesToAdd:
        gridRepository.deleteAllGrids()
        categoryRepository.deleteAllCategories()
        categoryRepository.addCategories(categoriesToAdd)
    return 200

def updateAllMatches():
    courtsMap = courtRepository.getCourtsMap()
    playersIdMap = playerCategoriesRepository.getPlayersMap()
    teamsIdMap = teamRepository.getTeamsMap()
    nextGridMap = gridRepository.getNextGridsMap()
    gridsFFTMap = gridRepository.getGridsFFTMap()
    matchesMap = matchRepository.getMatchesMap()
    tempMatchesMap = {}
    report = UpdatedMatchReport(0, 0, 0)
    result = 200
    oldCategory = None
    matchIndex = 1
    newMatchs = []
    playersInfo = []
    for grid in gridRepository.getAllGrids():
        if oldCategory != grid.categoryId:
            matchIndex = 1
        matchAdded = updateMatches(newMatchs, matchesMap, tempMatchesMap, grid, gridsFFTMap, nextGridMap, matchIndex, report, courtsMap, playersIdMap, teamsIdMap, playersInfo)
        if matchAdded == 404:
            result = 404
        else:
            matchIndex += matchAdded
        oldCategory = grid.categoryId
    for match in newMatchs:
        if match.futurPlayer1 is not None and match.futurPlayer1 != "QE":
            match.futurPlayer1 = tempMatchesMap.get(str(match.futurPlayer1))
        if match.futurPlayer2 is not None and match.futurPlayer2 != "QE":
            match.futurPlayer2 = tempMatchesMap.get(str(match.futurPlayer2))
        if match.nextRound is not None:
            nextMatch = tempMatchesMap.get(str(match.nextRound))
            if nextMatch is not None:
                match.nextRound = nextMatch
            else:
                nextGrid = nextGridMap.get(match.nextRound)
                if nextGrid is not None:
                    match.nextRound = gridsFFTMap.get(nextGrid)
                else:
                    match.nextRound = None
    if newMatchs:
        matchRepository.addMatches(newMatchs)
    if matchesMap:
        matchRepository.deleteMatches([m.id for m in matchesMap.values()])
        report.deleted += len(matchesMap)
    message = report.createMessage()
    log.info(BATCH, message)
    return result

def updateGrids():
    for category in categoryRepository.getAllCategories():
        updateGrid(category.id, category.fftId, category.code)

#TODO : Update instead of delete and add
def updateGrid(categoryId, categoryFftId, categoryCode):
    categoryInfos = getCategoryInfos(categoryFftId)
    if categoryInfos is None:
        return 404
    gridsToAdd = []
    grids = sorted(categoryInfos, key=lambda x: x['decId'])
    for index, grid in enumerate(grids):
        newGrid = Grid.fromFFT(grid)
        newGrid.categoryId = categoryId
        if index != len(grids) - 1:
            newGrid.code = "T" + categoryCode + str(index + 1)
        else :
            newGrid.code = "TF" + categoryCode
        gridsToAdd.append(newGrid)
    if gridsToAdd:
        gridRepository.deleteAllGridsByCategory(categoryId)
        gridRepository.addGrids(gridsToAdd)
    return 200

def getConvocations(categoryFftId):
    url = getConvocationsUrl(categoryFftId)
    return mojaRequests.sendGetRequest(url)

def getPlayersInfos(homologationId):
    url = getPlayersUrl(homologationId)
    return mojaRequests.sendGetRequest(url)

def getTeamsInfos(homologationId):
    url = getTeamsUrl(homologationId)
    return mojaRequests.sendGetRequest(url)

def getRankingsInfos():
    url = getRankingsUrl()
    return mojaRequests.sendGetRequest(url)

def updateMatches(newMatchs, matchesMap, tempMatchesMap, grid, gridsFFTMap, nextGridMap, matchIndex, report, courtsMap, playersIdMap, teamsIdMap, playersInfo):
    matches = []
    #if grid.type == "POU": #TODO Poules
    #    url = getGridDataUrlPoule(grid.fftId)
    #else:
    url = getGridDataUrl(grid.tableId)
    matchesFromFFT = mojaRequests.sendGetRequest(url)
    if matchesFromFFT is None:
        return 404
    if grid.type != "POU" :
        sortedMatchs = sorted(matchesFromFFT, key=lambda x: getTuple(x["numeroMatch"]))
    else:
        sortedMatchs = matchesFromFFT
    for match in sortedMatchs:
        newMatch = createMatch(match, grid, courtsMap, grid.category.code, matchIndex, playersIdMap, teamsIdMap)
        matches.append(newMatch)
        matchIndex += 1
        tempMatchesMap[str(newMatch.fftId)] = newMatch.label
    for match in matches:
        matchInDB = matchesMap.get(match.fftId)
        if matchInDB:
            if match.isDifferent(matchInDB):
                match.id = matchInDB.id
                report.updated += 1
                matchRepository.updateMatchFromBatch(match)
            matchesMap.pop(match.fftId)
        else:
            newMatchs.append(match)
            report.added += 1
    return len(matches)

def getTuple(numeroMatch):
    value1 = int(numeroMatch.split('T')[1].split('M')[0])
    value2 = int(numeroMatch.split('M')[1])
    value3 = int(numeroMatch.split('Q')[1].split('T')[0])
    return (value1, value2, value3)

def createMatch(match, grid, courtsMap, categoryCode, matchIndex, playersIdMap, teamsIdMap):
    newMatch = Match.fromFFT(match)
    newMatch.categoryId = grid.categoryId
    newMatch.gridId = grid.id
    newMatch.double = match["epreuveIsDouble"]
    newMatch.courtId = courtsMap.get(int(match['courtId'])) if match['courtId'] is not None else None
    newMatch.label = categoryCode + str(matchIndex).zfill(2)
    setPlayersOrTeam(newMatch, match, playersIdMap, teamsIdMap)
    setNextRound(newMatch, match)
    setWinner(newMatch, match)
    setProgrammation(newMatch, match)
    return newMatch

def setPlayersOrTeam(match, matchData, playersIdMap, teamsIdMap):
    prec = 0
    qe = 0
    if matchData['insId1'] is None:
        if len(matchData['matchsPrecedents']) > 0:
            match.futurPlayer1 = str(matchData['matchsPrecedents'][0]['matchId'])
            prec += 1
        elif matchData['haveQe']:
            match.futurPlayer1 = "QE"
            qe += 1
    elif match.double:
        match.team1Id = getTeamId(matchData['insId1'], teamsIdMap)
    else:
        match.player1Id = getPlayerId(matchData['insId1'], playersIdMap)
    if matchData['insId2'] is None:
        if len(matchData['matchsPrecedents']) > prec:
            match.futurPlayer2 = str(matchData['matchsPrecedents'][prec]['matchId'])
        elif not qe and matchData['haveQe']: # TODO : 2 qe ?
            match.futurPlayer2 = "QE"
    elif match.double:
        match.team2Id = getTeamId(matchData['insId2'], teamsIdMap)
    else:
        match.player2Id = getPlayerId(matchData['insId2'], playersIdMap)

def setNextRound(match, matchData):
    if len(matchData['matchsSuivants']) > 0:
        match.nextRound = str(matchData['matchsSuivants'][0]['matchId'])
    else:
        match.nextRound = str(matchData['decoupageId'])

def setWinner(match, matchData):
    if matchData["insIdWin"] is None:
        return
    match.finish = True
    if match.double:
        if matchData["insIdWin"] == matchData['insId1']:
            match.teamWinnerId = match.team1Id
        else:
            match.teamWinnerId = match.team2Id
    else:
        if matchData["insIdWin"] == matchData['insId1']:
            match.winnerId = match.player1Id
        else:
            match.winnerId = match.player2Id
    setScore(match, matchData)

def setScore(match, matchData):
    score = ""
    for set in matchData["sets"]:
        if ["scoreA"] == 0 and set["scoreB"] == 0:
            break
        if score != "":
            score += " "
        if matchData["insIdWin"] == matchData['insId1']:
            score += str(set["scoreA"]) + "/" + str(set["scoreB"])
        else:
            score += str(set["scoreB"]) + "/" + str(set["scoreA"])
        if set["tieBreak"] is not None:
            score += "(" + str(set["tieBreak"]) + ")"
    match.score = score

def setProgrammation(match, matchData):
    if matchData["dateProgrammation"] and "T" in matchData["dateProgrammation"]:
        match.day = matchData["dateProgrammation"].split("T")[0]
        match.hour = matchData["dateProgrammation"].split("T")[1][:5]

def addRankings(categoryCode, rankingsToAdd, rankings):
    for ranking in rankings:
        if categoryCode.startswith("S"):
            newRanking = Ranking.fromFFT(ranking)
        if newRanking is not None and newRanking not in rankingsToAdd :
            rankingsToAdd.append(newRanking)

def getPlayerId(inscriptionId, playersIdMap):
    if inscriptionId is None:
        return None
    return playersIdMap.get(inscriptionId)

def getTeamId(inscriptionId, teamsIdMap):
    if inscriptionId is None:
        return None
    return teamsIdMap.get(inscriptionId).id

def setResult(matchFftId, winnerTeam, score):
    resultUlt = getResultUrl(matchFftId)
    sets = extractScore(score, winnerTeam)
    if sets is None:
        return 400
    data = {
        "equipeGagnante" : winnerTeam,
        "format": "1", #TODO : Enregistrer le format dans le match ou la catégorie ?
        "typeResultat" : "S", #TODO : Double ?
        "sets": sets
    }
    return mojaRequests.sendPostRequestWithHeaders(resultUlt, data)

def extractScore(score, winnerTeam):
    #TODO : Check with score construction
    setsToSend = []
    sets = score.split(" ")
    for index, set in enumerate(sets):
        scores = set.split("/")
        if "(" in score[1]:
            score[1] = score[1].split("(")[0] #TODO : Add tieBreak
        if winnerTeam == "equipeA":
            scoreA = scores[0]
            scoreB = scores[1]
        else:
            scoreA = scores[1]
            scoreB = scores[0]
        set = {
            "rank" : index+1,
            "scoreA" : scoreA,
            "scoreB" : scoreB
        }
        setsToSend.append(set)
    return setsToSend

class PlayersInfos:
    def __init__(self, fftId, email, phoneNumber):
        self.fftId = fftId
        self.email = email
        self.phoneNumber = phoneNumber

class UpdatedMatchReport:
    def __init__(self, updated, added, deleted):
        self.updated = updated
        self.added = added
        self.deleted = deleted

    def createMessage(self):
        return f"{constants.ADD_MATCHES}{self.added}\
            | {constants.UPDATE_MATCHES}{self.updated}\
            | {constants.DELETE_MATCHES}{self.deleted}"