from wordlistools.helpertest import AsStdinWordlist, AsWordlist, runtest


def test_simple():
    runtest("unique", args=(AsStdinWordlist(["a", "b"]),), ret=AsWordlist(["a", "b"]))

    runtest(
        "unique", args=(AsStdinWordlist(["a", "b", "b"]),), ret=AsWordlist(["a", "b"])
    )

    runtest(
        "unique", args=(AsStdinWordlist(["a", "b", "a"]),), ret=AsWordlist(["a", "b"])
    )

    runtest(
        "unique",
        args=(AsStdinWordlist(["a", "b", "b", "a", "a"]),),
        ret=AsWordlist(["a", "b"]),
    )

    runtest(
        "unique", args=(AsStdinWordlist(["b", "b", "a"]),), ret=AsWordlist(["b", "a"])
    )


def test_multiple_wordlists():
    runtest(
        "unique",
        args=(AsWordlist(["d", "b"]), AsStdinWordlist(["c", "b"])),
        ret=AsWordlist(["d", "b", "c"]),
    )
