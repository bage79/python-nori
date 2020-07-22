import csv


def smart_split(in_str):
    # input:   '"aaaa",32,"bbbb","ccc,ddd"'
    # output:  ['aaaa', '32', 'bbbb', 'ccc,ddd']
    splited_arr = ['{}'.format(x) for x in list(csv.reader([in_str], delimiter=',', quotechar='"'))[0]]
    return splited_arr


import pickle


def save_pkl(data, name):  # name: ‘..._pkl'
    fp = open(name, 'wb')
    pickle.dump(data, fp)
    fp.close()


def load_pkl(name):  # name: ‘..._pkl'
    fp = open(name, 'rb')
    return pickle.load(fp)


data = load_pkl('data.pkl')

# -------------------------------------------------------------------

from konlpy.tag import Hannanum
from konlpy.tag import Kkma
from konlpy.tag import Komoran
from konlpy.tag import Okt
from pynori.korean_analyzer import KoreanAnalyzer

hannanum = Hannanum()
kkma = Kkma()
komoran = Komoran()
okt = Okt()
nori = KoreanAnalyzer(decompound_mode='MIXED',
                      discard_punctuation=True,
                      output_unknown_unigrams=True,
                      pos_filter=False,
                      stop_tags=['JKS', 'JKB', 'VV', 'EF'])

import time


def analyzer_exe_time(sample_data, analyzer_obj, use_nori):
    start_time = time.time()
    for text in sample_data:
        if use_nori:
            analyzer_obj.do_analysis(text)
        else:
            analyzer_obj.pos(text)
    return time.time() - start_time


# -------------------------------------------------------------------

for idx in [1, 10, 100, 1000, 10000, 100000]:

    # for analyzer in [hannanum, kkma, komoran, okt, nori]

    sample_data = data[:idx]
    print('# number of sample data: ', len(sample_data))

    print('\n')

    # Hannanum
    start_time = time.time()
    for x in sample_data:
        hannanum.pos(x)
    print('Hanna:\t{}'.format(time.time() - start_time))

    # Kkma
    start_time = time.time()
    for x in sample_data:
        kkma.pos(x)
    print('Kkma:\t{}'.format(time.time() - start_time))

    # Okt
    start_time = time.time()
    for x in sample_data:
        okt.pos(x)
    print('Okt:\t{}'.format(time.time() - start_time))

    # Nori
    start_time = time.time()
    for x in sample_data:
        nori.do_analysis(x)
    print('Nori:\t{}'.format(time.time() - start_time))

    print('\n')

    # break

"""
pynori 0.1.0.

# number of sample data:  1


Hanna:	0.0013859272003173828
Kkma:	0.0024421215057373047
Okt:	0.0005130767822265625
Nori:	0.002794981002807617


# number of sample data:  10


Hanna:	0.034677982330322266
Kkma:	0.07546067237854004
Okt:	0.011886119842529297
Nori:	0.0965571403503418


# number of sample data:  100


Hanna:	0.28960275650024414
Kkma:	0.7048020362854004
Okt:	0.09319186210632324
Nori:	0.7220721244812012


# number of sample data:  1000


Hanna:	2.5906150341033936
Kkma:	6.380319356918335
Okt:	0.9402952194213867
Nori:	6.466601133346558


# number of sample data:  10000


Hanna:	27.611809730529785
Kkma:	77.73616790771484
Okt:	11.43677806854248
Nori:	68.20249319076538


# number of sample data:  100000


Hanna:	262.72305488586426
Kkma:	699.7041671276093
Okt:	95.79926490783691
Nori:	672.8327238559723
"""
