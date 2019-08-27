from denorm.text2phone import TelephoneParser
from denorm.utils import white_space_tokenizer

from testutils import assert_strings


test_strings = [
    ("6 6 3 3 6 0 6", "6633606"),
    ("0 0 3 5 4 6 6 3 3 6 0 6", "003546633606"),
    ("3 5 4 6 6 3 3 6 0 6", "3546633606"),
    ("5 8 1 2 3 4 5", "5812345"),
    ("4 20 2000", "4202000"),
    (
        "18 18",
        "18 18",
    ),  # This need context, can clash with 18:18 the time, so should be left as is
    ("5 36 36 36", "5363636"),
    ("númerið er 5 80 8000 ekkert annað", "númerið er 5808000 ekkert annað"),
    ("hver er með símanúmerið 5 88 55 22", "hver er með símanúmerið 5885522"),
]


def test_parser():
    parser = TelephoneParser()
    assert_strings(test_strings, parser, white_space_tokenizer)
