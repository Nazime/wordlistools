import inspect

from wordlistools.base import BaseTool


class BaseModifyTool(BaseTool):
    group = "modifiers"
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
        if inspect.ismethoddescriptor(self.__class__.func):
            for word in words:
                yield self.__class__.func(word)
        else:
            for word in words:
                yield self.func(word)


class UpperTool(BaseModifyTool):
    name = "upper"
    description = "Upper case all words in the wordlists"
    func = str.upper


class LowerTool(BaseModifyTool):
    name = "lower"
    description = "Lower case all words in the wordlists"
    func = str.lower


class CapitalizeTool(BaseModifyTool):
    name = "capitalize"
    description = "Capitalize all words in the wordlists"
    func = str.capitalize


class InvertTool(BaseModifyTool):
    name = "invert"
    description = "Invert all words in the wordlists"

    def func(self, e):
        return e[::-1]


class ReplaceTool(BaseTool):
    group = "modifiers"
    name = "replace"
    description = "Replace pattern with string"

    def init_parser(self):
        self.add_argument("pattern", help="pattern to search")
        self.add_argument("replace", help="string to replace with")
        self.add_argument(
            "wordlists", help="wordlists to modify", nargs="+", stdin=True
        )

    def cmd(self, args):
        return self.run(args.pattern, args.replace, *args.wordlists)

    def run(self, pattern, replace, wordlist, *wordlists):
        words = self.wordlists2words(wordlist, *wordlists)
        for word in words:
            yield word.replace(pattern, replace)
