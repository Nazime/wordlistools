import argparse
import sys
import types

from koalak import SubcommandParser
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


def main(args=None):
    """Tentative desepéré de le faire avec koalak"""
    if args is None:
        args = sys.argv[1:]

    # INIT PARSER
    wordlistools_cmd = SubcommandParser(
        "wordlistools",
        description=f"You can add your own plugin tools by adding a python script to {tools.homepath}",
        prolog=consts.ASCII_ART,
    )

    # ADD GROUPS
    wordlistools_cmd.add_group(
        "basic",
        title="Basic commands",
        description="Commands to interact with many wordlist at the same time",
    )

    wordlistools_cmd.add_group(
        "filters",
        title="Filters commands",
        description="Keep only words that match the filter",
    )

    wordlistools_cmd.add_group(
        "modifiers",
        title="Modifiers commands",
        description="Apply a modification to each word in the wordlist",
    )

    wordlistools_cmd.add_group(
        "statistics",
        title="Statistics commands",
        description="Tools to better understand the wordlist",
    )

    instance_tools = {}

    def generate_parser_and_run_functions(Tool, parser):
        tool = Tool()
        instance_tools[tool.name] = tool

        tool._parser = parser
        tool.init_parser()
        tool.add_argument_output()
        tool.add_argument_stdout_output()

    # Create subcommands dynamically
    for Tool in tools:
        wordlistools_tool_cmd = wordlistools_cmd.add_subcommand(
            Tool.name, group=Tool.group, description=Tool.description
        )

        generate_parser_and_run_functions(Tool, wordlistools_tool_cmd._argparse_parser)
        wordlistools_tool_cmd.function = lambda args: None

    # FIXME: add autocomplete argcomplete.autocomplete(command.parser)
    args = wordlistools_cmd.parse_args(args)
    if args.subcommand is None:
        wordlistools_cmd.print_help()
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
