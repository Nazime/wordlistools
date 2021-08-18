"""Helper class for unitest"""
import io
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from typing import Any, Dict, List, Tuple

from koalak.utils import file2stdin
from wordlistools import api
from wordlistools.cmdline import main


def _normalize_api_argument(arg):
    if isinstance(arg, Argument):
        return arg.value
    else:
        return arg


class PolyArgument:
    def __init__(
        self, *, api_key: str = None, api_value: Any = None, cmd_args: List[str] = None
    ):
        """Use it when API arguments are different then cmdline argument
        Example when the cmdline argument have the action store_true"""

        if api_key is not None and api_value is None:
            raise TypeError(f"If api_key is present, api_value must be present")
        if cmd_args is not None and not isinstance(cmd_args, list):
            raise TypeError(f"cmd_args must be a list of strings")

        self.api_key = api_key
        self.api_value = api_value
        self.cmd_args = cmd_args


class Argument:
    def __init__(self, value, wordlist=False, stdin=False):
        if wordlist and not isinstance(value, list):
            raise TypeError(f"value must be a list when wordlist is True")
        self.value = value
        self.wordlist = wordlist
        self.stdin = stdin


def AsWordlist(value):
    return Argument(value, wordlist=True)


def AsStdin(value):
    return Argument(value, stdin=True)


def AsStdinWordlist(value):
    return Argument(value, wordlist=True, stdin=True)


def runtest(
    tool_name: str, *, args: Tuple = None, kwargs: Dict = None, ret: Any = None
):
    """The main helper function to test a wordlist tool
    This function will test the tool in API mode, cmdline mode, and with
    stdin if specified.

    Args:
        tool_name: name of the wordlist tool to test
        args: arguments for the tool and poly arguments (see PolyArguments)
        kwargs: keyword arguments for the wordlist
        poly_kwargs: keywords poly arguments, since we can not
            add poly argument in a dictionary (syntax must be key:value
            not value alone)
        ret: the expected return with the specified args/kwargs
    """
    # Check args
    args = args if args is not None else tuple()
    kwargs = kwargs if kwargs is not None else {}

    if not isinstance(args, tuple):
        raise TypeError(f"args must be of type Tuple")
    if not isinstance(kwargs, dict):
        raise TypeError(f"kwargs must be of type Dict")
    if not isinstance(tool_name, str):
        raise TypeError(f"tool_name must be of type str")
    # print("called with", tool_name, args, kwargs, ret)
    # --
    # Normalize arguments
    # --

    # normalize API arguments
    api_args = []
    api_kwargs = {}
    api_ret = _normalize_api_argument(ret)

    for arg in args:
        if isinstance(arg, PolyArgument):
            # If api_key is None that mean it's an args and not a kwargs
            if arg.api_key is None:
                if arg.api_value is not None:
                    api_args.append(_normalize_api_argument(arg))
                else:
                    pass  # Do nothing
            # add it to kwargs
            else:
                # check that kwargs don't exist
                assert arg.api_key not in api_kwargs
                api_kwargs[arg.api_key] = _normalize_api_argument(arg.api_value)
        # Not a poly argument, add it to ap_args
        else:
            api_args.append(_normalize_api_argument(arg))

    for key, value in kwargs.items():
        assert key not in api_kwargs
        api_kwargs[key] = _normalize_api_argument(value)

    # --
    # Test API
    # --

    toolapi = getattr(api, tool_name)
    # print(tool_name, "api_args", api_args, "api_kwargs", api_kwargs)
    real_ret = toolapi(*api_args, **api_kwargs)
    # print("real_ret", real_ret)
    if isinstance(api_ret, int):
        assert api_ret == real_ret
    else:
        # print(real_ret)
        # print(api_ret)
        real_list = list(real_ret)
        expected_list = list(api_ret)
        # print("expected", type(expected_list), expected_list)
        # print("real", type(real_list), real_list)
        x = real_list == expected_list
        # print(x)
        # x = True
        assert True
        assert x

    # --
    # normalize cmd arguments
    # --

    tmp_files = []  # Files created from wordlists, store them to close after
    cmd_args = [tool_name]
    stdin_args = [tool_name]
    test_stdin = False  # If we are going to test stdin or not
    stdin_file = None
    for arg in args:
        if isinstance(arg, Argument):
            if arg.stdin:
                # Check if there is another stdin argument
                if test_stdin:
                    raise TypeError(f"Can't have two arguments with stdin True")
                test_stdin = True

            if arg.wordlist:
                # Create a temporary file from the wordlist
                tmp_file = tempfile.NamedTemporaryFile()
                tmp_files.append(tmp_file)
                tmp_file.write(("\n".join(arg.value) + "\n").encode())
                tmp_file.flush()
                # add argument filename for cmd_args and stdin_args
                arg.value = tmp_file.name

            cmd_args.append(arg.value)
            if arg.stdin:
                stdin_file = arg.value
            else:
                stdin_args.append(arg.value)

        elif isinstance(arg, PolyArgument):
            if arg.cmd_args is not None:
                cmd_args.extend(arg.cmd_args)
                stdin_args.extend(arg.cmd_args)
        else:
            if isinstance(arg, int):
                arg = str(arg)
            cmd_args.append(arg)
            stdin_args.append(arg)

    for key, value in kwargs.items():
        cmd_args.append(f"--{key}")
        stdin_args.append(f"--{key}")
        if isinstance(value, list):
            for v in value:
                cmd_args.append(v)
                stdin_args.append(v)
        else:
            if isinstance(value, int):
                value = str(value)
            cmd_args.append(value)
            stdin_args.append(value)

    # Run tests for cmd
    # print("process_args", cmd_args)
    f_stdout = io.StringIO()
    f_stderr = io.StringIO()
    # print("Before main(cmd_args) stdin", sys.stdin)
    with redirect_stdout(f_stdout), redirect_stderr(f_stderr):
        main(cmd_args)

    # Assert no error (stderr)
    assert f_stderr.getvalue() == ""
    # Assert stdout is the normal output line by line
    if isinstance(api_ret, int):
        real_ret = f_stdout.getvalue().strip()
        # print("real_ret cmd", repr(real_ret))
        assert int(real_ret) == api_ret
    else:
        real_result = f_stdout.getvalue().strip()
        expected_result = "\n".join(list(api_ret))
        # print("real_result", repr(real_result))
        # print("expected_result", repr(expected_result))
        assert real_result == expected_result

    # Run tests for stdin
    if test_stdin:
        # print("Enter STDIN testing")
        # print("stdin_args", stdin_args)
        # print("STDIN BEFORE", sys.stdin)
        with file2stdin(stdin_file):
            # print("STDIN AFTER", sys.stdin)
            f_stdout = io.StringIO()
            f_stderr = io.StringIO()
            with redirect_stdout(f_stdout), redirect_stderr(f_stderr):
                main(stdin_args)
            # Assert no error (stderr)
            assert f_stderr.getvalue() == ""
            # Assert stdout is the normal output line by line
            if isinstance(api_ret, int):
                real_ret = f_stdout.getvalue().strip()
                # print("real_ret", real_ret)
                assert int(real_ret) == api_ret
            else:
                real_result = f_stdout.getvalue().strip()
                expected_result = "\n".join(list(api_ret))
                # print("real_result", repr(real_result))
                # print("expected_result", repr(expected_result))
                assert real_result == expected_result
        # print("stdin AFTER AFTER", sys.stdin)
    # Clean files
    # FIXME: add finally close to clean?
    for tmp_file in tmp_files:
        tmp_file.close()


def print_debug(string):
    print(string)
