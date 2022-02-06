import re

import colorama
from wordlistools.base import BaseTool


def red(text):
    return f"{colorama.Fore.RED}{colorama.Style.BRIGHT}{text}{colorama.Style.RESET_ALL}"


class SearchTool(BaseTool):
    name = "search"
    description = "Search words in one or more wordlists with filename like pattern"
    group = "filters"

    def init_parser(self):
        self.add_argument("pattern", help="pattern to search for")
        self.add_argument(
            "wordlists", help="wordlist to product", nargs="+", stdin=True
        )
        self.add_argument_color()

    def cmd(self, args):
        # By default we check if it's connected to stdout
        self.normalize_argument_color(args)
        return self.run(args.pattern, *args.wordlists, color=args.color)

    def run(self, pattern, wordlist, *wordlists, color=False):
        words = self.wordlists2words(wordlist, *wordlists)

        if color:
            for word in words:
                index = word.find(pattern)
                if index != -1:
                    end_index = len(pattern) + index
                    yield f"{word[:index]}{red(word[index:end_index])}{word[end_index:]}"
        else:
            for word in words:
                if pattern in word:
                    yield word


class MatchTool(BaseTool):
    name = "match"
    description = "Search words in one or more wordlists with regular expression"
    group = "filters"

    def init_parser(self):
        self.add_argument("pattern", help="pattern to search for")
        self.add_argument(
            "wordlists", help="wordlist to product", nargs="+", stdin=True
        )
        self.add_argument_color()

    def cmd(self, args):
        self.normalize_argument_color(args)
        return self.run(args.pattern, *args.wordlists, color=args.color)

    def run(self, pattern, wordlist, *wordlists, color=False):
        obj = re.compile(pattern)
        words = self.wordlists2words(wordlist, *wordlists)
        if color:
            for word in words:
                search_obj = obj.search(word)
                if search_obj:
                    index, end_index = search_obj.span()
                    if word[index:end_index]:
                        yield f"{word[:index]}{red(word[index:end_index])}{word[end_index:]}"
                    else:  # If word is empty return word without color
                        # example re.search("a*", "b"), there is a match but the match is empty
                        yield word
        else:
            for word in words:
                if obj.search(word):
                    yield word


def static(g):
    def s_g(self, e):
        return g(e)

    return s_g


class BaseFilterTool(BaseTool):
    group = "filters"
    abstract = True
    func = None  # FIXME in koalak: can add constaints in base clases

    def init_parser(self):
        self.add_argument(
            "wordlists", help="wordlists to modify", nargs="+", stdin=True
        )

    def cmd(self, args):
        return self.run(*args.wordlists)

    def run(self, wordlist, *wordlists):
        words = self.wordlists2words(wordlist, *wordlists)
        for word in words:
            if self.func(word):
                yield word


class IsdigitTool(BaseFilterTool):
    name = "isdigit"
    description = "Keep only digits"

    def func(self, e):
        return str.isdigit(e)


class StartswithTool(BaseTool):
    group = "filters"
    name = "startswith"
    description = "Keep only words that start with a certain string"

    def init_parser(self):
        self.add_argument("string", help="String to check if the word starts with it")
        self.add_argument(
            "wordlists", help="wordlists to modify", nargs="+", stdin=True
        )

    def cmd(self, args):
        return self.run(args.string, *args.wordlists)

    def run(self, string, wordlist, *wordlists):
        words = self.wordlists2words(wordlist, *wordlists)
        for word in words:
            if str.startswith(word, string):
                yield word


class EndswithTool(BaseTool):
    group = "filters"
    name = "endswith"
    description = "Keep only words that end with a certain string"

    def init_parser(self):
        self.add_argument("string", help="String to check if the word ends with it")
        self.add_argument(
            "wordlists", help="wordlists to modify", nargs="+", stdin=True
        )

    def cmd(self, args):
        return self.run(args.string, *args.wordlists)

    def run(self, string, wordlist, *wordlists):
        words = self.wordlists2words(wordlist, *wordlists)
        for word in words:
            if str.startswith(word, string):
                yield word
