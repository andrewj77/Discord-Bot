from Repositories import *


class FactsController:
    def __init__(self, factsRepo, shuffledFactsRepo):
        self.__factsRepo = factsRepo
        self.__shuffledFactsRepo = shuffledFactsRepo

    def factsIterate(self):
        return self.__factsRepo.getAll()

    def addFact(self, text, author, thumbsUp = 0, thumbsDown = 0):
        fact = Fact(text, author, thumbsUp, thumbsDown)
        self.__factsRepo.add(fact)
        self.__shuffledFactsRepo.add(fact)

    def getRandomFact(self):
        return self.__shuffledFactsRepo.pop()

    def getDescendingSortedFacts(self):
        facts = self.__factsRepo.getAll()
        facts.sort(key=lambda x: x.getThumbsUp() - x.getThumbsDown(), reverse=True)
        return facts

    def updateThumbsUp(self, text):
        fact = Fact(text)
        self.__factsRepo.updateThumbsUp(fact)
        self.__shuffledFactsRepo.updateThumbsUp(fact)

    def updateThumbsDown(self, text):
        fact = Fact(text)
        self.__factsRepo.updateThumbsDown(fact)
        self.__shuffledFactsRepo.updateThumbsDown(fact)

class PunishedUserController:
    def __init__(self, userRepo):
        self.__userRepo = userRepo

    def addUser(self, userId, timer):
        user = PunishedUser(userId, timer)
        self.__userRepo.add(user)

    def removeUser(self, userId):
        user = PunishedUser(userId)
        self.__userRepo.remove(user)

    def getUserById(self, userId):
        return self.__userRepo.getById(userId)

    def clearData(self):
        self.__userRepo.clearData()

class TeasingInfoController:
    def __init__(self, teaseRepo):
        self.__teaseRepo = teaseRepo

    def addTease(self, teasedId, teaserId, keyText):
        tease = Tease(teasedId, teaserId, keyText)
        self.__teaseRepo.add(tease)

    def removeTease(self, teaseId):
        tease = Tease(teaseId)
        self.__teaseRepo.remove(tease)

    def getTeaseByTeasedId(self, teasedId):
        return self.__teaseRepo.getById(teasedId)

    def clearData(self):
        self.__teaseRepo.clearData()


class TeasedController:
    def __init__(self, userRepo):
        self.__userRepo = userRepo

    def addUser(self, userId, timer):
        user = TeasedUser(userId, timer)
        self.__userRepo.add(user)

    def removeUser(self, userId):
        user = TeasedUser(userId)
        self.__userRepo.remove(user)

    def getTeasedUserById(self, userId):
        return self.__userRepo.getById(userId)

    def clearData(self):
        self.__userRepo.clearData()


class TypingUsersController:
    def __init__(self, userRepo):
        self.__userRepo = userRepo

    def addUser(self, userId):
        self.__userRepo.add(userId)

    def removeUser(self, userId):
        self.__userRepo.remove(userId)

    def isUserInRepo(self, userId):
        return self.__userRepo.isInList(userId)

