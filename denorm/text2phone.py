import operator
import re

from .parser import Parser
from .utils import white_space_tokenizer as t


number = re.compile(r"^[0-9]+$")


class TelephoneParser(Parser):
    def parse(self, tokens, text):
        i = 0
        new_string = []
        n_string = []

        while i < len(tokens):
            token = tokens[i]
            is_num = number.match(token)
            if is_num:
                n_string.append(token)
            else:
                n = "".join(n_string)
                if len(n) in [7, 10, 12]:
                    new_string.append(n)
                else:
                    new_string.extend(n_string)
                new_string.append(token)
                n_string = []
            i += 1

        n = "".join(n_string)
        if len(n) in [7, 10, 12]:
            new_string.append(n)
        else:
            new_string.extend(n_string)


        return " ".join(new_string)
