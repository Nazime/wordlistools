# wordlistools
Wordlistools is a collection of tools to play with wordlists. This tool is meant to help bruteforcing in penetration testing. The project is still under development.

**Features**

- Can be used as command lines or as a python library
- Can be used with stdin redirection ``|``
- Easily extensible, you can add your own plugins on your home directory ```~/.koala/wordlistools/plugins```

```bash
usage: wordlistool [-h] {product,minus,count,merge,search,match,backup,parse,split,sort,unique,duplicate,occurrence,sample} ...

You can add your own plugin tools by adding a python script to /home/nazime/.koala/wordlistools/plugins

positional arguments:
  {product,minus,count,merge,search,match,backup,parse,split,sort,unique,duplicate,occurrence,sample}
                        Tool to run
    product             Product two or more wordlists
    minus               Words that are in the first wordlist but not in the others
    count               Count the number of words in one or more wordlists
    merge               Merge two or more wordlists
    search              Search words in one or more wordlists with filename like pattern
    match               Search words in one or more wordlists with regular expression
    backup              Extends backup extensions to one or more wordlists
    parse               Convert tool output to a wordlist (Example gobuster output)
    split               Split wordlist into many wordlists with a specific separator
    sort                Sort wordlist
    unique              Remove duplicate from a wordlist
    duplicate           Show all duplicated words
    occurrence          Show all duplicated words with their occurrences
    sample              Output a random number of words from the wordlist

optional arguments:
  -h, --help            show this help message and exit
```





## Install

```bash
pip3 install wordlistools
```

## Demonstration

[![wordlistools demo](https://raw.githubusercontent.com/nazime/wordlistools/master/images/wordlistools.gif)](https://asciinema.org/a/430731)



## Add a tool

You can easily add a plugin in wordlistools. Create a python file in ``~/fwm/wordlistools/plugins/`` and subclass ``BasePlugin``, wordlistools will automatically execute your script and register your plugin.



You have to define the following attribute

- name(str): the name of your plugin (must be unique)
- description(str): description of what your plugin do, it will be displayed in arguments help

Implement the following abstract method and add the decorator ``classmethod``

- run: implement here the logic of your plugin, take any thing as parameters and must return
- help
- init_parser

Plugin Template

```python
import argparse
from wordlistools import BaseTool


class MyTool(BaseTool):
    name = "my"
    description = "Do nothing"

    @classmethod
    def init_parser(cls, parser: argparse.ArgumentParser):
        parser.add_argument("wordlists", help="wordlist to product", nargs="+")

    @classmethod
    def cmd(cls, args):
        return cls.run(*args.wordlists)

    @classmethod
    def run(cls, *wordlists):
        wordlists = cls.normalize_wordlists(wordlists)
        yield from itertools.chain(*wordlists)
```
