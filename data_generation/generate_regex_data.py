import sys
import random
from collections import Counter
import subprocess
import re

words = [word.rstrip() for word in open("words.txt", 'r+').readlines()]

class Function():
	def __init__(self, *args):
		self.parent = None
		self.children = []
		self.params = []
		self.lineage = []
		for value in args:
			if issubclass(value.__class__, Function):
				# if(not issubclass(self.__class__, Modifier) ):
				# 	value = SpecialMod(value)
				self.children.append(value)
				value.parent = self
			else:
				self.params.append(value)

	def logical_form(self):
		raise Exception("Not implemented for {}".format(self.__class__.__name__))

	def description(self):
		raise Exception("Not implemented for {}".format(self.__class__.__name__))

	def get_all_functions_flat_list(self):
		cur_list = []
		for child in self.children:
			if child:
				cur_list = cur_list + [child]
				cid = child.get_all_functions_flat_list()
				if cid:
					cur_list = cur_list + cid
		return cur_list


	@classmethod
	def children_type_candidates(self):
		return [ANY]

	@classmethod
	def generate(self, depth, total_nodes, num_comps, MAX_DEPTH, MAX_TOTAL):
		things = []
		i = 0
		for can_gen_candidates in self.children_type_candidates():
			i = i + 1
			can_gen_candidates = flatten(can_gen_candidates)
			can_gen_candidates = filter_gen_candidates(can_gen_candidates, depth, total_nodes, num_comps, MAX_DEPTH, MAX_TOTAL)			
			if not can_gen_candidates:
				return 'None'
			to_gen = random.choice(can_gen_candidates)
			next_thing = to_gen()
			total_nodes += 1 + len(next_thing.children_type_candidates())
			num_comps += 1 if (isinstance(next_thing, AndComp) or isinstance(next_thing, OrComp)) else 0
			things.append(next_thing)

		arguments = []
		for thing in things:
			generated = thing.generate(depth+1, total_nodes, num_comps, MAX_DEPTH, MAX_TOTAL)
			if not generated or generated is 'None':
				return 'None'
			arguments.append(generated)
		arguments = [thing.generate(depth+1, total_nodes, num_comps, MAX_DEPTH, MAX_TOTAL) for thing in things]
		if arguments:
			return self(*arguments)
		return self()

	def raw_logical_form_recurse(self, space_separate_tokens):
		children_strings = [child.raw_logical_form_recurse(space_separate_tokens) for child in self.children]
		space_token = " " if space_separate_tokens else ""
		comma_token = "{}, ".format(space_token)
		open_paren_token = "{0}({0}".format(space_token)
		close_paren_token = "{0}){0}".format(space_token)
		children_string = comma_token.join(children_strings)
		params_str = ""
		for p in self.params:
			params_str += str(p) + ", "
		path_str = self.__class__.__name__ + open_paren_token + params_str + children_string + close_paren_token
		return path_str

	def example_str_positive_candidates(self):
		raise Exception("Not implemented for {}".format(self.__class__.__name__))

	def example_str_negative_candidates(self):
		candidates = self.example_str_positive_candidates()
		can_not_generate = ""
		if type(candidates) is list:
			can_not_generate = [random_string()]
		else:
			can_generate = map(ord, candidates)
			can_generate = set(can_generate)
			can_not_generate = [i for i in range(32, 127) if i not in can_generate]
			can_not_generate = map(chr, can_not_generate)
		return can_not_generate

	def example_str_candidates(self, negative=False):
		negative = len([func for func in self.lineage if isinstance(func, NotComp)]) > 0
		if negative:
			return self.example_str_negative_candidates()
		return self.example_str_positive_candidates()

	def example_str(self):
		if self.children:
			return ' '.join([child.example_str() for child in self.children])
		else:
			s = str(random.choice(self.example_str_candidates()))
			return s

	def set_root(self, root):
		self.root = root

def filter_gen_candidates(candidates, depth, total_nodes, num_comps, MAX_DEPTH=2, MAX_TOTAL=3):
	MAX_COMPS = 2
	if depth < MAX_DEPTH and total_nodes < MAX_TOTAL and num_comps < MAX_COMPS:
		return candidates
	new_candidates = []
	for candidate in candidates:
		if len(candidate.children_type_candidates()) == 0:
			new_candidates.append(candidate)
	return new_candidates

def flatten(l):
	if l and not isinstance(l[0], list):
		return l
	return [item for sublist in l for item in sublist]

def run_regex(regex, sample_string):
	out = subprocess.check_output(['java', '-jar', 'run_one_regex_one_example.jar', regex, sample_string])
	if out == "1":
		return True
	return False

def random_string():
	ran_str = ''
	r = random.random()
	if r < 0.8:
		ran_str = ''.join([rand_valid_char() for i in range(random.randint(1, 6))])
	else:
		ran_str = random.choice(["dog", "truck", "ring", "lake"])
	return ran_str

class BaseFunction(Function):

	def __init__(self, *args):
		Function.__init__(self, *args)
		if self.children:
			build_lineage(self.children[0])

	def logical_form(self):
		form = self.children[0].logical_form()
		filler_words = ["dog", "truck", "ring", "lake"]
		for filler_word in filler_words:
			form = form.replace("WORD", filler_word, 1)
		return form


	def description(self, tryit=False):
		desc = ""
		try:
			desc = "lines {}".format(self.children[0].description())
			a = [("having containing", "containing"), ("having before","before"), ("lines a", "lines with a"), ("lines not the", "lines not having the"), ("lines the", "lines with the"), ("lines not a", "lines not having a"), ("lines words", "lines with words"), ("having containing", "containing"), ("having starting","starting"), ("having ending","ending"), ("having not", "not having"), ("containing not", "not containing"), ("containing having", "containing"), ("having having", "having"), ("with having", "with"), ("lines with words with not a", "lines with words that don't have a"), ("lines with words with not", "lines with words that don't"), ("not not", "not"), ("lines either", "lines having either"), ("lines <and3filler>", "lines having"), ("<and3filler> ", ""), ("words with containing", "words that contain")]
			for e in a:
				desc = desc.replace(e[0], e[1])
			filler_words = ["dog", "truck", "ring", "lake"]

			for filler_word in filler_words:
				desc = desc.replace("WORD", filler_word, 1)
		except Exception as e:
			if tryit:
				return "Fail"
			else:
				raise Exception(e)

		return desc

	@classmethod
	def children_type_candidates(self):
		return [ANY_NOT_LITERAL]

	def raw_logical_form(self, space_separate_tokens=False):
		path_str = self.children[0].raw_logical_form_recurse(space_separate_tokens)
		return path_str

	def get_positive_example(self):
		done = False
		example = ""
		regex = self.logical_form()
		desc = self.description()
		while not done:
			# print(regex)
			r = random.random()
			if r > 0.2:
				example = self.get_base_positive_example()
			elif r > 0.4:
				example = " ".join([self.get_base_positive_example() for i in range(random.randint(10))])
			else:
				example = self.get_base_positive_example()
			r2 = random.random()
			if r2 > 0.2:
				example = surround() + " " + example + " " + surround()
			elif r2 > 0.4:
				example = example + " " + surround()
			elif r2 > 0.6:
				example = surround() + " " + example
			else:
				example = example
			# print(example)
			if run_regex(regex, example):
				done = True
			# print(regex, desc, example, run_regex(regex, example))
		return example

	def try_get_positive_example(self, N=1):
		done = False
		example = ""
		regex = self.logical_form()
		desc = self.description()
		i = 0
		while not done:
			# print(regex)
			r = random.random()
			if r > 0.2:
				example = self.get_base_positive_example()
			elif r > 0.4:
				example = " ".join([self.get_base_positive_example() for i in range(random.randint(10))])
			else:
				example = self.get_base_positive_example()
			r2 = random.random()
			if r2 > 0.2:
				example = surround() + " " + example + " " + surround()
			elif r2 > 0.4:
				example = example + " " + surround()
			elif r2 > 0.6:
				example = surround() + " " + example
			else:
				example = example
			# print(example)
			while len(example) > 15:
				example = example[int(len(example)*0.25):int(len(example)*0.75)]
			if run_regex(regex, example):
				done = True
			i += 1
			if not done and i > N:
				return None
			# print(regex, desc, example, run_regex(regex, example))
		return example

	def try_get_negative_example(self, N=1):
		ex = BaseFunction(NotComp(self.children[0])).try_get_positive_example(N)
		return ex


	def try_get_negative_example_from_positive(self, positive, N=1):
		done = False
		example = positive
		regex = self.logical_form()
		i = 0
		while not done:
			r2 = random.random()
			example = modify(example)
			while len(example) > 15:
				example = example[int(len(example)*0.25):int(len(example)*0.75)]
			if run_regex(regex, example) == False:
				done = True
			i += 1
			if not done and i > N:
				return None
			# print(regex, desc, example, run_regex(regex, example))
		return example

	def get_base_positive_example(self):
		example = self.children[0].example_str()
		filler_words = ["dog", "truck", "ring", "lake"]
		for filler_word in filler_words:
			example = example.replace("WORD", filler_word, 1)
		return example

def modify(inp):
	r0 = random.random()
	r = random.randint(0, len(inp))
	r2 = None
	try:
		r2 = random.randint(1, len(inp))
	except:
		pass

	out = inp
	if r0 < 0.2:
		out = inp[:r] + rand_valid_char() + inp[r+1:] # add 1 char
	if r0 < 0.4 and r2:
		out = inp[:r2-1] + inp[r2:] # delete 1 char
	elif r0 < 0.5:
		out = inp.lower()
	elif r0 < 0.6:
		out = inp.upper()
	elif r0 < 0.7:
		out = inp[:r]
	elif r0 < 0.8:
		out = inp[r:]
	elif r0 < 0.90:
		out = re.sub(r"[0-9]", "", inp)
	elif r0 < 0.95:
		out = "".join([rand_valid_char() for i in range(random.randint(1,5))])
	return out

def valid_chars():
	return map(chr, range(33, 127))

def rand_valid_char():
	return str(random.choice(valid_chars()))


def load_books():
	book_lines = []
	book_file_name = "twocities.txt"
	with open(book_file_name) as f:
	    book_lines = f.read().splitlines() 
	    book_lines = [line.rstrip() for line in book_lines]
	    book_lines = [line for line in book_lines if line]
	return book_lines

book_lines = load_books()

def surround():
	r = random.randint(1, len(book_lines))
	line = book_lines[r-1]
	r2 = random.randint(0, min(len(line), 2))
	line = line[:r2-1]
	return line


def build_lineage(node, parent=None):
	if parent:
		node.lineage = node.lineage + parent.lineage + [parent]
	for child in node.children:
		build_lineage(child, node)
	

class Literal(Function):
	pass
	# def description(self):
	# 	desc = self._description()
	# 	print(self.parent)
	# 	print("grand", self.parent.parent)
	# 	if isinstance(self.parent, Composition):
	# 		grandparent = self.parent.parent
	# 		if "action_word" in dir(grandparent):
	# 			act_word = grandparent.action_word()
	# 			desc = " " + desc 
	# 			desc = desc.replace(" a ", " " + act_word + " a ")
	# 			desc = desc.strip()
	# 			print(desc)
	# 			exit()
	# 	return desc

	# def _description(self):
	# 	raise Exception("Not implemented for {}".format(self.__class__.__name__))

class NumberFunc(Literal):
	def logical_form(self):
		return "[0-9]"

	def description(self):
		return "a number"

	@classmethod
	def children_type_candidates(self):
		return []

	def example_str_positive_candidates(self):
		return map(str, (range(10)))

#Tokens
class CapitalLetterFunc(Literal):
	def logical_form(self):
		return "[A-Z]"

	def description(self):
		return "a capital letter"

	@classmethod
	def children_type_candidates(self):
		return []

	def example_str_positive_candidates(self):
		upper_case_letters =  map(chr, range(65, 91))
		# print("upper letter")
		# print(upper_case_letters)
		return upper_case_letters


class LowerCaseLetterFunc(Literal):
	def logical_form(self):
		return "[a-z]"

	def description(self):
		return "a lower-case letter"

	@classmethod
	def children_type_candidates(self):
		return []

	def example_str_positive_candidates(self):
		lower_case_letters = map(chr, range(97, 123))
		return lower_case_letters

class LetterFunc(Literal):
	def logical_form(self):
		return "[A-Za-z]"
	def description(self):
		return "a letter"
	@classmethod
	def children_type_candidates(self):
		return []

	def example_str_positive_candidates(self):
		upper_case_letters = map(chr, range(97, 123))
		lower_case_letters = map(chr, range(65, 91))
		return lower_case_letters + upper_case_letters

class VowelsFunc(Literal):
	def logical_form(self):
		return "[AEIOUaeiou]"
	def description(self):
		return "a vowel"
	@classmethod
	def children_type_candidates(self):
		return []

	def example_str_positive_candidates(self):
		vowels = "AEIOUaeiou"	
		return vowels

class CharacterFunc(Literal):
	def logical_form(self):
		return "."
	def description(self):
		return "a character"

	@classmethod
	def children_type_candidates(self):
		return []

	def example_str_positive_candidates(self):
		characters = map(chr, range(65, 123))
		return characters

#Functions
class ContainsFunc(Function):
	def logical_form(self):
		return ".*{}.*".format(self.children[0].logical_form())

	def description(self):
		return "containing {}".format(self.children[0].description())

	def action_word(self):
		return "containing"

	@classmethod
	def children_type_candidates(self):
		return [ANY]


class ContainsOnlyFunc(Function):
	def logical_form(self):
		return "{}".format(self.children[0].logical_form())

	def description(self):
		return "containing only {}".format(self.children[0].description())

	@classmethod
	def children_type_candidates(self):
		return [LITERALS]

	def example_str(self):
		return "{}".format(self.children[0].example_str())

	def action_word(self):
		return "containing only"


#Functions
class StartsWithFunc(Function):
	def logical_form(self):
		return "({})(.*)".format(self.children[0].logical_form())

	def description(self):
		return "starting with {}".format(self.children[0].description())
	@classmethod
	def children_type_candidates(self):
		return [ANY_NOT_MOD]

	def action_word(self):
		return "starting with"

class EndsWithFunc(Function):
	def logical_form(self):
		return "(.*)({})".format(self.children[0].logical_form())

	def description(self):
		return "ending with {}".format(self.children[0].description())

	@classmethod
	def children_type_candidates(self):
		return [ANY_NOT_MOD]

	def action_word(self):
		return "ending with"


class F8(Function):
	def logical_form(self):
		return "\\b{}\\b".format(self.children[0].logical_form())

	def description(self):
		return "words with {}".format(self.children[0].description())

	def action_word(self):
		return "words with"

	@classmethod
	def children_type_candidates(self):
		return [ANY_NOT_LITERAL]

	def example_str(self):
		return " {} ".format(self.children[0].example_str())



class RandWordFunc(Literal):
	def __init__(self, *args):
		Function.__init__(self, *args)
		self.real_word = random.choice(words)
		self.word = "WORD"

	def logical_form(self):
		return "{}".format(self.word)

	def description(self):
		return "the string '{}'".format(self.word)

	@classmethod
	def children_type_candidates(self):
		return []

	def example_str_positive_candidates(self):
		return [self.word]

class FollowedByFunc(Function):
	def logical_form(self):
		return "{}.*{}.*".format(self.children[0].logical_form(), self.children[1].logical_form())

	def description(self):
		return "{} followed by {}".format(self.children[0].description(), self.children[1].description())

	@classmethod
	def children_type_candidates(self):
		return [LITERALS, LITERALS]

class Modifier(Function):
	pass

class SpecialMod(Modifier):
	def logical_form(self):
		return self.children[0].logical_form()

	def description(self):
		return "one {}".format(self.children[0].description())

	@classmethod
	def children_type_candidates(self):
		return [ANY]

class AtMostMod(Modifier):
	def __init__(self, *args):
		Modifier.__init__(self, *args)
		if self.params != None and len(self.params) < 1:
			self.params.append(random.randint(2, 5))

	def logical_form(self):
		return "({}){}1,{}{}".format(self.children[0].logical_form(),  "{", self.params[0], "}")

	def description(self):
		return "{}, at most {} times".format(self.children[0].description(),self.params[0])

	@classmethod
	def children_type_candidates(self):
		return [ANY_NOT_MOD]

class OneOrMoreMod(Modifier):
	def logical_form(self):
		return "({})+".format(self.children[0].logical_form())

	def description(self):
		return "{} at least once".format(self.children[0].description())

	@classmethod
	def children_type_candidates(self):
		return [ANY_NOT_MOD]

class NOrMoreMod(Modifier):
	def __init__(self, *args):
		Modifier.__init__(self, *args)
		if self.params != None and len(self.params) < 1:
			self.params.append(random.randint(2, 7))

	def logical_form(self):
		return "({}){}{},{}".format(self.children[0].logical_form(),  "{", self.params[0], "}")
	def description(self):
		return "{}, {} or more times".format(self.children[0].description(),self.params[0])

	@classmethod
	def children_type_candidates(self):
		return [ANY_NOT_MOD]

class ZeroOrMoreMod(Modifier):
	def logical_form(self):
		return "({})*".format(self.children[0].logical_form())

	def description(self):
		return "{}, zero or more times".format(self.children[0].description())

	@classmethod
	def children_type_candidates(self):
		return [ANY_NOT_MOD]


class Composition(Function):
	pass

class BeforeComp(Composition):
	def to_generate(self):
		self.to_generate = [["Function","Compostion"],"Param"]
	def logical_form(self):
		return "({}).*({}).*".format(self.children[0].logical_form(),self.children[1].logical_form())
	def description(self):
		return "{} before {}".format(self.children[0].description(),self.children[1    ].description())
	
	@classmethod
	def children_type_candidates(self):
		return [ANY, ANY]

	def example_str(self):
		return "{}{}".format(self.children[0].example_str(),self.children[1].example_str())

class BetweenComp(Composition):
	def to_generate(self):
		self.to_generate = [["Function","Compostion"],"Param"]
	def logical_form(self):
		return "({}).*({}).*".format(self.children[0].logical_form(),self.children[1].logical_form())
	def description(self):
		return "{} before {}".format(self.children[0].description(),self.children[1    ].description())
	
	@classmethod
	def children_type_candidates(self):
		return [ANY, ANY]

	def example_str(self):
		return "{}{}".format(self.children[0].example_str(),self.children[1].example_str())



class OrComp(Composition):
	def to_generate(self):
		self.to_generate = [["Function", "Composition"], "Param"]
	def logical_form(self):
		return "({})|({})".format(self.children[0].logical_form(),self.children[1].logical_form())

	def description(self):
		return "{} or {}".format(self.children[0].description(),self.children[1].description())

	@classmethod
	def children_type_candidates(self):
		return [ANY, ANY]

	def example_str(self):
		r = random.random() 
		if r > 0.4:
			return self.children[0].example_str()
		elif r > 0.8 :
			return self.children[0].example_str()
		elif r > 0.9:
			return "{} {}".format(self.children[0].example_str(),self.children[1].example_str())
		else:
			return "{}{}".format(self.children[0].example_str(),self.children[1].example_str())

class AndComp(Composition):
	def to_generate(self):
		self.to_generate = [["Function", "Composition"], "Param"]

	def logical_form(self):
		return "({})&({})".format(self.children[0].logical_form(),self.children[1].logical_form())

	def description(self):
		negative = len([func for func in self.lineage if isinstance(func, NotComp)]) > 0
		if negative:
			return "{} and not {}".format(self.children[0].description(),self.children[1].description())	
		else:
			return "{} and {}".format(self.children[0].description(),self.children[1].description())

	@classmethod
	def children_type_candidates(self):
		return [ANY, ANY]

	def example_str(self):
		r = random.random()
		if r > 0.5:
			return "{} {}".format(self.children[0].example_str(),self.children[1].example_str())
		else:
			return "{}{}".format(self.children[0].example_str(),self.children[1].example_str())



class NotComp(Composition):
	def logical_form(self):
		return "~({})".format(self.children[0].logical_form())

	def description(self):
		return "not {}".format(self.children[0].description())

	@classmethod
	def children_type_candidates(self):
		return [ANY]

class And3Comp(Composition):
	def logical_form(self):
		return "({})&({})&({})".format(self.children[0].logical_form(), self.children[1].logical_form(), self.children[2].logical_form())

	def to_generate(self):
		self.to_generate = [["Function", "Composition"], "Param"]

	def description(self):
		negative = len([func for func in self.lineage if isinstance(func, NotComp)]) > 0
		if negative:
			return "{}, not {}, and not {}".format(self.children[0].description(),self.children[1].description(), self.children[2].description())	
		else:
			return "<and3filler> {}, {}, and {}".format(self.children[0].description(),self.children[1].description(), self.children[2].description())

	@classmethod
	def children_type_candidates(self):
		return [LITERALS, LITERALS, LITERALS]

	def example_str(self):
		return "{} {} {}".format(self.children[0].example_str(),self.children[1].example_str(), self.children[2].example_str())

class Or3Comp(Composition):
	def logical_form(self):
		return "({})|({})|({})".format(self.children[0].logical_form(), self.children[1].logical_form(), self.children[2].logical_form())

	def to_generate(self):
		self.to_generate = [["Function", "Composition"], "Param"]

	def description(self):
		negative = len([func for func in self.lineage if isinstance(func, NotComp)]) > 0
		if negative:
			return "{}, {}, or {}".format(self.children[0].description(),self.children[1].description(), self.children[2].description())	
		else:
			return "either {}, {}, or {}".format(self.children[0].description(),self.children[1].description(), self.children[2].description())

	@classmethod
	def children_type_candidates(self):
		return [LITERALS, LITERALS, LITERALS]

	def example_str(self):
		r = random.random() 
		if r > 0.3:
			return self.children[0].example_str()
		elif r > 0.6:
			return self.children[1].example_str()
		elif r > 0.9:
			return self.children[2].example_str()
		else:
			return "{} {} {}".format(self.children[0].example_str(),self.children[1].example_str(), self.children[2].example_str())


type_dict = {}
type_dict["Function"] = [ContainsFunc, F8, StartsWithFunc, EndsWithFunc, FollowedByFunc]
type_dict["Literal"] = [NumberFunc, CapitalLetterFunc, LowerCaseLetterFunc, LetterFunc, RandWordFunc, RandWordFunc, RandWordFunc, RandWordFunc, CharacterFunc, VowelsFunc]
type_dict["Modifier"] = [OneOrMoreMod, NOrMoreMod, ZeroOrMoreMod, ContainsOnlyFunc]
type_dict["Composition"] = [OrComp, NotComp, AndComp, BeforeComp, And3Comp, Or3Comp]

ANY = type_dict["Function"] + type_dict["Composition"], type_dict["Modifier"] + type_dict["Literal"]
ANY_NOT_LITERAL = type_dict["Function"] + type_dict["Modifier"] + type_dict["Composition"]
ANY_NOT_MOD = type_dict["Function"] + type_dict["Modifier"] + type_dict["Literal"] + [OrComp]
LITERALS = type_dict["Literal"]

def is_a_good_func(func):
	if not func or isinstance(func, basestring):
		return False
	all_sub_funcs = func.get_all_functions_flat_list()
	if not all_sub_funcs or 'None' in all_sub_funcs or None in all_sub_funcs:
		return False
	sub_func_names = [sub.__class__.__name__ for sub in all_sub_funcs]
	num_unique_funcs = len(set(sub_func_names))
	if len(all_sub_funcs) - num_unique_funcs  > 5:
		return False
	sub_func_names_2 = [n for n in sub_func_names if n != "RandWordFunc"]
	func_counts = Counter(sub_func_names_2)
	max_func_count = max(func_counts.values())
	if max_func_count > 1:
		return False

	sub_func_names_2_all = [n for n in sub_func_names]
	func_counts_all = Counter(sub_func_names_2_all)
	max_func_count_all = max(func_counts_all.values())
	if max_func_count_all > 4:
		return False

	side_by_side_exact = False
	for i in range(len(sub_func_names)-1):
		if sub_func_names[i] == sub_func_names[i+1] and sub_func_names[i] != "RandWordFunc":
			return False
		if issubclass(all_sub_funcs[i].__class__, Modifier) and issubclass(all_sub_funcs[i+1].__class__, Modifier):
			return False
		if issubclass(all_sub_funcs[i].__class__, F8) and issubclass(all_sub_funcs[i+1].__class__, F8):
			return False
	mod_func_counts = len([sub for sub in all_sub_funcs if issubclass(sub.__class__, Modifier)])
	if mod_func_counts > 1:
		return False
	if has_any_at_depth(func, [OrComp, AndComp, Or3Comp, And3Comp], 1) and has_any_at_depth(func, LITERALS, 2):
		return False
	if has_any_at_depth(func, [ContainsOnlyFunc], 2) and not has_any_at_depth(func, [NotComp], 1):
		return False
	func_desc = func.description(True)
	if func_desc == "Fail":
		return False
	if 'letter before a letter' in func_desc:
		return False
	if 'starting with ending' in func_desc or 'ending with starting' in func_desc:
		return False
	if 'starting with contains' in func_desc:
		return False
	if 'containing contains' in func_desc:
		return False
	if 'containing starting' in func_desc:
		return False
	if 'before starting' in func_desc:
		return False
	if 'starting with containing' in func_desc:
		return False

	if 'And3Comp' in sub_func_names or 'Or3Comp' in sub_func_names:
		if random.random() > 0.5:
			return False
	return True

def has_any_at_depth(func, types_to_check, target_depth):
	agenda = [(func, 0)]
	while agenda:
		node, cur_depth = agenda.pop()
		agenda = agenda + [(c, cur_depth + 1) for c in node.children]
		if cur_depth == target_depth and sum([int(isinstance(node, type_to_check)) for type_to_check in types_to_check]) > 0:
			return True
	return False

# def has_any_sames(func):
# 	d_dict = {}
# 	agenda = [func]
# 	cur_depth = 0
# 	while agenda:
# 		node = agenda.pop()
# 		agenda = agenda + node.children
# 		if cur_depth == target_depth and sum([int(isinstance(node, type_to_check)) for type_to_check in types_to_check]) > 0:
# 			return True
# 		depth_list = d_dict.get(depth, [])
# 		if str(node._class__) in depth_list:
# 			return True
# 		d_dict.append(str(node._class__))
# 		d_dict[depth] = depth_list
# 		cur_depth += 1
# 	return False


def test_basic_construction():
	example0 = BaseFunction(StartsWithFunc(
		OneOrMoreMod(
			F8(
				OrComp(
					AtMostMod(CapitalLetterFunc()),
					NumberFunc()
				)
			)
		)
	))

	example1 = BaseFunction(NotComp(ContainsFunc(NumberFunc())))

	print example0.description()
	print example0.logical_form()
	print example0.raw_logical_form()

	print example1.description()
	print example1.logical_form()
	print example1.raw_logical_form()

def test_generation(print_format='pretty'):
	all_generated = []
	all_generated_raw_logicals = set()
	# params_list = [(1, 3, 5000), (2, 5, 300000), (3, 6, 50000)]
	params_list = [(1, 4, 10000), (2, 5, 600000), (3, 7, 70000)]
	# params_list = [(1, 4, 10000)]

	# params_list = [(1, 3, 5000), (2, 4, 5000), (3, 5, 5000)]

	for k in range(len(params_list)):
		params = params_list[k]
		iterations = params[2]
		for i in range(iterations):
			generated = BaseFunction.generate(0, 0, 0, params[0], params[1])
			if not is_a_good_func(generated):
				continue
			raw_logical = generated.description()
			if raw_logical not in all_generated_raw_logicals:
				all_generated_raw_logicals.add(raw_logical)
				all_generated.append(generated)
		print(len(all_generated))

	if print_format == 'pretty':
		for form in all_generated:
			print("Desc:", form.description())
			print("Regex Form", form.logical_form())
			print("Raw Logic Form", form.raw_logical_form())
			print("\n")
		print("# Generated: ", len(all_generated))

	elif print_format == "raw":
		print("Descriptions\n")
		# for form in all_generated:
			# print(form.description())
		with open('{}{}'.format("data_descriptions_3", '.txt'), "w") as out_file:
			out_file.write("\n".join([gen.description() for gen in all_generated]))

		print("Raw Logical Forms:\n")
		# for form in all_generated:
			# print(form.raw_logical_form(True))
		with open('{}{}'.format("data_funcs_3", '.txt'), "w") as out_file:
			out_file.write("\n".join([gen.raw_logical_form(True) for gen in all_generated]))
		
		print("Logical Forms:\n")
		# for form in all_generated:
		# 	logical = form.logical_form()
			# print(logical)
		with open('{}{}'.format("data_regexes_3", '.txt'), "w") as out_file:
			out_file.write("\n".join([gen.logical_form() for gen in all_generated]))

	elif print_format == "csv":
		for form in all_generated:
			print('"{}","{}","{}","{}","{}","{}","{}","{}"'.format(*[form.description(), form.raw_logical_form(), form.logical_form()] + [k for k in range(5)]))
			# print('"{}","{}","{}","{}","{}","{}","{}","{}"'.format([form.description(), form.raw_logical_form(), form.logical_form()] + [form.get_positive_example() for i in range(10)]))
		print("# Generated: ", len(all_generated))

def test_example_generation():
	example0 = BaseFunction(NotComp(ContainsFunc(LetterFunc())))
	example1 = BaseFunction(OrComp(ContainsFunc(CapitalLetterFunc()), ContainsFunc(NumberFunc())))
	example2 = BaseFunction(AndComp(ContainsFunc(NotComp(CapitalLetterFunc())), ContainsFunc(NumberFunc())))
	example3 = BaseFunction(BeforeComp(CapitalLetterFunc(), RandWordFunc()))


	print(example0.get_positive_example())
	print(example1.get_negative_example())
	# print(example2.get_positive_example())
	# print(example3.get_positive_example())

	# example_string = example1.get_positive_example()
	# print(example_string)

def main(argv):
	# print(run_regex("[0-9]","5"))
	# test_example_generation()
	# exit()
	# test_basic_construction()
	# test_generation('raw')
	test_generation()

if __name__ == "__main__":
    main(sys.argv)
