from pynori.token import Token


class DecompoundToken(Token):
    """
    A token that was generated from a compound
    """

    def __init__(self, posTag, surfaceForm, startOffset, endOffset, posType, dictType):
        super().__init__(surfaceForm, 0, len(surfaceForm), startOffset, endOffset, posType, None, posTag, dictType)
# self.posTag = posTag

# @Override
# def getPOSType(self):
#    """ Get the {@link POS.Type} of the token. """
#    return POS.Type.MORPHEME

# @Override
# def getLeftPOS(self):
#    """ Get the left part of speech of the token. """
#    return self.posTag

# @Override
# def getRightPOS(self):
#    """ Get the right part of speech of the token. """
#    return self.posTag

# @Override
# def getReading(self):
#    """ Get the reading of the token. """
#    return None

# @Override
# def getMorphemes(self):
#    """ Get the {@link Morpheme} decomposition of the token. """
#    return None
