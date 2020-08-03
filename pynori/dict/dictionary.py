class Dictionary(object):  # Abstract Class
    """
    Dictionary interface for retrieving morphological data by id

    dictionary class는 모두 dictionary로부터 단어 정보를 불러오는 get 함수들로 구성.
    pyNori 버전에서는 token에 그대로 모든 단어 정보들을 다 포함되므로 wordID를 사용하면서 dictionary에 접근하지 않음.
    따라서 dictionary class는 pyNori에서는 Morpheme 만 사용.
    """

    def __init__(self):
        pass

    class Morpheme(object):
        """A morpheme extracted from a compound token."""

        def __init__(self, posTag, surfaceForm):
            self.posTag = posTag
            self.surfaceForm = surfaceForm


# def __getstate__(self):
#    return self.__dict__
#    #return {'posTag': self.posTag, 'surfaceForm': self.surfaceForm}

# def __setstate__(self, dct):
#    self.__dict__ = dct
#    #self.posTag = dct['posTag']
#    #self.surfaceForm = dct['surfaceForm']


"""
    def getLeftId(self, wordId: "int") -> int:
        ## Get left id of specified word 
        raise NotImplementedError("The method not implemented")
        
    def getRightId(self, wordId: "int") -> int:
        ## Get right id of specified word
        raise NotImplementedError("The method not implemented")
        
    def getWordCost(self, wordId: "int") -> int:
        ## Get word cost of specified word
        raise NotImplementedError("The method not implemented")

    def getPOSType(self, wordId: "int") -> POS.Type:
        ## Get the POS.Type of specified word (morpheme, compound, inflect or pre-analysis)
        raise NotImplementedError("The method not implemented")
        
    def getLeftPOS(self, wordId: "int") -> POS.Type:
        ## Get the left POS.Tag of specified word.
        ## For POS.Type.MORPHEME} and POS.Type.COMPOUND the left and right POS are the same.
        raise NotImplementedError("The method not implemented")
        
    def getRightPOS(self, wordId: "int") -> POS.Type:
        ## Get the right POS.Tag of specified word.
        ## For POS.Type.MORPHEME and POS.Type.COMPOUND the left and right POS are the same.
        raise NotImplementedError("The method not implemented")        
        
    def getReading(self, wordId: "int"):
        ## Get the reading of specified word (mainly used for Hanja to Hangul conversion).
        # return String
        raise NotImplementedError("The method not implemented")        
        
    def getMorphemes(self, wordId: "int", surfaceForm: "char[]", off: "int", len: "int"):
        ## Get the morphemes of specified word (e.g. 가깝으나: 가깝 + 으나).
        # return Morpheme[]
        raise NotImplementedError("The method not implemented")
"""
