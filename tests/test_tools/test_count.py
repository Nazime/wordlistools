from wordlistools.helpertest import AsStdinWordlist, runtest


def test_simple():
    runtest("count", args=(AsStdinWordlist(["a", "b"]),), ret=2)

    runtest("count", args=(AsStdinWordlist(["a", "b", "c", "d", "e"]),), ret=5)


def test_search():
    runtest(
        "count",
        args=(AsStdinWordlist(["aa", "ab", "b"]),),
        kwargs={"pattern": "a"},
        ret=2,
    )

    runtest(
        "count",
        args=(AsStdinWordlist(["read", "rat", "at", "atmo"]),),
        kwargs={"pattern": "at"},
        ret=3,
    )
