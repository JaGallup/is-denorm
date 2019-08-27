import operator
import re

from .parser import Parser
from .utils import white_space_tokenizer as t

patterns = [
    #  (keywords, symbol, operator, priority)
    ("deilt með", "/", operator.truediv, 2),
    ("sinnum", "*", operator.mul, 2),
    ("plús", "+", operator.add, 1),
    ("mínus", "-", operator.sub, 1),
    ("í veldinu af", "^", operator.pow, 3),
    ("veldi", "^", operator.pow, 3),
    #("minna en|minni en", "<", operator.lt, 0),
    #("stærra en|stærri en", "<", operator.lt, 0),
    #("jafnt og|sama og|sama sem|samasem", "=", operator.eq, 0),
    #("ekki jafnt og|ekki sama og|ekki sama sem|ekki samasem", "=", operator.eq, 0),
]

patterns_dict = dict()
for words, *rest in patterns:
    for word in words.split("|"):
        patterns_dict[word] = rest

number = re.compile(r"^-?[0-9]+$")


class MathParser(Parser):
    def parse(self, tokens, text):
        i = 0
        new_string = []
        after_num = False
        between = []

        while i < len(tokens):
            token = tokens[i]
            is_num = number.match(token)
            if is_num and not after_num:
                after_num = True
                new_string.append(token)
                i += 1
            elif token == "mínus":
                if len(tokens) > i + 1 and number.match(tokens[i+1]):
                    if not after_num:
                        after_num = True
                        new_string.append("-" + tokens[i+1])
                        i += 2
                    elif (after_num and len(between) > 0):
                        tokens[i + 1] = "-" + tokens[i+1]
                        i += 1
                    else:
                        between.append(token)
                        i += 1
                else:
                    new_string.append(token)
                    i += 1
            elif is_num:
                if len(between):
                    b = " ".join(between)
                    s = patterns_dict.get(b, [b])[0]
                    new_string.append(s)
                    new_string.append(token)
                else:
                    new_string.extend(between + [token])
                between = []
                i += 1
            elif after_num:
                between.append(token)
                i += 1
            else:
                new_string.append(token)
                i += 1

        return " ".join(new_string + between)


if __name__ == "__main__":
    test_strings = [
        ("1 plús 2", "1 + 2"),
        ("4 mínus 3", "4 - 3"),
        ("1 deilt með 10", "1 / 10"),
        ("5 sinnum 10 deilt með 4 plús 8", "5 * 10 / 4 + 8"),
        ("mínus 10 sinnum 33", "-10 * 33"),
        ("mínus 55 deilt með mínus 5", "-55 / -5"),
    ]

    parser = MathParser()
    for s, target in test_strings:
        try:
            parsed = parser.parse(t(s), s)
            assert parsed == target
            print("Success: ", parsed, "==", target)
        except AssertionError:
            print("Failed: ", parsed, "!=", target)
