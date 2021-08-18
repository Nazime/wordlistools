from wordlistools.helpertest import AsStdinWordlist, AsWordlist, runtest


def test_simple():
    runtest(
        "occurrence",
        args=(AsStdinWordlist(["a", "b"]),),
        ret=AsWordlist(["1 a", "1 b"]),
    )

    runtest(
        "occurrence",
        args=(AsStdinWordlist(["a", "b", "b"]),),
        ret=AsWordlist(["1 a", "2 b"]),
    )

    runtest(
        "occurrence",
        args=(AsStdinWordlist(["a", "b", "a"]),),
        ret=AsWordlist(["2 a", "1 b"]),
    )

    # The first duplicate it will find is the 'b' and not the 'a'
    runtest(
        "occurrence",
        args=(AsStdinWordlist(["a", "b", "b", "a", "a"]),),
        ret=AsWordlist(["3 a", "2 b"]),
    )

    runtest(
        "occurrence",
        args=(AsStdinWordlist(["b", "b", "a"]),),
        ret=AsWordlist(["2 b", "1 a"]),
    )


def test_min():
    runtest(
        "occurrence",
        args=(AsStdinWordlist(["a", "b"]),),
        kwargs={"min": 3},
        ret=AsWordlist([]),
    )
    runtest(
        "occurrence",
        args=(AsStdinWordlist(["a", "a", "b", "b", "b"]),),
        kwargs={"min": 3},
        ret=AsWordlist(["3 b"]),
    )


def test_multiple_wordlists():
    runtest(
        "occurrence",
        args=(AsWordlist(["d", "b"]), AsStdinWordlist(["c", "b"])),
        ret=AsWordlist(["1 d", "2 b", "1 c"]),
    )
