class Fact:
    def __init__(self, text, author = '', thumbsUp = 0, thumbsDown = 0):
        self.__text = text
        self.__author = author
        self.__thumbsUp = thumbsUp
        self.__thumbsDown = thumbsDown

    def __str__(self):
        return f'{self.__text}(added by: {self.__author}); thumbsUp:{self.__thumbsUp}; thumbsDown:{self.__thumbsDown}'

    def getText(self):
        return self.__text

    def getAuthor(self):
        return self.__author

    def getThumbsUp(self):
        return self.__thumbsUp

    def getThumbsDown(self):
        return self.__thumbsDown

    def incrementThumbsUp(self):
        self.__thumbsUp += 1

    def incrementThumbsDown(self):
        self.__thumbsDown += 1

    def toFile(self):
        return f'{self.__text}|{self.__author}|{self.__thumbsUp}|{self.__thumbsDown}\n'


class PunishedUser:
    def __init__(self, userId, timer = 0):
        self.__userId = userId
        self.__timer = timer

    def getUserId(self):
        return self.__userId

    def getTimer(self):
        return self.__timer

    def toFile(self):
        return f'{self.__userId},{self.__timer}\n'


class TeasedUser(PunishedUser):
    def __init__(self, userId, timer = 0):
        super().__init__(userId, timer)

    def getUserId(self):
        return super().getUserId()

    def getTimer(self):
        return super().getTimer()

    def toFile(self):
        return super().toFile()


class Tease:
    def __init__(self, teasedId, teaserId = None, keyText = ''):
        self.__teasedId = teasedId
        self.__teaserId = teaserId
        self.__keyText = keyText

    def getTeasedId(self):
        return self.__teasedId

    def getTeaserId(self):
        return self.__teaserId

    def getKeyText(self):
        return self.__keyText

    def toFile(self):
        return f'{self.__teasedId}~{self.__teaserId}~{self.__keyText}\n'
