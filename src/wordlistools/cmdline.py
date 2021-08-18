import argparse
import sys
import types

import argcomplete

from . import tools


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
    if args is None:
        args = sys.argv[1:]

    main_parser = argparse.ArgumentParser(
        "wordlistool",
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


def main3(args=None):
    # print()
    # print("main\n====")
    # print("main", args)
    # print("stdin in main", sys.stdin, sys.stdin.isatty())
    if args is None:
        args = sys.argv[1:]
    # init parser
    main_parser = argparse.ArgumentParser(
        "wordlistool",
        description=f"You can add your own plugin tools by adding a python script to {tools.homepath}",
    )
    subparsers = main_parser.add_subparsers(dest="subcommand", help="Tool to run")

    # init subcommand from tool plugin manager
    for tool in tools:
        subparser = subparsers.add_parser(tool.name, help=tool.description)
        tool._parser = subparser
        tool._usable_with_stdin = False
        tool.init_parser()

    # run subcommand
    argcomplete.autocomplete(main_parser)
    args = main_parser.parse_args(args)
    if args.subcommand is None:
        main_parser.print_help()
        sys.exit(1)

    tool = tools[args.subcommand]
    # print("args befor _stdin_arg treatement", args)
    if hasattr(tool, "_stdin_arg"):
        # Create dummy argparser juste to know the dest name
        print(tool, tool._stdin_arg)
        dummy_parser = argparse.ArgumentParser()
        _stdin_arg = tool._stdin_arg
        arg = dummy_parser.add_argument(*_stdin_arg["args"], **_stdin_arg["kwargs"])
        argname = arg.dest
        setattr(args, argname, _stdin_arg["stdin_default"])

    """
    # Handle PIPE ( | ) and stdin rediraction <
    if not sys.stdin.isatty():  # Called from pipe or stdin redirection
        # Must have either wordlist or wordlists args not both

        if hasattr(args, "wordlists"):
            args.wordlists.append(None)

        elif hasattr(args, "wordlist"):

            if args.wordlist is not None:
                print(
                    f"Can't have argument wordlist for subcmd {args.subcommand}, already there from stdin"
                )
                sys.exit(1)
            args.wordlist = (
                None
            )  # If it's None normalize_wordlist will readit from stdin

        else:
            print(
                f"Subcmd {args.subcommand} must have at least wordlist or wordlists argument"
            )
            sys.exit(1)

    else:
        # Check that arguments are not None
        if hasattr(args, "wordlist"):
            if args.wordlist is None:
                print(
                    f"Wordlist argument is missing for subcommand {args.subcommand} (since it's not piped)"
                )
                sys.exit(1)
    """
    # print("args befor tool.cmd", args)
    result = tool.cmd(args)

    if isinstance(result, types.GeneratorType):
        for e in result:
            print(e)
    elif isinstance(result, int):
        print(result)
