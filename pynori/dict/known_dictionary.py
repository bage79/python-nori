import gc
import gzip
import os
import pickle

from appliednl_faq.utils.memory_leak_util import MemoryLeakUtil
from pynori.dict.dictionary import Dictionary
# from pynori.dict.character_definition import CharacterDefinition
from pynori.dict.trie import Trie


class KnownDictionary(Dictionary):
    """Buid Known Dictionary (or System Dictionary)

    Load korean words from mecab-ko-dic
    Loaded words will be used as system words
    """

    @staticmethod
    def open(KNOWN_PATH):

        # entries = []
        # for dirName, subdirList, fileList in os.walk(KNOWN_PATH):
        #    for fname in fileList:
        #        if fname.split('.')[-1] == 'csv':
        #            PATH_EACH = dirName + '/' + fname
        #            #with open(PATH_EACH, 'r', encoding='UTF8') as rf: 
        #            #    for line in rf:
        #            #        line = line.strip()
        #            #        if len(line) == 0:
        #            #            continue
        #            #        entries.append(line)
        #            entries += open(PATH_EACH, 'r', encoding='UTF8').readlines()
        if not os.path.isfile(KNOWN_PATH):
            pass

        with gzip.open(KNOWN_PATH, 'rb') as rf:
            entries = pickle.load(rf)  # csv 데이터를 포함한 Trie 자료구조.

        if len(entries) == 0:
            return None
        else:
            return KnownDictionary(entries)

    def __init__(self, entries):
        # charDef = CharacterDefinition()
        # entries = sorted(entries)

        self.sysTrie = Trie()

        for token, morph_inf in entries:
            if morph_inf['morphemes'] is not None:
                morphemes_list = []
                for subpos, subword in morph_inf['morphemes']:
                    morphemes_list.append(Dictionary.Morpheme(posTag=subpos, surfaceForm=subword))
                morph_inf['morphemes'] = morphemes_list
            self.sysTrie.insert(token, morph_inf)

        """
        self.sysTrie = Trie()
        for entry in entries:
            entry = entry.strip()

            # Use shlex. 
            # to deal with the case: ",",1792,3558,788,SC,*,*,*,*,*,*,*
            shlex_splitter = shlex.shlex(entry, posix=True)
            shlex_splitter.whitespace = ','
            shlex_splitter.whitespace_split = True
            splits = list(shlex_splitter)
            #splits = entry.split(',')
                        
            token = splits[0]
            
            morph_inf = dict()
            morph_inf['surface'] = splits[0]
            morph_inf['left_id'] = splits[1]
            morph_inf['right_id'] = splits[2]
            morph_inf['word_cost'] = int(splits[3])
            morph_inf['POS'] = splits[4]

            if splits[8] == '*':
                morph_inf['POS_type'] = POS.Type.MORPHEME
                morph_inf['morphemes'] = None
            else:
                mecab_pos_type_naming = splits[8].upper()
                if mecab_pos_type_naming == 'COMPOUND':
                    morph_inf['POS_type'] = POS.Type.COMPOUND
                elif mecab_pos_type_naming == 'INFLECT':
                    morph_inf['POS_type'] = POS.Type.INFLECT
                elif mecab_pos_type_naming == 'PREANALYSIS':
                    morph_inf['POS_type'] = POS.Type.PREANALYSIS
                else:
                    morph_inf['POS_type'] = mecab_pos_type_naming
        
                if len(splits[11].split('+')) == 1: # Compound인데 1개면 잘못 명시한 케이스 (확인 필요. 오류?)
                    # 예외처리 (ex. 개태,1783,3538,3534,NNP,*,F,개태,Compound,*,*,*)
                    morph_inf['POS_type'] = POS.Type.MORPHEME # Compound인데 토큰이 1개니까 그냥 MORPHEME으로 처리
                    morph_inf['morphemes'] = None
                else: # 2개 이상: 정상적인 COMPOUND
                    morphemes_list = []
                    for substr in splits[11].split('+'):
                        # substr = 목/NNG/*+매기/NNG/*+송아지/NNG/*
                        subword = substr.split('/')[0]
                        subpos = substr.split('/')[1]
                        morphemes_list.append(Dictionary.Morpheme(posTag=subpos, surfaceForm=subword))
                    morph_inf['morphemes'] = morphemes_list

            #morph_inf['analysis'] = splits[11]
            # 짐수레꾼,1781,3535,2835,NNG,*,T,짐수레꾼,Compound,*,*,짐/NNG/*+수레/NNG/*+꾼/NNG/*
            self.sysTrie.insert(token, morph_inf)
        """


"""
    #@override
    def getLeftId(self, wordId):
        return None
    
    #@override
    def getRighId(self, wordId):
        return None
        
    #@override
    def getWordCost(self, wordId):
        return None
        
    #@override
    def getPOSType(self, wordId):
        return None
    
    #@override
    def getLeftPOS(self, wordId):
        return None
        
    #@override
    def getRightPOS(self, wordId):
        return None
"""
