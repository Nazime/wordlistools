from .base import BaseParser


class GobusterParser(BaseParser):
    name = "gobuster"

    @classmethod
    def parse(cls, input_file):
        for word in input_file:
            word = word.split(" ", 1)[0][1:]
            yield word
