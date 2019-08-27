from denorm.text2num import text2num, NumericalParser
from denorm.utils import white_space_tokenizer as t

from testutils import assert_strings


def test_text2num():
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


test_strings = [
    (
        "hvað eru þrjú hundruð og þrjátíu sænskar krónur í íslenskum",
        "hvað eru 330 sænskar krónur í íslenskum",
    ),
    ("framnesvegi tuttugu og átta", "framnesvegi 28"),
    ("álfheimum sjötíu og fjögur", "álfheimum 74"),
    (
        "hvað eru hundrað dollarar í íslenskum krónum",
        "hvað eru 100 dollarar í íslenskum krónum",
    ),
    ("hvað eru eitt þúsund krónur í evrum", "hvað eru 1000 krónur í evrum"),
    ("hvað eru þúsund krónur í evrum", "hvað eru 1000 krónur í evrum"),
    (
        "breyttu tvö þúsund og þrjú hundruð krónum í dollara",
        "breyttu 2300 krónum í dollara",
    ),
    ("hvað kosta áttatíu evrur", "hvað kosta 80 evrur"),
    ("vektu mig eftir átta klukkutíma", "vektu mig eftir 8 klukkutíma"),
    ("vektu mig eftir átta tíma", "vektu mig eftir 8 tíma"),
    ("stilltu vekjaraklukku á níu", "stilltu vekjaraklukku á 9"),
    ("settu vekjaraklukkuna á tíu þrjátíu", "settu vekjaraklukkuna á 10 30"),
    ("settu vekjaraklukkuna á níu þrjátíu", "settu vekjaraklukkuna á 9 30"),
    ("settu vekjaraklukkuna á hálf tólf", "settu vekjaraklukkuna á hálf 12"),
    (
        "getur þú vakið mig klukkan sjö á morgun",
        "getur þú vakið mig klukkan 7 á morgun",
    ),
    (
        "nennir þú að vekja mig eftir tuttugu mínútur",
        "nennir þú að vekja mig eftir 20 mínútur",
    ),
    (
        "nennir þú að vekja mig tuttugu og tvö fjörtíu og fimm",
        "nennir þú að vekja mig 22 45",
    ),
    ("hvað er sjö hundruð og tuttugu deilt með fjórum", "hvað er 720 deilt með 4"),
    ("sex sex þrír þrír sex núll sex", "6 6 3 3 6 0 6"),
    (
        "núll núll þrír fimm fjórir sex sex þrír þrír sex núll sex",
        "0 0 3 5 4 6 6 3 3 6 0 6",
    ),
    ("fimm átta einn tveir þrír fjórir fimm", "5 8 1 2 3 4 5"),
    ("fjórir tuttugu tvö þúsund", "4 20 2000"),
    ("átján átján", "18 18"),
    ("fimm þrjátíu og sex þrjátíu og sex þrjátíu og sex", "5 36 36 36"),
    ("árið var nítján hundruð og níutíu", "árið var 1990"),
    (
        "Genfarsamningurinn var áritaður fyrir sjötíu árum síðan eða árið nítján hundruð fjörtíu og níu",
        "Genfarsamningurinn var áritaður fyrir 70 árum síðan eða árið 1949",
    ),
    (
        "sjöundi áratugur sautjándu aldar var frá sautján hundruð og sjötíu til sautján hundruð og áttatíu",
        "sjöundi áratugur sautjándu aldar var frá 1770 til 1780",
    ),
]


def test_parser():
    parser = NumericalParser()
    assert_strings(test_strings, parser, t)
