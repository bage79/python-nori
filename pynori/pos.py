class POS(object):
    """
    Part of speech classification for Korean based on Sejong corpus classification.
    The list of tags and their meanings is available here:
    https://docs.google.com/spreadsheets/d/1-9blXKjtjeKZqsf4NzHeYJCrr49-nXeRF6D80udfcwY
    """

    class Type(object):
        MORPHEME = 'MORP'  # A simple morpheme
        COMPOUND = 'COMP'  # Compound noun
        INFLECT = 'INFL'  # Inflected token
        PREANALYSIS = 'PREANY'  # Pre-analysis token


# def describe(self):
#	return self.name, self.value


"""
	class Tag(Enum):
		E = 100 		# Verbal endings
		IC = 110		# Interjection
		J = 120			# Ending Particle
		MAG = 130		# General Adverb
		MAJ = 131		# Conjunctive adverb
		MM = 140		# Modifier
		NNG = 150		# General Noun
		NNP = 151		# Proper Noun
		NNB = 152 		# Dependent noun
		NNBC = 153		# Dependent noun
		NP = 154		# Pronoun
		NR = 155		# Numeral
		SF = 160		# Terminal punctuation
		SH = 161		# Chinese Characeter
		SL = 162		# Foreign language
		SN = 163		# Number
		SP = 164		# Space
		SSC = 165		# Closing brackets
		SSO = 166 		# Opening brackets
		SC = 167		# Separator
		SY = 168		# Other symbol
		SE = 169		# Ellipsis
		VA = 170		# Adjective
		VCN = 171		# Negative designator
		VCP = 172		# Positive designator
		VV = 173		# Verb
		VX = 174		# Auxiliary Verb or Adjective
		XPN = 181		# Prefix
		XR = 182		# Root
		XSA = 183		# Adjective Suffix
		XSN = 184		# Noun Suffix
		XSV = 185		# Verb Suffix
		UNKNOWN = 999 	# Unknown
		UNA = -1		# Unknown
		NA = -1 		# Unknown
		VSV = -1		# Unknown
"""
