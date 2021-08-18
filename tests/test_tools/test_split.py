from wordlistools.helpertest import AsStdinWordlist, AsWordlist, PolyArgument, runtest

# TODO: unique by default True or False?


def test_col():
    runtest(
        "split",
        args=(":", AsStdinWordlist(["a:c", "b:d"])),
        kwargs={"col": 0},
        ret=AsWordlist(["a", "b"]),
    )

    runtest(
        "split",
        args=(":", AsStdinWordlist(["a:c", "b:d"])),
        kwargs={"col": 1},
        ret=AsWordlist(["c", "d"]),
    )


def test_unique():
    runtest(
        "split",
        args=(
            ":",
            AsStdinWordlist(["a:c", "a:d", "b:c", "b:d"]),
            PolyArgument(api_key="unique", api_value=True),
        ),
        kwargs={"col": 0},
        ret=AsWordlist(["a", "b"]),
    )

    runtest(
        "split",
        args=(
            ":",
            AsStdinWordlist(["a:c", "a:d", "b:c", "b:d"]),
            PolyArgument(api_key="unique", api_value=False, cmd_args=["--repeat"]),
        ),
        kwargs={"col": 0},
        ret=AsWordlist(["a", "a", "b", "b"]),
    )


"""
def test_multiple():
    helper_testtool(
        "product",
        args=(AsWordlist(["a", "b"]), AsWordlist(["c", "d"]), AsWordlist(["e", "f"])),
        ret=AsWordlist(["ace", "acf", "ade", "adf", "bce", "bcf", "bde", "bdf"]),
    )


def test_multiple_with_sep():
    helper_testtool(
        "product",
        args=(AsWordlist(["a", "b"]), AsWordlist(["c", "d"]), AsWordlist(["e", "f"])),
        kwargs={"sep": ":"},
        ret=AsWordlist(
            ["a:c:e", "a:c:f", "a:d:e", "a:d:f", "b:c:e", "b:c:f", "b:d:e", "b:d:f"]
        ),
    )
"""
