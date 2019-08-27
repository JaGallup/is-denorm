"""
Icelandic de-normalizer Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

is-denorm is a denormalizer for Icelandic.
Basic usage:
	
	>>> from denorm import denormalize
	>>> denormalize("hvað er sjö hundruð og tuttugu deilt með fjórum")
	"hvað er 720 / 4"

"""

from .denormalizer import denormalize
