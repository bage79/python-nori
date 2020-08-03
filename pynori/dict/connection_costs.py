"""
bi-gram connection cost data from mecab

Reference: matrix.def
"""

import os
import gzip
import pickle
import math


class ConnectionCosts(object):
    """bi-gram connection cost data 를 관리하는 클래스.
    """

    @staticmethod
    def open(COST_PATH):  # 주의: self 는 여기서 필요없음.

        # total_entries = []
        # path_list = []
        # for dirName, subdirList, fileList in os.walk(COST_PATH):
        #    for fname in fileList:
        #        if fname.split('.')[-1] == 'txt':
        #            path_list.append(dirName + '/' + fname)
        # for path in path_list:
        #    entries = open(path, 'r', encoding='UTF8').readlines()
        #    total_entries += entries

        # if not os.path.isfile(COST_PATH):
        #     import pynori.resources.pkl_mecab_matrix.compress

        with gzip.open(COST_PATH, 'rb') as rf:
            total_entries = pickle.load(rf)  # 딕셔너리 타입 반환.

        if len(total_entries) == 0:
            return None
        else:
            return ConnectionCosts(total_entries)

    def __init__(self, total_entries):

        # self.conCosts = dict()
        # for entry in total_entries:
        #    splits = entry.split()
        #    if len(splits) != 3:
        #        continue
        #    rightId = int(splits[0])
        #    leftId = int(splits[1])
        #    cost = int(splits[2])
        #    self.conCosts[(rightId, leftId)] = cost

        self.conCosts = total_entries  # 딕셔너리 타입 저장.

    def get(self, rightId, leftId):
        # return self.conCosts[(int(rightId), int(leftId))]
        return self.conCosts[int(rightId)][int(leftId)]
