from Entities import *
from random import shuffle
from copy import deepcopy


class FactsRepository:
    def __init__(self, fileName):
        self.__facts = []
        self.__fileName = fileName
        self.__readFile()

    def add(self, fact, reading = False):
        self.__facts.append(fact)
        if not reading:
            self.__appendToFile(fact)

    def updateThumbsUp(self, fact):
        for f in self.__facts:
            if f.getText() == fact.getText():
                f.incrementThumbsUp()
        self.__writeToFile()

    def updateThumbsDown(self, fact):
        for f in self.__facts:
            if f.getText() == fact.getText():
                f.incrementThumbsDown()
        self.__writeToFile()

    def getAll(self):
        return deepcopy(self.__facts)

    def __appendToFile(self, fact):
        with open(self.__fileName, 'a+') as f:
            f.write(fact.toFile())

    def __writeToFile(self):
        with open(self.__fileName, 'w') as f:
            for fact in self.__facts:
                f.write(fact.toFile())

    def __readFile(self):
        file = open(self.__fileName, 'r')
        lines = file.readlines()
        for l in lines:
            l = l.split('|')
            self.add(Fact(l[0], l[1], int(l[2]), int(l[3])), True)
        file.close()

class ShuffledFactsRepository:
    def __init__(self, fileName, factsRepo):
        self.__shuffled = []
        self.__fileName = fileName
        self.__factsRepo = factsRepo
        self.__readFile()

    def __shuffleAgain(self):
        facts = self.__factsRepo.getAll()
        shuffle(facts)
        self.__shuffled = facts

    def add(self, fact, reading = False):
        self.__shuffled.append(fact)
        if not reading:
            self.__appendToFile(fact)

    def pop(self):
        if len(self.__shuffled) == 0:
            self.__shuffleAgain()
        first = self.__shuffled[0]
        self.__shuffled = self.__shuffled[1:]
        self.__writeToFile()
        return first

    def updateThumbsUp(self, fact):
        for s in self.__shuffled:
            if s.getText() == fact.getText():
                s.incrementThumbsUp()
        self.__writeToFile()

    def updateThumbsDown(self, fact):
        for s in self.__shuffled:
            if s.getText() == fact.getText():
                s.incrementThumbsDown()
        self.__writeToFile()

    def __appendToFile(self, fact):
        with open(self.__fileName, 'a+') as f:
            f.write(fact.toFile())

    def __writeToFile(self):
        with open(self.__fileName, 'w') as f:
            for fact in self.__shuffled:
                f.write(fact.toFile())

    def __readFile(self):
        file = open(self.__fileName, 'r')
        lines = file.readlines()
        for l in lines:
            l = l.split('|')
            self.add(Fact(l[0], l[1], int(l[2]), int(l[3])), True)
        file.close()


class PunishedUsersRepository:
    def __init__(self, fileName):
        self.__users = []
        self.__fileName = fileName
        self.__readFile()

    def add(self, user, reading = False):
        self.__users.append(user)
        if not reading:
            self.__appendToFile(user)

    def remove(self, user):
        toRemove = self.getById(user.getUserId())
        self.__users.remove(toRemove)
        self.__writeToFile()

    def getById(self, userId):
        return next((x for x in self.__users if x.getUserId() == userId), None)

    def __appendToFile(self, user):
        with open(self.__fileName, 'a+') as f:
            f.write(user.toFile())

    def __writeToFile(self):
        with open(self.__fileName, 'w') as f:
            for user in self.__users:
                f.write(user.toFile())

    def __readFile(self):
        file = open(self.__fileName, 'r')
        lines = file.readlines()
        for l in lines:
            l = l.split(',')
            self.add(PunishedUser(int(l[0]), float(l[1])), True)
        file.close()

    def clearData(self):
        open(self.__fileName, 'w').close()
        self.__users = []


class TeasingInfoRepository:
    def __init__(self, fileName):
        self.__teaseActs = []
        self.__fileName = fileName
        self.__readFile()

    def add(self, tease, reading = False):
        self.__teaseActs.append(tease)
        if not reading:
            self.__appendToFile(tease)

    def remove(self, tease):
        toRemove = self.getById(tease.getTeasedId())
        self.__teaseActs.remove(toRemove)
        self.__writeToFile()

    def getById(self, teasedId):
        return next((x for x in self.__teaseActs if x.getTeasedId() == teasedId), None)

    def __appendToFile(self, tease):
        with open(self.__fileName, 'a+') as f:
            f.write(tease.toFile())

    def __writeToFile(self):
        with open(self.__fileName, 'w') as f:
            for tease in self.__teaseActs:
                f.write(tease.toFile())

    def __readFile(self):
        file = open(self.__fileName, 'r')
        lines = file.readlines()
        for l in lines:
            l = l.split('~')
            self.add(Tease(int(l[0]), int(l[1]), l[2][:-1]), True)
        file.close()

    def clearData(self):
        open(self.__fileName, 'w').close()
        self.__teaseActs = []

class TeasedRepository:
    def __init__(self, fileName):
        self.__users = []
        self.__fileName = fileName
        self.__readFile()

    def add(self, user, reading = False):
        self.__users.append(user)
        if not reading:
            self.__appendToFile(user)

    def remove(self, user):
        toRemove = self.getById(user.getUserId())
        self.__users.remove(toRemove)
        self.__writeToFile()

    def getById(self, userId):
        return next((x for x in self.__users if x.getUserId() == userId), None)

    def __appendToFile(self, user):
        with open(self.__fileName, 'a+') as f:
            f.write(user.toFile())

    def __writeToFile(self):
        with open(self.__fileName, 'w') as f:
            for user in self.__users:
                f.write(user.toFile())

    def __readFile(self):
        file = open(self.__fileName, 'r')
        lines = file.readlines()
        for l in lines:
            l = l.split(',')
            self.add(TeasedUser(int(l[0]), float(l[1])), True)
        file.close()

    def clearData(self):
        open(self.__fileName, 'w').close()
        self.__users = []

class TypingUsersRepository:
    def __init__(self, fileName):
        self.__users = []
        self.__fileName = fileName

    def add(self, userId):
        self.__users.append(userId)
        self.__appendToFile(userId)

    def remove(self, userId):
        self.__users.remove(userId)
        self.__writeToFile()

    def isInList(self, userId):
        return userId in self.__users

    def __appendToFile(self, userId):
        with open(self.__fileName, 'a+') as f:
            f.write(f'{userId}\n')

    def __writeToFile(self):
        with open(self.__fileName, 'w') as f:
            for user in self.__users:
                f.write(f'{user}\n')