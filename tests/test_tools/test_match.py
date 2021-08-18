from wordlistools.helpertest import AsStdinWordlist, AsWordlist, PolyArgument, runtest
from wordlistools.plugins import red


def test_color_false():
    color_arg_false = PolyArgument(
        api_key="color", api_value=False, cmd_args=["--color", "no"]
    )

    runtest(
        "match",
        args=("a", AsStdinWordlist(["a", "b", "aa", "ab", "ba"]), color_arg_false),
        ret=AsWordlist(["a", "aa", "ab", "ba"]),
    )

    # test *
    runtest(
        "match",
        args=("a*", AsStdinWordlist(["a", "b", "aa", "ab", "ba"]), color_arg_false),
        ret=AsWordlist(["a", "b", "aa", "ab", "ba"]),
    )

    # test +
    runtest(
        "match",
        args=("a+", AsStdinWordlist(["a", "b", "aa", "ab", "ba"]), color_arg_false),
        ret=AsWordlist(["a", "aa", "ab", "ba"]),
    )

    # test repetition
    runtest(
        "match",
        args=("a{2}", AsStdinWordlist(["aba", "baa", "caaa"]), color_arg_false),
        ret=AsWordlist(["baa", "caaa"]),
    )

    # test start ^
    runtest(
        "match",
        args=("^a", AsStdinWordlist(["a", "baa", "ab"]), color_arg_false),
        ret=AsWordlist(["a", "ab"]),
    )

    # test end $
    runtest(
        "match",
        args=("a$", AsStdinWordlist(["a", "baa", "ab"]), color_arg_false),
        ret=AsWordlist(["a", "baa"]),
    )


def test_color_true():
    for cmd_args in (["--color", "yes"], ["--color"]):
        color_arg_true = PolyArgument(
            api_key="color", api_value=True, cmd_args=cmd_args
        )

        runtest(
            "match",
            args=("a", AsStdinWordlist(["a", "b", "aa", "ab", "ba"]), color_arg_true),
            ret=AsWordlist([red("a"), red("a") + "a", f"{red('a')}b", f"b{red('a')}"]),
        )

        # test *
        runtest(
            "match",
            args=("a*", AsStdinWordlist(["a", "b", "aa", "ab", "ba"]), color_arg_true),
            ret=AsWordlist([red("a"), "b", red("aa"), f"{red('a')}b", f"ba"]),
            # Last one is tricky re.search("a*", "ba") will match in index 0 an not 1
        )

        # test +
        runtest(
            "match",
            args=("a+", AsStdinWordlist(["a", "b", "aa", "ab", "ba"]), color_arg_true),
            ret=AsWordlist([red("a"), red("aa"), red("a") + "b", "b" + red("a")]),
        )

        # test repetition
        runtest(
            "match",
            args=("a{2}", AsStdinWordlist(["aba", "baa", "caaa"]), color_arg_true),
            ret=AsWordlist(["b" + red("aa"), "c" + red("aa") + "a"]),
        )

        # test start ^
        runtest(
            "match",
            args=("^a", AsStdinWordlist(["a", "baa", "ab"]), color_arg_true),
            ret=AsWordlist([red("a"), red("a") + "b"]),
        )

        # test end $
        runtest(
            "match",
            args=("a$", AsStdinWordlist(["a", "baa", "ab"]), color_arg_true),
            ret=AsWordlist([red("a"), "ba" + red("a")]),
        )
