import inspect
import re
import string

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
        if inspect.ismethoddescriptor(self.__class__.func):
            for word in words:
                if self.__class__.func(word):
                    yield word
        else:
            for word in words:
                if self.func(word):
                    yield word


class IsdigitTool(BaseFilterTool):
    name = "isdigit"
    description = "Keep only digits"
    func = str.isdigit


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
            if str.endswith(word, string):
                yield word


class DontStartsWithTool(BaseTool):
    group = "filters"
    name = "dontstartswith"
    description = "Keep only words that doesn't start with a certain string"

    def init_parser(self):
        self.add_argument(
            "string", help="String to check if the word doesn't start with it"
        )
        self.add_argument("wordlists", help="wordlist to return", stdin=True, nargs="+")

    def cmd(self, args):
        return self.run(args.string, *args.wordlists)

    def run(self, string, wordlist, *wordlists):
        words = self.wordlists2words(wordlist, *wordlists)
        for word in words:
            if not word.startswith(string):
                yield word


class DontEndsWithTool(BaseTool):
    group = "filters"
    name = "dontendswith"
    description = "Keep only words that doesn't end with a certain string"

    def init_parser(self):
        self.add_argument(
            "string", help="String to check if the word doesn't end with it"
        )
        self.add_argument("wordlists", help="wordlist to return", stdin=True, nargs="+")

    def cmd(self, args):
        return self.run(args.string, *args.wordlists)

    def run(self, string, wordlist, *wordlists):
        words = self.wordlists2words(wordlist, *wordlists)
        for word in words:
            if not word.endswith(string):
                yield word


class PolicyTool(BaseTool):
    group = "filters"
    name = "policy"
    description = "Keep only words that match the provided policy"

    def init_parser(self):
        self.add_argument(
            "policy",
            help="Policy to check with.\n"
            "'a' => contain at least one lower case letter.\n"
            "'A' contains at least one upper case letter.\n"
            "'1' contains at least one digit.\n"
            "'@' contains at least one special character.\n"
            "You can check the length with == != <= >= < > and the number after.\n"
            "Length must arrive always after the policy\n"
            "Example, check lowercase uppercase and at least 8 chars: policy 'aA>=8' ",
        )
        self.add_argument(
            "-n", help="Number of rules that must be valid to accept the word", type=int
        )
        self.add_argument(
            "wordlists", help="wordlists to modify", nargs="+", stdin=True
        )

    def cmd(self, args):
        return self.run(args.policy, *args.wordlists, n=args.n)

    def run(self, policy, wordlist, *wordlists, n=None):
        rules = self._parse_policy(policy)
        words = self.wordlists2words(wordlist, *wordlists)

        if n is None:
            for word in words:
                if all(rule(word) for rule in rules):
                    yield word
        else:
            if n <= 0 or n >= len(rules):
                raise ValueError(
                    "at_least argument must be greater than 0 and less than the length of rules"
                )

            for word in words:
                satisfied_rules = 0
                for rule in rules:
                    if rule(word):
                        satisfied_rules += 1
                    if satisfied_rules >= n:
                        yield word
                        break

    def _parse_policy(self, policy: str):
        """Policy contain [base_policy][operator][n]
        base_policy: combination of "aA1@" """
        if not policy:
            raise ValueError("Empty policy")

        regex = re.compile(
            r"""^  # match starting
        ([aA1@]*)  # capture base policy
        (?:   # non capturing grp (to have both operator and lenght)
            (==|!=|<=|>=|<|>)(\d+)  # capture operator and digit
        )?
        $  # match ending
        """,
            re.VERBOSE,
        )
        obj = regex.search(policy)
        if obj is None:
            raise ValueError("Wrong policy provided.")

        policy_rules = []
        base_policy, operator, n = obj.groups()

        # Handle base policy: lowercase, uppercase, special char, one digit
        if "a" in base_policy:
            policy_rules.append(lambda s: any(x.islower() for x in s))

        if "A" in base_policy:
            policy_rules.append(lambda s: any(x.isupper() for x in s))

        if "1" in base_policy:
            policy_rules.append(lambda s: any(x.isdigit() for x in s))

        if "@" in base_policy:
            # FIXME: fix special chats
            policy_rules.append(lambda s: any(x in string.punctuation for x in s))

        # Handle the length
        if n is not None:
            n = int(n)
            if operator == "==":
                policy_rules.append(lambda s: len(s) == n)
            elif operator == "!=":
                policy_rules.append(lambda s: len(s) != n)
            elif operator == "<=":
                policy_rules.append(lambda s: len(s) <= n)
            elif operator == ">=":
                policy_rules.append(lambda s: len(s) >= n)
            elif operator == "<":
                policy_rules.append(lambda s: len(s) < n)
            elif operator == ">":
                policy_rules.append(lambda s: len(s) > n)

        return policy_rules
