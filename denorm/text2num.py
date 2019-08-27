from parser import Parser
from utils import white_space_tokenizer as t

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


if __name__ == "__main__":
    assert 1 == text2num(t("einn"))
    assert 12 == text2num(t("tólf"))
    assert 72 == text2num(t("sjötíu og tveir"))
    assert 72 == text2num(t("sjötíu og tvær"))
    assert 72 == text2num(t("sjötíu og tvö"))
    assert 300 == text2num(t("þrjú hundruð"))
    assert 1230 == text2num(t("tólf hundruð og þrjátíu"))
    assert 13404 == text2num(t("þrettán þúsund fjögur hundruð og fjórir"))
    assert 6000000 == text2num(t("sex milljón"))
    assert 18700059 == text2num(t("átján milljónir sjö hundruð þúsund fimmtíu og níu"))

    test_sentences = [
        ("hvað eru þrjú hundruð og þrjátíu sænskar krónur í íslenskum", "hvað eru 330 sænskar krónur í íslenskum"),
        ("framnesvegi tuttugu og átta", "framnesvegi 28"),
        ("álfheimum sjötíu og fjögur", "álfheimum 74"),
        ("hvað eru hundrað dollarar í íslenskum krónum", "hvað eru 100 dollarar í íslenskum krónum"),
        ("hvað eru eitt þúsund krónur í evrum", "hvað eru 1000 krónur í evrum"),
        ("hvað eru þúsund krónur í evrum", "hvað eru 1000 krónur í evrum"),
        ("breyttu tvö þúsund og þrjú hundruð krónum í dollara", "breyttu 2300 krónum í dollara"),
        ("hvað kosta áttatíu evrur", "hvað kosta 80 evrur"),
        ("vektu mig eftir átta klukkutíma", "vektu mig eftir 8 klukkutíma"),
        ("vektu mig eftir átta tíma", "vektu mig eftir 8 tíma"),
        ("stilltu vekjaraklukku á níu", "stilltu vekjaraklukku á 9"),
        ("settu vekjaraklukkuna á tíu þrjátíu", "settu vekjaraklukkuna á 10 30"),
        ("settu vekjaraklukkuna á níu þrjátíu", "settu vekjaraklukkuna á 9 30"),
        ("settu vekjaraklukkuna á hálf tólf", "settu vekjaraklukkuna á hálf 12"),
        ("getur þú vakið mig klukkan sjö á morgun", "getur þú vakið mig klukkan 7 á morgun"),
        ("nennir þú að vekja mig eftir tuttugu mínútur", "nennir þú að vekja mig eftir 20 mínútur"),
        ("nennir þú að vekja mig tuttugu og tvö fjörtíu og fimm", "nennir þú að vekja mig 22 45"),
        ("hvað er sjö hundruð og tuttugu deilt með fjórum", "hvað er 720 deilt með 4"),
        ("sex sex þrír þrír sex núll sex", "6 6 3 3 6 0 6"),
        ("núll núll þrír fimm fjórir sex sex þrír þrír sex núll sex", "0 0 3 5 4 6 6 3 3 6 0 6"),
        ("fimm átta einn tveir þrír fjórir fimm", "5 8 1 2 3 4 5"),
        ("fjórir tuttugu tvö þúsund", "4 20 2000"),
        ("átján átján", "18 18"),
        ("fimm þrjátíu og sex þrjátíu og sex þrjátíu og sex", "5 36 36 36"),
        ("árið var nítján hundruð og níutíu", "árið var 1990"),
        ("Genfarsamningurinn var áritaður fyrir sjötíu árum síðan eða árið nítján hundruð fjörtíu og níu",
            "Genfarsamningurinn var áritaður fyrir 70 árum síðan eða árið 1949"),
        ("sjöundi áratugur sautjándu aldar var frá sautján hundruð og sjötíu til sautján hundruð og áttatíu", 
            "sjöundi áratugur sautjándu aldar var frá 1770 til 1780"),
    ]

    import pprint
    parser = NumericalParser()
    for s, target in test_sentences:
        try:
            parsed = parser.parse(t(s), s)
            assert parsed == target
            print("Success: ", parsed, "==", target)
        except AssertionError:
            pprint.pprint(resp)
            print("Failed: ", parsed, "!=", target)
