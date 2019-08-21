

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
    for w in tokens:
        if w == "og":
            continue
        x = units_dict.get(w, None)
        if x is not None:
            g += x
            length += 1
        elif w in ["hundrað", "hundruð"]:
            g *= 100
            length += 1
        else:
            x = magnitude_dict.get(w, None)
            if x is not None:
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

def parse_numbers(tokens):
    i = 0
    entities = []
    while i < len(tokens):
        try:
            num, length = _text2num(tokens[i:])
            entities.append({
                "entity": "number",
                "text": " ".join(tokens[i:i+length+1]),
                "value": str(num),
                "start": i,
                "end": i + length + 1,
            })
            i += length + 1
        except NumberException:
            i += 1
    return entities


def _tokenize(s):
    return s.split(" ")

if __name__ == "__main__":
    t = _tokenize
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

    s = "hvað eru þrjú hundruð og þrjátíu sænskar krónur í íslenskum"
    for entity in parse_numbers(t(s)):
        s = s.replace(entity["text"], entity["value"])
    sr = "hvað eru 330 sænskar krónur í íslenskum"
    assert sr == s

