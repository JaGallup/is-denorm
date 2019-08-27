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


if __name__ == "__main__":
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
        ("hvað er sjö hundruð og tuttugu deilt með fjórum", "hvað er 720 / 4"),
        ("sex sex þrír þrír sex núll sex", "6633606"),
        ("núll núll þrír fimm fjórir sex sex þrír þrír sex núll sex", "003546633606"),
        ("fimm átta einn tveir þrír fjórir fimm", "5812345"),
        ("fjórir tuttugu tvö þúsund", "4202000"),
        ("átján átján", "18 18"),
        ("fimm þrjátíu og sex þrjátíu og sex þrjátíu og sex", "5363636"),
        ("árið var nítján hundruð og níutíu", "árið var 1990"),
        ("Genfarsamningurinn var áritaður fyrir sjötíu árum síðan eða árið nítján hundruð fjörtíu og níu",
            "Genfarsamningurinn var áritaður fyrir 70 árum síðan eða árið 1949"),
        ("sjöundi áratugur sautjándu aldar var frá sautján hundruð og sjötíu til sautján hundruð og áttatíu", 
            "sjöundi áratugur sautjándu aldar var frá 1770 til 1780"),
    ]

    import pprint
    for s, target in test_sentences:
        try:
            parsed = denormalize(s)
            assert parsed == target
            print("Success: ", parsed, "==", target)
        except AssertionError:
            print("Failed: ", parsed, "!=", target)

