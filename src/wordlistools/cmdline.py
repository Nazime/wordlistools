import argparse
import sys
import types

import argcomplete
import coloring
from koalak import ArgparseSubcmdHelper
from wordlistools import consts, tools


def _normalize_result(value):
    if isinstance(value, str):
        return value
    elif isinstance(value, int):
        return str(value)
    else:
        raise TypeError(f"Can't handle type {type(value)}")


def normalize_result(value):
    if isinstance(value, tuple):
        return [_normalize_result(e) for e in value]
    else:
        return [_normalize_result(value)]


def old_main(args=None):
    # FIXME: remove me
    if args is None:
        args = sys.argv[1:]

    # create main parser "wordlistools"
    main_parser = argparse.ArgumentParser(
        "wordlistools",
        description=f"You can add your own plugin tools by adding a python script to {tools.homepath}",
    )
    subparsers = main_parser.add_subparsers(dest="subcommand", help="Tool to run")
    instance_tools = {}
    for Tool in tools:
        subparser = subparsers.add_parser(Tool.name, help=Tool.description)
        tool = Tool()
        instance_tools[tool.name] = tool
        # print("INITED PARSER FOR", tool.name)
        tool._parser = subparser
        tool.init_parser()
        tool.add_argument_output()
        tool.add_argument_stdout_output()
        # run subcommand
    argcomplete.autocomplete(main_parser)
    args = main_parser.parse_args(args)
    if args.subcommand is None:
        main_parser.print_help()
        sys.exit(1)

    tool = instance_tools[args.subcommand]
    # print("args befor _stdin_arg treatement", args)
    # print()
    # print("_stdin_arg", tool.name, tool._stdin_arg)
    if tool._stdin_arg:
        # Create dummy argparser juste to know the dest name
        # print("entering stdin_arg")
        dummy_parser = argparse.ArgumentParser()
        _stdin_arg = tool._stdin_arg
        arg = dummy_parser.add_argument(*_stdin_arg["args"], **_stdin_arg["kwargs"])
        argname = arg.dest
        #       print("args in stdin_arg", args)
        if _stdin_arg["action"] == "append":
            attr = getattr(args, argname)
            attr.append(_stdin_arg["value"])
        elif _stdin_arg["action"] == "create":
            setattr(args, argname, _stdin_arg["value"])

    # -------------------------
    # Handle outputs and stdout
    # -------------------------
    # get nb_tool_outputs
    if isinstance(tool.nb_outputs, int):
        nb_tool_outputs = tool.nb_outputs
    else:
        nb_tool_outputs = tool.nb_outputs(args)

    # number of output that the user is waiting
    if args.output:

        nb_user_output = len(args.output)
        # By default if outputs are present and stdin_output is not
        # Default stdin_output to None
        stdout_output = args.stdout_output
        if args.stdout_output is not None:
            nb_user_output += 1

    else:
        stdout_output = 0
        nb_user_output = 1

    # print(f"Number of user output {nb_user_output}")
    # print(f"Waiting for {nb_tool_outputs} outputs")
    if nb_user_output != nb_tool_outputs:
        msg = f"The number of the tool {tool.name} outputs ({nb_tool_outputs})"
        msg += f" is different than the number of expected output ({nb_user_output})"
        print(msg)
        sys.exit(1)

    # Init writers (files/stdout)
    writers = list(args.output)
    writers.insert(stdout_output, sys.stdout)

    # -------------------------
    # Run tool and print output
    # -------------------------
    results = tool.cmd(args)
    if isinstance(results, types.GeneratorType):
        for result in results:
            result = normalize_result(result)
            for i, e in enumerate(result):
                writers[i].write(e + "\n")
    else:
        result = normalize_result(results)
        for i, e in enumerate(result):
            writers[i].write(e + "\n")


def main(args=None):
    """Tentative desepéré de le faire avec koalak"""
    if args is None:
        args = sys.argv[1:]

    class WordlistoolsCommand(ArgparseSubcmdHelper):
        prog = "wordlistools"
        description = f"You can add your own plugin tools by adding a python script to {tools.homepath}"
        prolog = coloring.bdodger_blue(consts.ASCII_ART)
        color_help = True

        groups = {
            "basic": {
                "title": "Basic commands",
                "description": "Commands to interact with many wordlist at the same time",
                "commands": [],
            },
            "filters": {
                "title": "Filters commands",
                "description": "Keep only words that match the filter",
                "commands": [],
            },
            "modifiers": {
                "title": "Modifiers commands",
                "description": "Apply a modification to each word in the wordlist",
                "commands": [],
            },
            "statistics": {
                "title": "Statistics commands",
                "description": "Tools to better understand the wordlist",
                "commands": [],
            },
        }
        for Tool in tools:

            groups[Tool.group]["commands"].append(Tool.name)

    instance_tools = {}

    def generate_parser_and_run_functions(Tool):
        tool = Tool()
        instance_tools[tool.name] = tool

        def parser_cmd(self, parser):
            tool._parser = parser
            tool.init_parser()
            tool.add_argument_output()
            tool.add_argument_stdout_output()

        def run_cmd(self, args):
            tool.cmd(args)

        return parser_cmd, run_cmd, tool

    for Tool in tools:

        parser_cmd, run_cmd, tool = generate_parser_and_run_functions(Tool)
        setattr(WordlistoolsCommand, f"run_{Tool.name}", run_cmd)
        setattr(WordlistoolsCommand, f"parser_{Tool.name}", parser_cmd)
        setattr(WordlistoolsCommand, f"description_{Tool.name}", Tool.description)

    command = WordlistoolsCommand()
    argcomplete.autocomplete(command.parser)
    args = command.parse_args(args)
    if args.subcommand is None:
        command.parser.print_help()
        sys.exit(1)

    tool = instance_tools[args.subcommand]
    # print("args befor _stdin_arg treatement", args)
    # print()
    # print("_stdin_arg", tool.name, tool._stdin_arg)ol
    if tool._stdin_arg:
        # Create dummy argparser juste to know the dest name
        # print("entering stdin_arg")
        dummy_parser = argparse.ArgumentParser()
        _stdin_arg = tool._stdin_arg
        arg = dummy_parser.add_argument(*_stdin_arg["args"], **_stdin_arg["kwargs"])
        argname = arg.dest
        #       print("args in stdin_arg", args)
        if _stdin_arg["action"] == "append":
            attr = getattr(args, argname)
            attr.append(_stdin_arg["value"])
        elif _stdin_arg["action"] == "create":
            setattr(args, argname, _stdin_arg["value"])

    # -------------------------
    # Handle outputs and stdout
    # -------------------------
    # get nb_tool_outputs
    if isinstance(tool.nb_outputs, int):
        nb_tool_outputs = tool.nb_outputs
    else:
        nb_tool_outputs = tool.nb_outputs(args)

    # number of output that the user is waiting
    if args.output:

        nb_user_output = len(args.output)
        # By default if outputs are present and stdin_output is not
        # Default stdin_output to None
        stdout_output = args.stdout_output
        if args.stdout_output is not None:
            nb_user_output += 1

    else:
        stdout_output = 0
        nb_user_output = 1

    # print(f"Number of user output {nb_user_output}")
    # print(f"Waiting for {nb_tool_outputs} outputs")
    if nb_user_output != nb_tool_outputs:
        msg = f"The number of the tool {tool.name} outputs ({nb_tool_outputs})"
        msg += f" is different than the number of expected output ({nb_user_output})"
        print(msg)
        sys.exit(1)

    # Init writers (files/stdout)
    writers = list(args.output)
    writers.insert(stdout_output, sys.stdout)

    # -------------------------
    # Run tool and print output
    # -------------------------
    results = tool.cmd(args)
    if isinstance(results, types.GeneratorType):
        for result in results:
            result = normalize_result(result)
            for i, e in enumerate(result):
                writers[i].write(e + "\n")
    else:
        result = normalize_result(results)
        for i, e in enumerate(result):
            writers[i].write(e + "\n")
