from wordlistools.helpertest import AsStdinWordlist, AsWordlist, runtest


def test_simple():
    runtest("duplicate", args=(AsStdinWordlist(["a", "b"]),), ret=AsWordlist([]))

    runtest(
        "duplicate", args=(AsStdinWordlist(["a", "b", "b"]),), ret=AsWordlist(["b"])
    )

    runtest(
        "duplicate", args=(AsStdinWordlist(["a", "b", "a"]),), ret=AsWordlist(["a"])
    )

    # The first duplicate it will find is the 'b' and not the 'a'
    runtest(
        "duplicate",
        args=(AsStdinWordlist(["a", "b", "b", "a", "a"]),),
        ret=AsWordlist(["b", "a"]),
    )

    runtest(
        "duplicate", args=(AsStdinWordlist(["b", "b", "a"]),), ret=AsWordlist(["b"])
    )


def test_min():
    runtest(
        "duplicate",
        args=(AsStdinWordlist(["a", "b"]),),
        kwargs={"min": 3},
        ret=AsWordlist([]),
    )
    runtest(
        "duplicate",
        args=(AsStdinWordlist(["a", "a", "b", "b", "b"]),),
        kwargs={"min": 3},
        ret=AsWordlist(["b"]),
    )


def test_multiple_wordlists():
    runtest(
        "duplicate",
        args=(AsWordlist(["d", "b"]), AsStdinWordlist(["c", "b"])),
        ret=AsWordlist(["b"]),
    )
