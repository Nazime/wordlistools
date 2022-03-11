from wordlistools.helpertest import AsStdinWordlist, AsWordlist, runtest


def test_startswith():
    runtest(
        "startswith",
        args=("a", AsStdinWordlist(["ab", "aa", "ba"])),
        ret=AsWordlist(["ab", "aa"]),
    )

    runtest(
        "startswith",
        args=("test", AsStdinWordlist(["ab", "testaa", "test"])),
        ret=AsWordlist(["testaa", "test"]),
    )


def test_endswith():
    runtest(
        "endswith",
        args=("a", AsStdinWordlist(["ab", "aa", "ba"])),
        ret=AsWordlist(["aa", "ba"]),
    )

    runtest(
        "endswith",
        args=("test", AsStdinWordlist(["ab", "testaa", "test"])),
        ret=AsWordlist(["test"]),
    )


def test_dontstartswith():
    runtest(
        "dontstartswith",
        args=("a", AsStdinWordlist(["ab", "aa", "ba", "b"])),
        ret=AsWordlist(["ba", "b"]),
    )

    runtest(
        "dontstartswith",
        args=("test", AsStdinWordlist(["ab", "aatest", "test"])),
        ret=AsWordlist(["ab", "aatest"]),
    )

    runtest(
        "dontstartswith", args=("test", AsStdinWordlist([""])), ret=AsWordlist([""])
    )


def test_dontendswith():
    runtest(
        "dontendswith",
        args=("a", AsStdinWordlist(["ab", "aa", "ba"])),
        ret=AsWordlist(["ab"]),
    )

    runtest(
        "dontendswith",
        args=("test", AsStdinWordlist(["ab", "testaa", "aatest"])),
        ret=AsWordlist(["ab", "testaa"]),
    )

    runtest("dontendswith", args=("test", AsStdinWordlist([""])), ret=AsWordlist([""]))


def test_isdigit():
    runtest(
        "isdigit",
        args=(AsStdinWordlist(["ab", "123", "12a", "0"]),),
        ret=AsWordlist(["123", "0"]),
    )
