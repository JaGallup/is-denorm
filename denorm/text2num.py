from .parser import Parser
from .utils import white_space_tokenizer as t

units = (
    ("núll", 0),
    ("einn|ein|eitt|einn|eina|eitt|einum|einni|einu|eins|einnar|eins|einir|einar|ein|eina|einar|ein|einum|einum|einum|einna|einna|einna", 1),
    ("tveir|tvær|tvö|tvo|tvær|tvö|tveimur|tveim|tveimur|tveim|tveimur|tveim|tveggja|tveggja|tveggja", 2),
    ("þrír|þrjár|þrjú|þrjá|þrjár|þrjú|þremur|þrem|þremur|þrem|þremur|þrem|þriggja|þriggja|þriggja", 3),
    ("fjórir|fjórar|fjögur|fjóra|fjórar|fjögur|fjórum|fjórum|fjórum|fjögurra|fjögra|fjögurra|fjögra|fjögurra|fjögra", 4),
    ("fimm", 5),
    ("sex", 6),
    ("sjö", 7),
    ("átta", 8),
    ("níu", 9),
    ("tíu", 10),
    ("ellefu", 11),
    ("tólf", 12),
    ("þrettán", 13),
    ("fjórtán", 14),
    ("fimmtán", 15),
    ("sextán", 16),
    ("sautján", 17),
    ("átján", 18),
    ("nítján", 19),
    ("tuttugu", 20),
    ("þrjátíu", 30),
    ("fjörutíu|fjörtíu|fjögurtíu", 40),
    ("fimmtíu", 50),
    ("sextíu", 60),
    ("sjötíu", 70),
    ("áttatíu", 80),
    ("níutíu", 90),
)

units_dict = dict()
for words, val in units:
    for word in words.split("|"):
        units_dict[word] = val

magnitude = (
    ("þúsund|þúsundir", 1000),
    ("milljón|milljónir", 1000000),
    ("milljarður|milljarðir", 1000000000),
    ("billjón|billjónir", 1000000000000),
    ("billjarður|billjarðir", 1000000000000000),
    ("trilljón|trilljónir", 1000000000000000000),
)

magnitude_dict = dict()
for words, val in magnitude:
    for word in words.split("|"):
        magnitude_dict[word] = val


class NumberException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


def _text2num(tokens):
    n = 0
    g = 0
    length = 0
    last = None
    for w in tokens:
        if w == "og":
            last = "AND"
            length += 1
            continue
        x = units_dict.get(w, None)
        if x is not None and last != "UNIT":
            last = "UNIT"
            g += x
            length += 1
        elif w in ["hundrað", "hundruð"]:
            last = "MAGN"
            if g == 0:
                g = 1  # One is assumed
            g *= 100
            length += 1
        else:
            x = magnitude_dict.get(w, None)
            if x is not None:
                last = "MAGN"
                if g == 0:
                    g = 1  # One is assumed
                n += g * x
                g = 0
                length += 1
            else:
                if length > 0:
                    return n + g, length
                else:
                    raise NumberException("Unknown number: " + w)
    return n + g, length


def text2num(tokens):
    num, length = _text2num(tokens)
    return num

class NumericalParser(Parser):
    def parse(self, tokens, text):
        if not text:
            text = " ".join(tokens)

        i = 0
        entities = []
        new_string = []
        while i < len(tokens):
            try:
                num, length = _text2num(tokens[i:])
                first, last = tokens[i], tokens[i + length - 1]
                new_string.append(str(num))
                entities.append({
                    "entity": "number",
                    "text": " ".join(tokens[i:i+length]),
                    "value": str(num),
                    "start": text.index(first),
                    "end": text.index(last) + len(last),
                })
                i += length
            except NumberException:
                new_string.append(tokens[i])
                i += 1
        return " ".join(new_string)
#        return {
#            "text": text,
#            "entities": entities,
#            "parsed_text": " ".join(new_string),
#        }
