import operator
import re

from .utils import white_space_tokenizer as t
from .parser import Parser


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


if __name__ == "__main__":
    test_strings = [
        ("6 6 3 3 6 0 6", "6633606"),
        ("0 0 3 5 4 6 6 3 3 6 0 6", "003546633606"),
        ("3 5 4 6 6 3 3 6 0 6", "3546633606"),
        ("5 8 1 2 3 4 5", "5812345"),
        ("4 20 2000", "4202000"),
        ("18 18", "18 18"),  # This need context, can clash with 18:18 the time, so should be left as is
        ("5 36 36 36", "5363636"),
        ("númerið er 5 80 8000 ekkert annað", "númerið er 5808000 ekkert annað"),
        ("hver er með símanúmerið 5 88 55 22", "hver er með símanúmerið 5885522"),
    ]   
    
    parser = TelephoneParser()
    for s, target in test_strings:
        try:
            parsed = parser.parse(t(s), s)
            assert parsed == target
            print("Success: ", parsed, "==", target)
        except AssertionError:
            print("Failed: ", parsed, "!=", target)
