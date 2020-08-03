import copy
import gc
import os
from configparser import ConfigParser

from pynori.korean_posstop_filter import KoreanPOSStopFilter
from pynori.korean_tokenizer import DcpdMode
from pynori.korean_tokenizer import KoreanTokenizer
from pynori.preprocessing import Preprocessing
from pynori.synonym_graph_filter import SynonymGraphFilter

cfg = ConfigParser()
# PATH_CUR = os.getcwd() + '/pynori'
PATH_CUR = os.path.dirname(__file__)
cfg.read(PATH_CUR + '/config.ini')

# OPTION
DECOMPOUND_MODE = cfg['OPTION']['DECOMPOUND_MODE']
INFL_DECOMPOUND_MODE = cfg['OPTION']['INFL_DECOMPOUND_MODE']
VERBOSE = cfg.getboolean('OPTION', 'VERBOSE')
OUTPUT_UNKNOWN_UNIGRAMS = cfg.getboolean('OPTION', 'OUTPUT_UNKNOWN_UNIGRAMS')
DISCARD_PUNCTUATION = cfg.getboolean('OPTION', 'DISCARD_PUNCTUATION')
# FILTER
USE_SYNONYM_FILTER = cfg.getboolean('FILTER', 'USE_SYNONYM_FILTER')
USE_POS_FILTER = cfg.getboolean('FILTER', 'USE_POS_FILTER')
MODE_SYNONYM_FILTER = cfg['FILTER']['MODE_SYNONYM_FILTER']
# PATH
PATH_USER_DICT = cfg['PATH']['USER_DICT']
PATH_SYN_DICT = cfg['PATH']['SYN_DICT']


class KoreanAnalyzer(object):
    """Analyzer for Korean text, composed of Pre-/Post-processors, Filters, and Tokenizers.

    KoreanAnalyzer - Users only need to initialize this object.
    Basic only use tokenizer.
    Advanced constructs pipeline that consists of Pre-/Post-processors, Filters, and Tokenizers.
    The order of the pipeline is important.
    """

    def __init__(self,
                 verbose=VERBOSE,
                 path_userdict=None,
                 path_synonyms=None,
                 decompound_mode=DECOMPOUND_MODE,
                 infl_decompound_mode=INFL_DECOMPOUND_MODE,
                 output_unknown_unigrams=OUTPUT_UNKNOWN_UNIGRAMS,
                 discard_punctuation=DISCARD_PUNCTUATION,
                 pos_filter=USE_POS_FILTER,
                 stop_tags=KoreanPOSStopFilter.DEFAULT_STOP_TAGS,
                 synonym_filter=USE_SYNONYM_FILTER,
                 mode_synonym=MODE_SYNONYM_FILTER):
        PATH_CUR = os.path.dirname(__file__)
        print('pynori root:', PATH_CUR)
        self.preprocessor = Preprocessing()
        self.kor_tokenizer = KoreanTokenizer(verbose=verbose,
                                             path_userdict=path_userdict if path_userdict else os.path.join(PATH_CUR, PATH_USER_DICT),
                                             decompound_mode=decompound_mode,
                                             infl_decompound_mode=infl_decompound_mode,
                                             output_unknown_unigrams=output_unknown_unigrams,
                                             discard_punctuation=discard_punctuation)
        self.pos_filter = pos_filter
        self.kor_pos_filter = KoreanPOSStopFilter(stop_tags=stop_tags, verbose=verbose)
        self.synonym_filter = synonym_filter
        self.mode_synonym = mode_synonym
        self.syn_graph_filter = None
        if self.synonym_filter:  # SynonymGraphFilter 초기화 처리 지연 시간으로 True일 때만 활성.
            self.syn_graph_filter = SynonymGraphFilter(preprocessor=self.preprocessor,
                                                       kor_tokenizer=self.kor_tokenizer,
                                                       mode_synonym=self.mode_synonym,
                                                       path_synonyms=path_synonyms if path_synonyms else os.path.join(PATH_CUR, PATH_SYN_DICT))

    def do_analysis(self, in_string):
        """Analyze text input string and return tokens

            Filtering 순서에 유의. (POS -> SYNONYM)
        """

        ##################
        # Pre-processing #
        #################
        in_string = self.preprocessor.pipeline(in_string)

        ##############
        # Tokenizing #
        ##############
        self.kor_tokenizer.set_input(in_string)
        while self.kor_tokenizer.increment_token():
            pass
        tkn_attr_obj = self.kor_tokenizer.tkn_attr_obj

        #################
        # POS Filtering #
        #################
        if self.pos_filter:
            tkn_attr_obj = self.kor_pos_filter.do_filter(tkn_attr_obj)

        #####################
        # Synonym Filtering #
        #####################
        if self.synonym_filter:
            tkn_attr_obj = self.syn_graph_filter.do_filter(tkn_attr_obj)

        # reset token offset
        # tkn_attr_obj = self._reset_token_offset(tkn_attr_obj)

        ###################
        # Post-processing #
        ###################
        # ...

        return tkn_attr_obj.__dict__

    def _reset_token_offset(self, tkn_attrs):
        # TODO: 필터링 후 포지션 재정렬 필요.
        pass

    def set_option_tokenizer(self,
                             decompound_mode=None,
                             infl_decompound_mode=None,
                             output_unknown_unigrams=None,
                             discard_punctuation=None):
        if decompound_mode is not None:
            self.kor_tokenizer.mode = decompound_mode
        if infl_decompound_mode is not None:
            self.kor_tokenizer.infl_mode = infl_decompound_mode
        if output_unknown_unigrams is not None:
            self.kor_tokenizer.output_unknown_unigrams = output_unknown_unigrams
        if discard_punctuation is not None:
            self.kor_tokenizer.discard_punctuation = discard_punctuation
        pass

    def set_option_filter(self,
                          pos_filter=None,
                          stop_tags=None,
                          synonym_filter=None,
                          mode_synonym=None,
                          path_synonyms=None):
        if pos_filter is not None:
            self.pos_filter = pos_filter
        if stop_tags is not None:
            self.kor_pos_filter.stop_tags = stop_tags
        if synonym_filter is not None or mode_synonym is not None:
            if self.synonym_filter or synonym_filter:
                # 주의: 현재 상태 모드의 kor_tokneizer가 입력.
                self.syn_graph_filter = SynonymGraphFilter(preprocessor=self.preprocessor,
                                                           kor_tokenizer=self.kor_tokenizer,
                                                           mode_synonym=mode_synonym,
                                                           path_synonyms=path_synonyms)
        if mode_synonym is not None:
            self.mode_synonym = mode_synonym
        if synonym_filter is not None:
            self.synonym_filter = synonym_filter
        pass


if __name__ == "__main__":
    PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
    nori = KoreanAnalyzer(path_userdict=os.path.join(PROJECT_ROOT_DIR, 'data/userdict_ko.txt'),
                          path_synonyms=os.path.join(PROJECT_ROOT_DIR, 'data/synonyms.txt'),
                          synonym_filter=False,
                          decompound_mode=DcpdMode.DISCARD,
                          infl_decompound_mode=DcpdMode.DISCARD,
                          discard_punctuation=True,
                          output_unknown_unigrams=False,
                          pos_filter=False,
                          stop_tags=[
                              "NNB", "NR", "NP",
                              # "VV", "VA",
                              "VX", "VCP", "VCN", "VSV",
                              "MM",
                              "MAG", "MAJ", "IC", "JKS", "JKC", "JKG", "JKO", "JKB", "JKV", "JKQ",
                              "JX", "JC", "EP", "EF", "EC", "ETN", "ETM", "XPN", "XSN", "XSV",
                              "XSA", "XR", "SF", "SE", "SP", "SSO", "SSC", "SC", "SSC", "SSO",
                              "SY", "E", "J", "UNA", "NA"
                          ])

    # print(nori.do_analysis("아빠가 방에 들어가신다.")['termAtt'])
    print(nori.do_analysis("박혜웅은 베이지라고 불린다.")['termAtt'])
    print(nori.do_analysis("5 G")['termAtt'])
    print(nori.do_analysis("5 GX")['termAtt'])
    print(nori.do_analysis("5G X")['termAtt'])
    print(nori.do_analysis("apple pie")['termAtt'])
    print(nori.do_analysis("a p")['termAtt'])
    print(nori.do_analysis("4 p")['termAtt'])
    print(nori.do_analysis("⓪ 틴")['termAtt'])
    print(nori.do_analysis("T 플랜")['termAtt'])
    print(nori.do_analysis("플랜 T")['termAtt'])
