import os
import random

from wordlistools.base import BaseTool


class SampleTool(BaseTool):
    name = "sample"
    description = "Output a random number of words from the wordlist"
    group = "statistics"
    # TODO: handle many wordlist (treat as merge)

    def init_parser(self):
        self.add_argument("wordlist", help="Wordlist")

        self.add_argument(
            "-n", "--number", help="Number of words to output", default=10, type=int
        )

    def cmd(self, args):
        return self.run(args.wordlist, number=args.number)

    def run(self, filepath: str, number=10):
        # TODO: what if wordlist come from stdin
        if not isinstance(filepath, str):
            raise TypeError("RandomTool expect only files")

        # Algo
        # Let's say we have a wordlist of 500 words and we want to take randomly
        # 10 words, the idea is we want to chose one word from 0 to 50,
        # an other word from 50 to 100, ..., we take one word from each chunk
        # a chunk is the size of all wordlist / number of word
        #
        # The problem is that we can't split the file depending on the words
        # we don't know where the words starts and stop, we can only seek
        # at an offset, so we will use the size of the file, seek at a random
        # position, and then ignore the current word to take the next one
        # ----

        # size of file in bytes
        size = os.stat(filepath).st_size
        chunk_size = int(size / number)
        f = open(filepath, errors="ignore")
        i_word = 0
        while i_word < number:
            start_chunk = i_word * chunk_size
            end_chunk = (i_word + 1) * chunk_size
            start_word = random.randint(start_chunk, end_chunk)
            # move file pointer
            f.seek(start_word)
            # don't take first line because we are probably in the middle of the word
            _ = f.readline()
            yield f.readline()[:-1]
            i_word += 1


class CountTool(BaseTool):
    name = "count"
    description = "Count the number of words in one or more wordlists"
    group = "statistics"

    def init_parser(self):
        # FIXME: constraint, each argument must have a help!
        self.add_argument("wordlists", help="Wordlists", stdin=True)
        self.add_argument(
            "-p", "--pattern", help="Count only word that match that pattern"
        )

    def cmd(self, args):
        return self.run(args.wordlists, pattern=args.pattern)

    def run(self, wordlist, *wordlists, pattern=None):
        words = self.wordlists2words(wordlist, *wordlists)
        if pattern is None:
            return sum(1 for word in words)
        else:
            return sum(1 for word in words if pattern in word)
