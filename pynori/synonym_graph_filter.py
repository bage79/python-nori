import os
from copy import deepcopy

from configparser import ConfigParser
from pynori.dict.trie import Trie
from pynori.token_attribute import TokenAttribute

cfg = ConfigParser()
#PATH_CUR = os.getcwd() + '/pynori'
PATH_CUR = os.path.dirname(__file__)
cfg.read(PATH_CUR+'/config.ini')

# PATH
PATH_SYN_DICT = cfg['PATH']['SYN_DICT']



class SynMode(object):
	""" Synonym mode to select synonyms """
	NORM = 'NORM' # select representative synonym token
	EXT = 'EXTENSION' # select all synonym tokens


class SynonymGraphFilter(object):
	"""Synonym Text Processing

	Add synonym words to token stream / or Norm synonmy words
	keeping token offsets.

	Parameters
	----------
	kor_tokenizer

	mode_synonym : {'EXTENSION', 'NORM'}

	동의어 필터링 특징
	 - Decompound 모드(MIXED, DISCARD, NONE)에 상관없이 동작

	"""

	def __init__(self, preprocessor, kor_tokenizer, mode_synonym, path_synonyms=None):
		self.SEP_CHAR = '_' # separate charcter in token
		self.preprocessor = preprocessor
		self.kor_tokenizer = kor_tokenizer # korean_analyzer.py 에서 decompound mode가 이미 결정
		self.mode_synonym = mode_synonym
		self.syn_trie = None
		self.synonym_build(path_synonyms)
		pass

	def _simple_tokenizer(self, in_string):
		# Pre-processing
		in_string = self.preprocessor.pipeline(in_string)
		# Tokenizing
		self.kor_tokenizer.set_input(in_string)
		while self.kor_tokenizer.increment_token():
			pass
		return self.kor_tokenizer.tkn_attr_obj

	def synonym_build(self, path_syn_file):
		# File Read
		entries = []
		with open(path_syn_file, 'r', encoding='utf-8') as rf:
			for line in rf:
				line = line.strip()
				if len(line) == 0:
					continue
				if line[:2] == '# ': # 주석 line
					continue
				entries.append(line)
		
		# Save entries to data structure.
		self.syn_trie = Trie()
		for line in entries:
			tkn_attr_obj_list = []
			for i, token in enumerate(line.split(',')): # list
				tkn_attr_obj_list.append(self._simple_tokenizer(token)) # tkn_attr_obj

			if self.mode_synonym == SynMode.EXT:
				trie_result = tkn_attr_obj_list
			elif self.mode_synonym == SynMode.NORM:
				trie_result = [tkn_attr_obj_list[0]] # 첫 번째 토큰을 동의어 대표어

			for tkn_attr_obj in tkn_attr_obj_list: # result
				self.syn_trie.insert(self.SEP_CHAR.join(tkn_attr_obj.termAtt), trie_result)

	def _set_token_attribute(self, source, target, idx):
		for name, _ in target.__dict__.items():
			target.__dict__[name].append(source.__dict__[name][idx])
		return target

	def do_filter(self, tkn_attrs):
		new_tkn_attrs = TokenAttribute()
		token_list = tkn_attrs.termAtt
		step = -1

		for m, _ in enumerate(token_list):
			if m <= step:
				# m 이 아닌 n+1 이상에서 [C]가 실행된 경우 step을 맞춰줌
				continue

			step = m
			token = token_list[step] # 현재 step의 token
			for n in range(m, len(token_list)):
				tkn, node = self.syn_trie.search(token)
				if tkn == False and node is None: # [A]
					# 해당 token 중 어떤 음절이라도 node 생성이 되지 않은 경우
					new_tkn_attrs = self._set_token_attribute(tkn_attrs, new_tkn_attrs, n)
					break

				if tkn == True and node is None: # [B]
					# 해당 token이 노드가 생성된 token의 부분집합이고 그의 동의어가 없는 경우 (ex. '노리_분석기' 에서 현재 token이 '노리')
					if n != len(token_list)-1:
						token += self.SEP_CHAR
						token += token_list[n+1]
					# no break.
				if tkn == True and node is not None: # [C]
					# 동의어 사전 룩업 성공
					for trie_tkn_attrs in node.result[0]:
						for k, _ in enumerate(trie_tkn_attrs.termAtt):
							new_tkn_attrs = self._set_token_attribute(trie_tkn_attrs, new_tkn_attrs, k)
					step = n
					break

		return new_tkn_attrs

