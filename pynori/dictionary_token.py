from pynori.token import Token


# from pynori.src.koreantokenizer import Type # TODO: circular import problem


class DictionaryToken(Token):  # Abstract Class
    """
    Dictionary interface for retrieving morphological data by id
    """

    def __init__(self, dictType, dictionary, wordId, surfaceForm, offset, length,
                 startOffset, endOffset, posType, morphemes, posTag):
        super().__init__(surfaceForm, offset, length, startOffset, endOffset, posType, morphemes, posTag, dictType)
        self.dictType = dictType  # KoreanTokenizer.Type type
        self.dictionary = dictionary
        self.wordId = wordId

    def getType(self):
        return self.dictType

# def isKnown(self):
#	return self.dictType == Type.KNOWN

# def isUnknown(self):
#	return self.dictType == Type.UNKNOWN

# def isUser(self):
#	return self.dictType == Type.USER

# @Override
# def getPOSType(self):
#	return self.dictionary.getPOSType(self.wordId)

# @Override
# def getLeftPOS(self):
#	return self.dictionary.getLeftPOS(self.wordId)

# @Override
# def getRightPOS(self):
#	return self.dictionary.getRightPOS(self.wordId)

# @Override
# def getReading(self):
#	return self.dictionary.getReading(self.wordId)

# @Override
# def getMorphemes(self):
#	return self.dictionary.getMorphemes(self.wordId, super().getSurfaceForm(), super().getOffset(), super().getLength())
#	dictionary 에서 빼오는 작업은 하지 않는다.
