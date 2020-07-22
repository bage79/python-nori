"""
Reference: https://github.com/apache/lucene-solr/blob/master/lucene/analysis/nori/src/test/org/apache/lucene/analysis/ko/TestKoreanTokenizer.java

TODO Test List.
 - test_reading
 - test_random_strings
 - test_random_huge_strings
 - test_random_huge_string_mock_graph_after
 - test_combining
"""

import os
import unittest
from configparser import ConfigParser

from pynori.korean_tokenizer import KoreanTokenizer, DcpdMode
from pynori.pos import POS

cfg = ConfigParser()
PATH_CUR = os.getcwd() + '/pynori'
cfg.read(PATH_CUR + '/config.ini')
# PATH
PATH_USER_DICT = cfg['PATH']['USER_DICT']

## Initization
print('KoreanTokenizer Initializing...')

tokenizer = KoreanTokenizer(verbose=False, path_userdict=PATH_USER_DICT, decompound_mode=DcpdMode.NONE, infl_decompound_mode=DcpdMode.NONE, output_unknown_unigrams=False, discard_punctuation=True)
tokenizer_with_punctuation = KoreanTokenizer(False, PATH_USER_DICT, DcpdMode.NONE, DcpdMode.DISCARD, False, False)
tokenizer_unigram = KoreanTokenizer(False, PATH_USER_DICT, DcpdMode.NONE, DcpdMode.DISCARD, True, True)
tokenizer_decompound = KoreanTokenizer(False, PATH_USER_DICT, DcpdMode.DISCARD, DcpdMode.DISCARD, False, True)
tokenizer_decompound_keep = KoreanTokenizer(False, PATH_USER_DICT, DcpdMode.MIXED, DcpdMode.MIXED, False, True)
tokenizer_infl_decompound_none = KoreanTokenizer(False, PATH_USER_DICT, DcpdMode.DISCARD, DcpdMode.NONE, False, True)
tokenizer_infl_decompound_mixed = KoreanTokenizer(False, PATH_USER_DICT, DcpdMode.DISCARD, DcpdMode.MIXED, False, True)


# analyzer_reading => test_korean_analyzer


class TestKoreanTokenizer(unittest.TestCase):

    def setUp(self):
        pass

    def do(self, kor_tokenizer, token_attr, in_string):
        kor_tokenizer.set_input(in_string)
        while kor_tokenizer.increment_token():
            pass
        tkn_attr_obj = kor_tokenizer.tkn_attr_obj
        return tkn_attr_obj.__dict__[token_attr]

    def test_spaces(self):
        self.assertEqual(self.do(tokenizer, 'termAtt', "화학        이외의         것"), ["화학", "이외", "의", "것"])
        self.assertEqual(self.do(tokenizer, 'offsetAtt', "화학        이외의         것"), [(0, 2), (10, 12), (12, 13), (22, 23)])
        self.assertEqual(self.do(tokenizer, 'posLengthAtt', "화학        이외의         것"), [1, 1, 1, 1])
        self.assertEqual(self.do(tokenizer, 'termAtt', "화학 이외의 것"), ["화학", "이외", "의", "것"])
        self.assertEqual(self.do(tokenizer, 'offsetAtt', "화학 이외의 것"), [(0, 2), (3, 5), (5, 6), (7, 8)])
        self.assertEqual(self.do(tokenizer, 'posLengthAtt', "화학 이외의 것"), [1, 1, 1, 1])

    def test_part_of_speechs(self):
        self.assertEqual(self.do(tokenizer, 'posTagAtt', "화학 이외의         것"), ['NNG', 'NNG', 'JKG', 'NNB'])

    def test_part_of_speechs_with_punc(self):
        self.assertEqual(self.do(tokenizer_with_punctuation, 'termAtt', "화학 이외의 것!"), ['화학', ' ', '이외', '의', ' ', '것', '!'])
        self.assertEqual(self.do(tokenizer_with_punctuation, 'posTagAtt', "화학 이외의 것!"), ['NNG', 'SP', 'NNG', 'JKG', 'SP', 'NNB', 'SF'])

    def test_floating_point_number(self):
        self.assertEqual(self.do(tokenizer_with_punctuation, 'termAtt', "10.1 인치 모니터"), ['10', '.', '1', ' ', '인치', ' ', '모니터'])
        self.assertEqual(self.do(tokenizer_with_punctuation, 'offsetAtt', "10.1 인치 모니터"), [(0, 2), (2, 3), (3, 4), (4, 5), (5, 7), (7, 8), (8, 11)])
        self.assertEqual(self.do(tokenizer_with_punctuation, 'posLengthAtt', "10.1 인치 모니터"), [1, 1, 1, 1, 1, 1, 1])

        self.assertEqual(self.do(tokenizer, 'termAtt', "10.1 인치 모니터"), ['10', '1', '인치', '모니터'])
        self.assertEqual(self.do(tokenizer, 'offsetAtt', "10.1 인치 모니터"), [(0, 2), (3, 4), (5, 7), (8, 11)])
        self.assertEqual(self.do(tokenizer, 'posLengthAtt', "10.1 인치 모니터"), [1, 1, 1, 1])

    def test_part_of_speechs_with_compound(self):
        self.assertEqual(self.do(tokenizer, 'termAtt', "가락지나물은 한국, 중국, 일본"), ['가락지나물', '은', '한국', '중국', '일본'])
        self.assertEqual(self.do(tokenizer, 'offsetAtt', "가락지나물은 한국, 중국, 일본"), [(0, 5), (5, 6), (7, 9), (11, 13), (15, 17)])
        self.assertEqual(self.do(tokenizer, 'posLengthAtt', "가락지나물은 한국, 중국, 일본"), [1, 1, 1, 1, 1])
        self.assertEqual(self.do(tokenizer, 'posTagAtt', "가락지나물은 한국, 중국, 일본"), ['NNG', 'JX', 'NNP', 'NNP', 'NNP'])
        self.assertEqual(self.do(tokenizer_decompound, 'termAtt', "가락지나물은 한국, 중국, 일본"), ['가락지', '나물', '은', '한국', '중국', '일본'])
        self.assertEqual(self.do(tokenizer_decompound, 'offsetAtt', "가락지나물은 한국, 중국, 일본"), [(0, 3), (3, 5), (5, 6), (7, 9), (11, 13), (15, 17)])
        self.assertEqual(self.do(tokenizer_decompound, 'posLengthAtt', "가락지나물은 한국, 중국, 일본"), [1, 1, 1, 1, 1, 1])
        self.assertEqual(self.do(tokenizer_decompound, 'posTagAtt', "가락지나물은 한국, 중국, 일본"), ['NNG', 'NNG', 'JX', 'NNP', 'NNP', 'NNP'])
        self.assertEqual(self.do(tokenizer_decompound_keep, 'termAtt', "가락지나물은 한국, 중국, 일본"), ['가락지나물', '가락지', '나물', '은', '한국', '중국', '일본'])
        self.assertEqual(self.do(tokenizer_decompound_keep, 'offsetAtt', "가락지나물은 한국, 중국, 일본"), [(0, 5), (0, 3), (3, 5), (5, 6), (7, 9), (11, 13), (15, 17)])
        self.assertEqual(self.do(tokenizer_decompound_keep, 'posLengthAtt', "가락지나물은 한국, 중국, 일본"), [2, 1, 1, 1, 1, 1, 1])
        self.assertEqual(self.do(tokenizer_decompound_keep, 'posTagAtt', "가락지나물은 한국, 중국, 일본"), ['NNG', 'NNG', 'NNG', 'JX', 'NNP', 'NNP', 'NNP'])

    def test_part_of_speechs_with_inflects(self):
        self.assertEqual(self.do(tokenizer, 'termAtt', "감싸여"), ['감싸여'])
        self.assertEqual(self.do(tokenizer, 'offsetAtt', "감싸여"), [(0, 3)])
        self.assertEqual(self.do(tokenizer, 'posLengthAtt', "감싸여"), [1])
        self.assertEqual(self.do(tokenizer, 'posTypeAtt', "감싸여"), [POS.Type.INFLECT])
        self.assertEqual(self.do(tokenizer, 'posTagAtt', "감싸여"), ['VV+EC'])
        self.assertEqual(self.do(tokenizer_decompound, 'termAtt', "감싸여"), ['감싸이', '어'])
        self.assertEqual(self.do(tokenizer_decompound, 'offsetAtt', "감싸여"), [(0, 3), (0, 3)])
        self.assertEqual(self.do(tokenizer_decompound, 'posLengthAtt', "감싸여"), [1, 1])
        self.assertEqual(self.do(tokenizer_decompound, 'posTypeAtt', "감싸여"), [POS.Type.MORPHEME, POS.Type.MORPHEME])
        self.assertEqual(self.do(tokenizer_decompound, 'posTagAtt', "감싸여"), ['VV', 'EC'])
        self.assertEqual(self.do(tokenizer_decompound_keep, 'termAtt', "감싸여"), ['감싸여', '감싸이', '어'])
        self.assertEqual(self.do(tokenizer_decompound_keep, 'offsetAtt', "감싸여"), [(0, 3), (0, 3), (0, 3)])
        self.assertEqual(self.do(tokenizer_decompound_keep, 'posLengthAtt', "감싸여"), [2, 1, 1])
        self.assertEqual(self.do(tokenizer_decompound_keep, 'posTypeAtt', "감싸여"), [POS.Type.INFLECT, POS.Type.MORPHEME, POS.Type.MORPHEME])
        self.assertEqual(self.do(tokenizer_decompound_keep, 'posTagAtt', "감싸여"), ['VV+EC', 'VV', 'EC'])

    def test_unknown_word(self):
        self.assertEqual(self.do(tokenizer, 'termAtt', "2018 평창 동계올림픽대회"), ['2018', '평창', '동계', '올림픽', '대회'])
        self.assertEqual(self.do(tokenizer, 'offsetAtt', "2018 평창 동계올림픽대회"), [(0, 4), (5, 7), (8, 10), (10, 13), (13, 15)])
        self.assertEqual(self.do(tokenizer, 'posLengthAtt', "2018 평창 동계올림픽대회"), [1, 1, 1, 1, 1])
        self.assertEqual(self.do(tokenizer, 'posTypeAtt', "2018 평창 동계올림픽대회"), [POS.Type.MORPHEME, POS.Type.MORPHEME, POS.Type.MORPHEME, POS.Type.MORPHEME, POS.Type.MORPHEME])
        self.assertEqual(self.do(tokenizer, 'posTagAtt', "2018 평창 동계올림픽대회"), ['SN', 'NNP', 'NNP', 'NNP', 'NNG'])
        self.assertEqual(self.do(tokenizer_unigram, 'termAtt', "2018 평창 동계올림픽대회"), ['2', '0', '1', '8', '평창', '동계', '올림픽', '대회'])
        self.assertEqual(self.do(tokenizer_unigram, 'offsetAtt', "2018 평창 동계올림픽대회"), [(0, 1), (1, 2), (2, 3), (3, 4), (5, 7), (8, 10), (10, 13), (13, 15)])
        self.assertEqual(self.do(tokenizer_unigram, 'posLengthAtt', "2018 평창 동계올림픽대회"), [1, 1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(self.do(tokenizer_unigram, 'posTypeAtt', "2018 평창 동계올림픽대회"),
                         [POS.Type.MORPHEME, POS.Type.MORPHEME, POS.Type.MORPHEME, POS.Type.MORPHEME, POS.Type.MORPHEME, POS.Type.MORPHEME, POS.Type.MORPHEME, POS.Type.MORPHEME])
        self.assertEqual(self.do(tokenizer_unigram, 'posTagAtt', "2018 평창 동계올림픽대회"), ['SN', 'SN', 'SN', 'SN', 'NNP', 'NNP', 'NNP', 'NNG'])

    # def test_reading(self):
    #	pass

    def test_userdict(self):
        self.assertEqual(self.do(tokenizer, 'termAtt', "c++ 프로그래밍 언어"), ['c++', '프로그래밍', '언어'])
        self.assertEqual(self.do(tokenizer, 'offsetAtt', "c++ 프로그래밍 언어"), [(0, 3), (4, 9), (10, 12)])
        self.assertEqual(self.do(tokenizer, 'posLengthAtt', "c++ 프로그래밍 언어"), [1, 1, 1])
        self.assertEqual(self.do(tokenizer, 'posTypeAtt', "c++ 프로그래밍 언어"), [POS.Type.MORPHEME, POS.Type.MORPHEME, POS.Type.MORPHEME])
        self.assertEqual(self.do(tokenizer, 'posTagAtt', "c++ 프로그래밍 언어"), ['NNG', 'NNG', 'NNG'])
        self.assertEqual(self.do(tokenizer_decompound, 'termAtt', "정부세종청사"), ['정부', '세종', '청사'])
        self.assertEqual(self.do(tokenizer_decompound, 'offsetAtt', "정부세종청사"), [(0, 2), (2, 4), (4, 6)])
        self.assertEqual(self.do(tokenizer_decompound, 'posLengthAtt', "정부세종청사"), [1, 1, 1])
        self.assertEqual(self.do(tokenizer_decompound, 'posTypeAtt', "정부세종청사"), [POS.Type.MORPHEME, POS.Type.MORPHEME, POS.Type.MORPHEME])
        self.assertEqual(self.do(tokenizer_decompound, 'posTagAtt', "정부세종청사"), ['NNG', 'NNG', 'NNG'])
        self.assertEqual(self.do(tokenizer, 'termAtt', "대한민국날씨"), ['대한민국날씨'])
        self.assertEqual(self.do(tokenizer, 'offsetAtt', "대한민국날씨"), [(0, 6)])
        self.assertEqual(self.do(tokenizer, 'posLengthAtt', "대한민국날씨"), [1])
        self.assertEqual(self.do(tokenizer, 'posTypeAtt', "대한민국날씨"), [POS.Type.MORPHEME])
        self.assertEqual(self.do(tokenizer, 'posTagAtt', "대한민국날씨"), ['NNG'])
        self.assertEqual(self.do(tokenizer, 'termAtt', "21세기대한민국"), ['21세기대한민국'])
        self.assertEqual(self.do(tokenizer, 'offsetAtt', "21세기대한민국"), [(0, 8)])
        self.assertEqual(self.do(tokenizer, 'posLengthAtt', "21세기대한민국"), [1])
        self.assertEqual(self.do(tokenizer, 'posTypeAtt', "21세기대한민국"), [POS.Type.MORPHEME])
        self.assertEqual(self.do(tokenizer, 'posTagAtt', "21세기대한민국"), ['NNG'])

    def test_inter_punct(self):
        self.assertEqual(self.do(tokenizer, 'termAtt', "도로ㆍ지반ㆍ수자원ㆍ건설환경ㆍ건축ㆍ화재설비연구"), ['도로', '지반', '수자원', '건설', '환경', '건축', '화재', '설비', '연구'])
        self.assertEqual(self.do(tokenizer, 'offsetAtt', "도로ㆍ지반ㆍ수자원ㆍ건설환경ㆍ건축ㆍ화재설비연구"), [(0, 2), (3, 5), (6, 9), (10, 12), (12, 14), (15, 17), (18, 20), (20, 22), (22, 24)])
        self.assertEqual(self.do(tokenizer, 'posLengthAtt', "도로ㆍ지반ㆍ수자원ㆍ건설환경ㆍ건축ㆍ화재설비연구"), [1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(self.do(tokenizer, 'posTagAtt', "도로ㆍ지반ㆍ수자원ㆍ건설환경ㆍ건축ㆍ화재설비연구"), ['NNG', 'NNG', 'NNG', 'NNG', 'NNG', 'NNG', 'NNG', 'NNG', 'NNG'])

    def test_infl_mode(self):
        self.assertEqual(self.do(tokenizer_infl_decompound_none, 'termAtt', "가벼운 냉장고"), ['가벼운', '냉장', '고'])
        self.assertEqual(self.do(tokenizer_infl_decompound_mixed, 'termAtt', "가벼운 냉장고"), ['가벼운', '가볍', 'ᆫ', '냉장', '고'])

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
