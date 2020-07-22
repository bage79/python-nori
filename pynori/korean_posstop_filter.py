from pynori.token_attribute import TokenAttribute


class KoreanPOSStopFilter(object):
    """
    Removes tokens that match a set of part-of-speech tags
    """

    DEFAULT_STOP_TAGS = [
        'EP', 'EF', 'EC', 'ETN', 'ETM',
        'IC',
        'JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ', 'JX', 'JC',
        'MAG',
        'MAJ',
        'MM',
        'SP',
        'SSC',
        'SSO',
        'SC',
        'SE',
        'XPN',
        'XSA',
        'XSN',
        'XSV',
        'UNA',
        'NA',
        'VSV'
    ]

    # noinspection PyDefaultArgument
    def __init__(self, stop_tags=DEFAULT_STOP_TAGS, verbose: bool = False):
        self.stop_tags = stop_tags
        self.verbose = verbose

    def do_filter(self, tkn_attrs: TokenAttribute):
        if self.verbose:
            print(tkn_attrs)
        cur_pos_list = tkn_attrs.posTagAtt
        # bool_applied_stoptag_list = [False if x in self.stop_tags else True for x in cur_pos_list]
        bool_applied_stoptag_list = [True] * len(cur_pos_list)
        for i, x in enumerate(cur_pos_list):
            if '+' in x:  # INFLECT 원형 때문에 추가. (VC+EMF) 에서 둘 중 하나라도 걸리면 삭제.
                splited_x = x.split('+')
                if splited_x[0] in self.stop_tags or splited_x[1] in self.stop_tags:
                    bool_applied_stoptag_list[i] = False
            else:
                if x in self.stop_tags:
                    bool_applied_stoptag_list[i] = False

        for name, value in tkn_attrs.__dict__.items():
            new_value_list = []
            cur_value_list = getattr(tkn_attrs, name)
            for i, _ in enumerate(cur_value_list):
                if bool_applied_stoptag_list[i]:
                    new_value_list.append(cur_value_list[i])
            setattr(tkn_attrs, name, new_value_list)

        return tkn_attrs
