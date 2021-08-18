from wordlistools.helpertest import AsStdinWordlist, AsWordlist, PolyArgument, runtest
from wordlistools.plugins import red


def test_color_false():
    # By default color is enabled in cmdline and disabled in API
    color_arg_false = PolyArgument(
        api_key="color", api_value=False, cmd_args=["--color", "no"]
    )
    runtest(
        "search",
        args=("a", AsStdinWordlist(["a", "b"]), color_arg_false),
        ret=AsWordlist(["a"]),
    )

    runtest(
        "search",
        args=(
            "a",
            AsStdinWordlist(["alpha", "beta", "gama", "omega"]),
            color_arg_false,
        ),
        ret=AsWordlist(["alpha", "beta", "gama", "omega"]),
    )

    runtest(
        "search",
        args=("bc", AsStdinWordlist(["abc", "xbc", "eff", "bxc"]), color_arg_false),
        ret=AsWordlist(["abc", "xbc"]),
    )

    # TODO: test multiple wordlist


def test_color_true():
    for cmd_args in (["--color", "yes"], ["--color"]):
        color_arg_true = PolyArgument(
            api_key="color", api_value=True, cmd_args=cmd_args
        )
        runtest(
            "search",
            args=("a", AsStdinWordlist(["a", "b"]), color_arg_true),
            ret=AsWordlist([red("a")]),
        )

        runtest(
            "search",
            args=(
                "a",
                AsStdinWordlist(["alpha", "beta", "gama", "omega"]),
                color_arg_true,
            ),
            ret=AsWordlist(
                [
                    f"{red('a')}lpha",
                    f"bet{red('a')}",
                    f"g{red('a')}ma",
                    f"omeg{red('a')}",
                ]
            ),
        )

        runtest(
            "search",
            args=("bc", AsStdinWordlist(["abc", "xbc", "eff", "bxc"]), color_arg_true),
            ret=AsWordlist([f"a{red('bc')}", f"x{red('bc')}"]),
        )
