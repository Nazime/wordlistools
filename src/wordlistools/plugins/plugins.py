import itertools
import sys
from collections import Counter

from wordlistools.base import BaseTool, parsers


class ProductTool(BaseTool):
    name = "product"
    description = "Product two or more wordlists"

    def init_parser(self):
        self.add_argument("wordlist", help="Wordlist")
        self.add_argument(
            "wordlists", help="wordlist to product", nargs="+", stdin=True
        )
        self.add_argument(
            "-s", "--sep", help="separator to add between words", default=""
        )

    def cmd(self, args):
        return self.run(args.wordlist, *args.wordlists, sep=args.sep)

    def run(self, wordlist1, wordlist2, *wordlists, sep=""):
        wordlists = [wordlist1, wordlist2] + list(wordlists)
        wordlists = self.normalize_wordlists(wordlists)
        for e in itertools.product(*wordlists):
            yield sep.join(e)


class MinusTool(BaseTool):
    name = "minus"
    description = "Words that are in the first wordlist but not in the others"

    def init_parser(self):
        self.add_argument("wordlist", help="First wordlist")
        self.add_argument("wordlists", help="Other wordlists", nargs="+", stdin=True)

    def cmd(self, args):
        return self.run(args.wordlist, *args.wordlists)

    def run(self, first_wordlist, other_wordlist, *other_wordlists):

        first_words = self.wordlists2words(first_wordlist)
        other_words = self.wordlists2words(other_wordlist, *other_wordlists)

        other_words = set(other_words)

        for word in first_words:
            if word not in other_words:
                yield word


class MergeTool(BaseTool):
    name = "merge"
    description = "Merge two or more wordlists"

    def init_parser(self):
        self.add_argument("wordlist", help="First wordlist")
        self.add_argument(
            "wordlists", help="wordlist to product", nargs="+", stdin=True
        )

    def cmd(self, args):
        return self.run(args.wordlist, *args.wordlists)

    def run(self, wordlist1, wordlist2, *wordlists):
        yield from self.wordlists2words(wordlist1, wordlist2, *wordlists)


class BackupTool(BaseTool):
    name = "backup"
    description = "Extends backup extensions to one or more wordlists"
    extensions = ["~", ".bak", ".old"]

    def init_parser(self):
        self.add_argument(
            "wordlists",
            help="Wordlist to extend with back extensions",
            stdin=True,
            nargs="+",
        )
        self.add_argument(
            "-a", "--add", help="Extensions to append", default=[], nargs="+"
        )
        self.add_argument(
            "-r", "--remove", help="Extensions to remove", default=[], nargs="+"
        )
        self.add_argument(
            "-e", "--extensions", help="Extensions", default=[], nargs="+"
        )

    def cmd(self, args):
        return self.run(
            *args.wordlists,
            add=args.add,
            remove=args.remove,
            extensions=args.extensions,
        )

    def run(self, wordlist, *wordlists, remove=None, add=None, extensions=None):
        # wordlists = self.normalize_wordlists(wordlists)
        wordlists = [wordlist] + list(wordlists)
        remove = remove or []
        add = add or []
        extensions = extensions or self.extensions
        extensions = list(extensions)  # To no modify the parameter list

        extensions += add
        extensions = [e for e in extensions if e not in remove]
        # FIXME: Faux! tu merge et product avec extensions
        # FIXME: find a way to pass a tool to an other
        return ProductTool().run(*wordlists, extensions)


class ParseTool(BaseTool):
    name = "parse"
    description = "Convert tool output to a wordlist (Example gobuster output)"
    # TODO: each type tool will have it's own subparser

    def init_parser(self):
        # FIXME: in koalak   add function to get names of plugins!
        self.add_argument(
            "type",
            help="Type of output to parse",
            choices=list(parsers._plugins.keys()),
        )
        #
        self.add_argument("input", help="input to parse", stdin=True)

    def cmd(self, args):
        return self.run(args.type, args.input)

    def run(self, type, input):

        parser = parsers[type]
        if input is None:
            input = sys.stdin
        else:
            input = open(input)
        yield from parser.parse(input)


class SplitTool(BaseTool):
    name = "split"
    description = "Split wordlist into many wordlists with a specific separator"

    def init_parser(self):
        self.add_argument("separator", help="Separator to split words", type=str)
        self.add_argument("wordlist", help="wordlist to product", stdin=True)
        self.add_argument("-c", "--col", help="Column to extract", type=int, default=0)
        self.add_argument(
            "-r",
            "--repeat",
            help="Repeat words (disable unique), faster since it will not check if the word was already printed",
            action="store_true",
        )

    def cmd(self, args):
        return self.run(
            args.separator, args.wordlist, col=args.col, unique=not args.repeat
        )

    def run(self, separator: str, wordlist, *, col=0, unique=True):
        wordlists = self.normalize_wordlist(wordlist)
        if not unique:
            for word in wordlists:
                yield word.split(separator)[col]
        else:
            unique_words = set()
            for word in wordlists:
                splitted_word = word.split(separator)[col]
                if splitted_word not in unique_words:
                    yield splitted_word
                    unique_words.add(splitted_word)


class SortTool(BaseTool):
    name = "sort"
    description = "Sort wordlist"

    def init_parser(self):
        self.add_argument(
            "wordlists", help="wordlist to product", nargs="+", stdin=True
        )

    def cmd(self, args):
        return self.run(*args.wordlists)

    def run(self, wordlist, *wordlists):
        words = self.wordlists2words(wordlist, *wordlists)
        yield from sorted(words)


class UniqueTool(BaseTool):
    name = "unique"
    description = "Remove duplicate from a wordlist"

    def init_parser(self):
        self.add_argument(
            "wordlists", help="wordlist to product", nargs="+", stdin=True
        )

    def cmd(self, args):
        return self.run(*args.wordlists)

    def run(self, *wordlists):
        words = self.wordlists2words(*wordlists)
        seen_words = set()
        for word in words:
            if word not in seen_words:
                yield word
                seen_words.add(word)


class DuplicateTool(BaseTool):
    name = "duplicate"
    description = "Show all duplicated words"

    def init_parser(self):
        self.add_argument(
            "wordlists", help="wordlist to product", nargs="+", stdin=True
        )
        self.add_argument(
            "-m", "--min", help="Minimum number of duplicate", default=2, type=int
        )

    def cmd(self, args):
        return self.run(*args.wordlists, min=args.min)

    def run(self, *wordlists, min: int = 2):
        words = self.wordlists2words(*wordlists)
        seen = {}
        returned_words = set()
        for word in words:
            if word not in seen:
                seen[word] = 1
            else:
                seen[word] += 1

            if seen[word] >= min and word not in returned_words:
                yield word
                returned_words.add(word)


class OccurrenceTool(BaseTool):
    name = "occurrence"
    description = "Show all duplicated words with their occurrences"

    def init_parser(self):
        self.add_argument(
            "wordlists", help="wordlist to product", nargs="+", stdin=True
        )
        self.add_argument(
            "-m", "--min", help="Minimum number of duplicate", default=1, type=int
        )

        # TODO: add possibility to not sort

    def cmd(self, args):
        return self.run(*args.wordlists, min=args.min)

    def run(self, *wordlists, min: int = 1, sort=True):
        # FIXME: should return tuples? find solution between API usage and cmd
        words = self.wordlists2words(*wordlists)
        words = Counter(words)
        if sort:
            words = words.most_common()
        else:
            words = words.items()
        for word, occurrence in words:
            if occurrence >= min:
                yield f"{occurrence} {word}"
