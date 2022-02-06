# First code to be executed
import itertools
import sys
from collections.abc import Iterable

import koalak

# Create the wordlistools framework with koalak
wordlistools = koalak.mkframework("wordlistools")
tools = wordlistools.mkpluginmanager("tools")


@tools.mkbaseplugin
class BaseTool:
    description = tools.attr(type=str)
    name = tools.attr(type=str)
    group = "basic"
    nb_outputs = 1

    def __init__(self):
        # Toos can have zero or one stdin argument
        # stdin argument are arguments (related to wordlists) that
        # can take their arguments from files or wordlist
        # => That means that, if stdin is not empty (when using pip "|" for example)
        # they will take args from stdin then from regular files
        self._parser = None
        self._usable_with_stdin = False
        self._stdin_arg = {}

    def normalize_wordlist(self, wordlist):
        # print("normalize wordlist", wordlist)
        if isinstance(wordlist, str):
            with open(wordlist, errors="ignore") as f:
                for word in f:
                    # FIXME: What if file don't contain \n at the end?
                    yield word[:-1]  # remove \n
        elif isinstance(wordlist, Iterable):
            yield from wordlist
        elif wordlist is None:
            # 0 is fd for stdin
            # print("Wordlist is None")
            # ignore stdin
            sys.stdin.reconfigure(errors="ignore")
            for word in sys.stdin:
                yield word[:-1]  # remove \n
        else:
            raise TypeError("Type not reconized")

    def normalize_wordlists(self, wordlists):
        return [self.normalize_wordlist(e) for e in wordlists]

    def _normalize_wordlists(self, *wordlists):
        return itertools.chain(*wordlists)

    def wordlists2words(self, *wordlists):
        yield from itertools.chain(
            *(self.normalize_wordlist(wordlist) for wordlist in wordlists)
        )

    def add_argument(self, *args, **kwargs):
        """Add argument to parser and handle the case of stdin
        if stdin=True, that means that the argument can be used
        from stdin"""
        # print("add_argument", self.name, args, kwargs)
        stdin = kwargs.pop("stdin", False)
        # If we don't wait args from stdin
        # or the argument is not meant to be used with stdin
        # we handle the argument normally
        if sys.stdin.isatty() or not stdin:
            self._parser.add_argument(*args, **kwargs)
            return

        # We wait args from stdin AND stdin is True
        # Check if we already have an argument with stdin
        if self._usable_with_stdin:
            raise TypeError("Parser can't have two arguments with stdin")
        self._usable_with_stdin = True
        nargs = kwargs.pop("nargs", None)
        # print("nargs", nargs)
        if nargs == "+":
            kwargs["nargs"] = "*"
            self._parser.add_argument(*args, **kwargs)
            self._stdin_arg = {
                "action": "append",
                "value": None,
                "args": args,
                "kwargs": kwargs,
            }
            # FIXME inject stdin in the list
        elif nargs is None:
            self._stdin_arg = {
                "args": args,
                "kwargs": kwargs,
                "value": None,
                "action": "create",
            }

    def add_argument_color(self):
        self.add_argument(
            "--color",
            help="Color the matched pattern",
            choices=["default", "yes", "no"],
            nargs="?",
            default="default",
            const="yes",
        )

    def add_argument_output(self):
        self.add_argument(
            "-o", "--output", help="Output result in a file", nargs="+", default=[]
        )

    def add_argument_stdout_output(self):
        self.add_argument(
            "--stdout-output",
            dest="stdout_output",
            help="Output in stdout",
            type=int,
            const=0,
            nargs="?",
        )

    def normalize_argument_color(self, args):
        if args.color == "default":
            # Not connected to stdout we color
            if sys.stdout.isatty():
                args.color = True
            # Connected to stdout we don't color
            else:
                args.color = False
        elif args.color == "yes":
            args.color = True
        else:
            args.color = False


"""
List of constraints in subclass
- name
- init_parser
- run
- cmd

- have wordlist or wordlists arguments (not both)
- If he have one of wordlist or wordlists can work with pipe?

"""


parsers = wordlistools.mkpluginmanager("parsers")


@parsers.mkbaseplugin
class BaseParser:
    pass
