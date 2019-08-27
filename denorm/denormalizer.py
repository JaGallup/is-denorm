from .text2num import NumericalParser
from .text2math import MathParser
from .text2phone import TelephoneParser

from .utils import white_space_tokenizer as t


pipeline = [
	NumericalParser(),
	MathParser(),
	TelephoneParser(),
]

def denormalize(text, tokenizer=t):
	message = {
		"text": text,
		"tokenizer": t,
	}
	for parser in pipeline:
		parser.process(message)

	return message["text"]
