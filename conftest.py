from sybil import Sybil
from sybil.parsers.rest import PythonCodeBlockParser, DocTestParser

pytest_collect_file = Sybil(
    parsers=[
        DocTestParser(),
        PythonCodeBlockParser(),
    ],
    pattern='*.rst',
).pytest()
