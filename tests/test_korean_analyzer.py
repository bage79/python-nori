"""
Reference: https://github.com/apache/lucene-solr/blob/master/lucene/analysis/nori/src/test/org/apache/lucene/analysis/ko/TestKoreanAnalyzer.java
"""

import unittest

from pynori.korean_analyzer import KoreanAnalyzer
from pynori.korean_tokenizer import DcpdMode
from pynori.synonym_graph_filter import SynMode

## Initization
print('KoreanAnalyzer Initializing...')
analyzer = KoreanAnalyzer(pos_filter=True, decompound_mode=DcpdMode.DISCARD)
analyzer_stoptags = KoreanAnalyzer(pos_filter=True, stop_tags=['NNP', 'NNG'], decompound_mode=DcpdMode.DISCARD)
analyzer_stoptags_infl = KoreanAnalyzer(pos_filter=True, stop_tags=['ETM', 'EP'], decompound_mode=DcpdMode.MIXED, infl_decompound_mode=DcpdMode.MIXED)
analyzer_synonym = KoreanAnalyzer(decompound_mode=DcpdMode.DISCARD, infl_decompound_mode=DcpdMode.DISCARD, discard_punctuation=True, output_unknown_unigrams=False, pos_filter=False,
                                  stop_tags=['JKS', 'JKB', 'VV', 'EF'], synonym_filter=True, mode_synonym=SynMode.NORM)


class TestKoreanAnalyzer(unittest.TestCase):

    def setUp(self):
        pass

    def do(self, kor_analyzer, token_attr, in_string):
        return kor_analyzer.do_analysis(in_string)[token_attr]

    def test_stoptags(self):
        self.assertEqual(self.do(analyzer, 'termAtt', "한국은 대단한 나라입니다."), ['한국', '대단', '나라', '이'])
        self.assertEqual(self.do(analyzer, 'offsetAtt', "한국은 대단한 나라입니다."), [(0, 2), (4, 6), (8, 10), (10, 13)])
        self.assertEqual(self.do(analyzer, 'posLengthAtt', "한국은 대단한 나라입니다."), [1, 1, 1, 1])
        self.assertEqual(self.do(analyzer_stoptags, 'termAtt', "한국은 대단한 나라입니다."), ['은', '대단', '하', 'ᆫ', '이', 'ᄇ니다'])
        self.assertEqual(self.do(analyzer_stoptags, 'offsetAtt', "한국은 대단한 나라입니다."), [(2, 3), (4, 6), (6, 7), (6, 7), (10, 13), (10, 13)])
        self.assertEqual(self.do(analyzer_stoptags, 'posLengthAtt', "한국은 대단한 나라입니다."), [1, 1, 1, 1, 1, 1])

    def test_stoptags_infl(self):
        self.assertEqual(self.do(analyzer_stoptags_infl, 'termAtt', "가벼운 냉장고"), ['가볍', '냉장고', '냉장', '고'])
        self.assertEqual(self.do(analyzer_stoptags_infl, 'termAtt', "들어가신다"), ['들어가', 'ㄴ다'])

    def test_synonym(self):
        self.assertEqual(self.do(analyzer_synonym, 'termAtt', "NLP 개발자"), ['자연어', '처리', '개발', '자'])

        analyzer_synonym.set_option_tokenizer(decompound_mode=DcpdMode.MIXED, infl_decompound_mode=DcpdMode.MIXED)
        analyzer_synonym.set_option_filter(mode_synonym=SynMode.EXT)
        self.assertEqual(self.do(analyzer_synonym, 'termAtt', "AI 개발자"), ['인공지능', '인공', '지능', 'ai', 'aritificial', 'intelligence', '개발자', '개발', '자', 'developer'])

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
