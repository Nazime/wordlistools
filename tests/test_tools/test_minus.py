from wordlistools.helpertest import AsStdinWordlist, AsWordlist, runtest


def test_simple():
    # Simple case
    runtest(
        "minus",
        args=(AsWordlist(["a", "b"]), AsWordlist(["b"])),
        ret=AsStdinWordlist(["a"]),
    )

    # Two wordlists to subtract
    runtest(
        "minus",
        args=(
            AsWordlist(["a", "b", "c", "d"]),
            AsWordlist(["b", "c"]),
            AsStdinWordlist(["a"]),
        ),
        ret=AsWordlist(["d"]),
    )

    # No word match subtraction
    runtest(
        "minus",
        args=(AsWordlist(["a", "b"]), AsStdinWordlist(["c", "d"])),
        ret=AsWordlist(["a", "b"]),
    )
