from sybil import Sybil
from sybil.parsers.codeblock import CodeBlockParser
from sybil.parsers.doctest import DocTestParser

pytest_collect_file = Sybil(
    parsers=[
        DocTestParser(),
        CodeBlockParser(future_imports=['print_function']),
    ],
    pattern='*.rst',
).pytest()
