# wordlistools
Wordlistools is a collection of tools to play with wordlists. This tool was built with offensive security in mind,
to help bruteforcing, filtering wordlists to crack passwords, building
wordlists for fuzzing, etc.
This project is still under development.

**Features**

- Can be used as command lines or as a python library
- Can be used with stdin redirection ``|``
- Easily extensible, you can add your own plugins on your home directory ```~/.koalak/wordlistools/plugins```


![wordlistools demo](https://raw.githubusercontent.com/nazime/wordlistools/master/images/help_v0.1.3.png)


## Install

```bash
pip3 install wordlistools
```

## Demonstration
Note: This demonstration is an old version of wordlistools,
but the principe remains the same.
[![wordlistools demo](https://raw.githubusercontent.com/nazime/wordlistools/master/images/wordlistools.gif)](https://asciinema.org/a/430731)


## Using policy subcommand
You can filter your wordlist based on a policy, the policy follow the following format ``[base_policy][lenght_policy]``.
The base policy can have the following rules:
- a: word must contain at least one lower case letter
- A: word must contain at least one upper case letter
- 1: word must contain at least one digit
- @: word must contain at least one special character

length rule have an operator (==, !=, <=, >=, <, >) followed by its length. Example if we want
to have passwords that have at least one lowercase, at least one upper case, at least one special
character and its length is at least 10 characters long ``policy 'aA@>=10'``. Do not forget
to quote your arguments.

![policy_cmd](https://raw.githubusercontent.com/nazime/wordlistools/master/images/policy_cmd.png)

## Add a tool

You can easily add your own tools in wordlistools. Create a python file in ``~/koalak/wordlistools/plugins/`` and subclass ``BasePlugin``, wordlistools will automatically execute your script and register your plugin.

You have to define the following attributes

- name(str): the name of your plugin (must be unique)
- description(str): description of what your will plugin do, it will be displayed in the help CLI

Implement the following abstract methods:

- ``init_parser()``: to configure the CLI arguments by using the standard library argparse, use ``self.add_argument`` which is a wrapper for the original argparse method.
- run: implement here the logic of your plugin, take any things as parameters and must return an iterator of strings
- cmd(args): must call the ``self.run`` method based on the ``args`` arguments of argparse

Plugin Template

```python
# path of this file: ~/koalak/wordlistools/plugins/myplugins.py
import itertools
from wordlistools import BaseTool


class MyTool(BaseTool):
    name = "myplugin"
    description = "Do nothing, return the same list"

    def init_parser(self):
        self.add_argument("wordlists", help="wordlist to return", nargs="+", stdin=True)

    def cmd(cls, args):
        return cls.run(*args.wordlists)

    def run(cls, *wordlists):
        wordlists = cls.normalize_wordlists(wordlists)
        for e in itertools.chain(*wordlists):
            yield e
```

If you want your plugins to handle stdin wordlists you have to add ``stdin=True`` in ``add_argument``.
