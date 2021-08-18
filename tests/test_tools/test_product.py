from wordlistools.helpertest import AsWordlist, runtest


def test_simple():
    runtest(
        "product",
        args=(AsWordlist(["a", "b"]), AsWordlist(["c", "d"])),
        ret=AsWordlist(["ac", "ad", "bc", "bd"]),
    )


def test_sep():
    runtest(
        "product",
        args=(AsWordlist(["a", "b"]), AsWordlist(["c", "d"])),
        kwargs={"sep": ":"},
        ret=AsWordlist(["a:c", "a:d", "b:c", "b:d"]),
    )


def test_multiple():
    runtest(
        "product",
        args=(AsWordlist(["a", "b"]), AsWordlist(["c", "d"]), AsWordlist(["e", "f"])),
        ret=AsWordlist(["ace", "acf", "ade", "adf", "bce", "bcf", "bde", "bdf"]),
    )


def test_multiple_with_sep():
    runtest(
        "product",
        args=(AsWordlist(["a", "b"]), AsWordlist(["c", "d"]), AsWordlist(["e", "f"])),
        kwargs={"sep": ":"},
        ret=AsWordlist(
            ["a:c:e", "a:c:f", "a:d:e", "a:d:f", "b:c:e", "b:c:f", "b:d:e", "b:d:f"]
        ),
    )
