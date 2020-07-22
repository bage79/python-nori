import inspect
import json


def to_dict(obj, max_values=100, exclude_private_members=True):
    _di = {}
    attributes = inspect.getmembers(obj, lambda a: not (inspect.isroutine(a)))
    for k, v in attributes:
        if exclude_private_members and k.startswith('_'):
            continue
        v_type = type(v)
        if (v_type is list or v_type is set) and len(v) > max_values:
            v = v[:max_values]
        if (v_type is dict) and len(v) > max_values:
            v = list(v.items())[:max_values]
        _di[k] = v
    return _di


class TokenAttribute(object):
    """Token Attribute Info."""

    def __init__(self):
        self.termAtt = []  # CharTermAttribute
        self.offsetAtt = []  # OffsetAttribute
        # self.posIncAtt = [] # PositionIncrementAttribute
        self.posLengthAtt = []  # PositionLengthAttribute
        # self.posAtt = [] # PartOfSpeechAttribute
        # self.readingAtt = [] # ReadingAttribute
        self.posTypeAtt = []
        self.posTagAtt = []
        self.dictTypeAtt = []

    def __repr__(self):
        return json.dumps(to_dict(self), ensure_ascii=False, indent=2, sort_keys=False)
