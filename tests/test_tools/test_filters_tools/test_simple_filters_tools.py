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


def test_isdigit():
    runtest(
        "isdigit",
        args=(AsStdinWordlist(["ab", "123", "12a", "0"]),),
        ret=AsWordlist(["123", "0"]),
    )
