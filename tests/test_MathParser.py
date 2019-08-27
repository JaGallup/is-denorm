from denorm.text2math import MathParser
from denorm.utils import white_space_tokenizer

from testutils import assert_strings


test_strings = [
    ("1 plús 2", "1 + 2"),
    ("4 mínus 3", "4 - 3"),
    ("1 deilt með 10", "1 / 10"),
    ("5 sinnum 10 deilt með 4 plús 8", "5 * 10 / 4 + 8"),
    ("mínus 10 sinnum 33", "-10 * 33"),
    ("mínus 55 deilt með mínus 5", "-55 / -5"),
]


def test_parser():
    parser = MathParser()
    assert_strings(test_strings, parser, white_space_tokenizer)
