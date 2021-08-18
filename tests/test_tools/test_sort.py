from wordlistools.helpertest import AsStdinWordlist, AsWordlist, runtest


def test_simple():
    runtest("sort", args=(AsStdinWordlist(["a", "b"]),), ret=AsWordlist(["a", "b"]))

    runtest("sort", args=(AsStdinWordlist(["b", "a"]),), ret=AsWordlist(["a", "b"]))


def test_multiple_wordlists():
    runtest(
        "sort",
        args=(AsWordlist(["b", "a"]), AsStdinWordlist(["c"])),
        ret=AsWordlist(["a", "b", "c"]),
    )

    runtest(
        "sort",
        args=(AsWordlist(["b", "a"]), AsStdinWordlist(["a"])),
        ret=AsWordlist(["a", "a", "b"]),
    )

    runtest(
        "sort",
        args=(AsWordlist(["d", "b"]), AsStdinWordlist(["c", "a"])),
        ret=AsWordlist(["a", "b", "c", "d"]),
    )
