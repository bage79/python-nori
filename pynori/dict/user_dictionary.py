from pynori.dict.dictionary import Dictionary
from pynori.dict.character_definition import CharacterDefinition
from pynori.dict.trie import Trie
from pynori.pos import POS


class UserDictionary(Dictionary):
    """Build User Dictionary
    """

    WORD_COST = -100000
    LEFT_ID = 1781  # NNG left
    RIGHT_ID = 3533  # NNG right
    RIGHT_ID_T = 3535  # NNG right with hangul and a coda on the last char
    RIGHT_ID_F = 3534  # NNG right with hangul and no coda on the last char
    USER_POS = 'NNG'

    @staticmethod
    def open(USER_PATH):
        entries = []
        with open(USER_PATH, 'r', encoding='UTF8') as rf:
            for line in rf:
                line = line.strip()
                if len(line) == 0:
                    continue
                if line[:2] == '# ':  # 주석 line
                    continue
                entries.append(line)
        if len(entries) == 0:
            return None
        else:
            return UserDictionary(entries)

    def __init__(self, entries):
        charDef = CharacterDefinition()
        # 복합명사 우선 순위 & 중복 단어 제거를 위해 정렬
        # entries = sorted(entries)
        entries = sorted(entries, reverse=True)
        self.userTrie = Trie()
        lastToken = ""
        segmentations = []
        rightIds = []
        ord = 0

        for entry in entries:
            splits = entry.split()
            token = splits[0]
            rightId = ""

            if token == lastToken:
                continue

            lastChar = list(entry)[0]
            if charDef.isHangul(lastChar):
                if charDef.hasCoda(lastChar):
                    rightId = self.RIGHT_ID_T
                    # rightIds.append(RIGHT_ID_T)
                else:
                    rightId = self.RIGHT_ID_F
                    # rightIds.append(RIGHT_ID_F)
            else:
                rightId = self.RIGHT_ID
                # rightIds.append(RIGHT_ID)

            if len(splits) == 1:
                # segmentations.append(None)
                pass
            else:
                length = []
                offset = 0
                for i in range(1, len(splits)):
                    length.append(len(splits[i]))
                    offset += len(splits[i])
                if offset > len(token):
                    raise Exception("Illegal user dictionary entry '{}' - the segmentation is bigger than the surface form ({})".format(entry, token))
                # segmentations.append(length)

            # add mapping to Trie (similar to FST)
            morph_inf = dict()
            morph_inf['surface'] = token
            morph_inf['left_id'] = self.LEFT_ID
            morph_inf['right_id'] = rightId
            morph_inf['word_cost'] = int(self.WORD_COST)
            morph_inf['POS'] = self.USER_POS
            if len(splits) == 1:
                morph_inf['POS_type'] = POS.Type.MORPHEME
                # morph_inf['analysis'] = token
                morph_inf['morphemes'] = None
                self.userTrie.insert(token, morph_inf)
            else:
                morph_inf['POS_type'] = POS.Type.COMPOUND
                # morph_inf['analysis'] = ' '.join(splits[1:]) # decompounded form
                morphemes_list = []
                for subword in splits[1:]:
                    morphemes_list.append(Dictionary.Morpheme(posTag=self.USER_POS, surfaceForm=subword))
                morph_inf['morphemes'] = morphemes_list
                self.userTrie.insert(token, morph_inf)

            lastToken = token
            # ord += 1

        # self.userTrie = userTrie
        # self.segmentations = segmentations
        # self.rightIds = rightIds


"""
    #@override
    def getMorphemes(self, wordId, surfaceForm, off, len):
        ## Get the morphemes of specified word (e.g. 가깝으나: 가깝 + 으나). 
        # return Morpheme[]
        raise NotImplementedError("The method not implemented")

    #@override
    def getLeftId(self, wordId):
        return LEFT_ID
    
    #@override
    def getRighId(self, wordId):
        return self.rightIds[wordId]
        
    #@override
    def getWordCost(self, wordId):
        return WORD_COST
        
    #@override
    def getPOSType(self, wordId):
        if self.segmentations[wordId] == None:
            return POS.Type.MORPHEME
        else:
            return POS.Type.COMPOUND
    
    #@override
    def getLeftPOS(self, wordId):
        return POS.Tag.NNG
        
    #@override
    def getRightPOS(self, wordId):
        return POS.Tag.NNG
"""
