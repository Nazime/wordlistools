from wordlistools.helpertest import AsStdinWordlist, AsWordlist, runtest


def test_simple():
    runtest(
        "merge",
        args=(AsWordlist(["a", "b"]), AsStdinWordlist(["c", "d"])),
        ret=AsWordlist(["a", "b", "c", "d"]),
    )


def test_multiple():

    runtest(
        "merge",
        args=(
            AsWordlist(["a", "b"]),
            AsWordlist(["c", "d"]),
            AsStdinWordlist(["e", "f"]),
        ),
        ret=AsWordlist(["a", "b", "c", "d", "e", "f"]),
    )
