

class Parser(object):
    def process(self, message):
        text = message["text"]
        tokens = message["tokenizer"](text)
        message["text"] = self.parse(tokens, text)

    def parse(self, tokens, text):
    	"""
    	Overwrite this function to do the parsing
    	"""
    	raise NotImplemented("This function needs to be overwritten")