from wordlistools.helpertest import AsStdinWordlist, AsWordlist, runtest


def test_upper():

    runtest("upper", args=(AsStdinWordlist(["a", "b"]),), ret=AsWordlist(["A", "B"]))

    runtest(
        "upper",
        args=(AsStdinWordlist(["aAa", "bB", "12a", "13", "A"]),),
        ret=AsWordlist(["AAA", "BB", "12A", "13", "A"]),
    )


def test_lower():

    runtest("lower", args=(AsStdinWordlist(["A", "B"]),), ret=AsWordlist(["a", "b"]))

    runtest(
        "lower",
        args=(AsStdinWordlist(["aAa", "bB", "12A", "13", "a"]),),
        ret=AsWordlist(["aaa", "bb", "12a", "13", "a"]),
    )


def test_capitalize():

    runtest(
        "capitalize",
        args=(AsStdinWordlist(["hello", "hey", "Test", "hey hey"]),),
        ret=AsWordlist(["Hello", "Hey", "Test", "Hey hey"]),
    )


def test_invert():

    runtest(
        "invert", args=(AsStdinWordlist(["Aa", "Bb"]),), ret=AsWordlist(["aA", "bB"])
    )

    runtest(
        "invert",
        args=(AsStdinWordlist(["aAa", "bB", "a21", "azerty", "13", "a"]),),
        ret=AsWordlist(["aAa", "Bb", "12a", "ytreza", "31", "a"]),
    )


def test_replace():

    runtest(
        "replace",
        args=("a", "b", AsStdinWordlist(["Aa", "Bb", "b"])),
        ret=AsWordlist(["Ab", "Bb", "b"]),
    )

    runtest(
        "replace",
        args=("test", "nop", AsStdinWordlist(["testtest", "testing", "tes"])),
        ret=AsWordlist(["nopnop", "noping", "tes"]),
    )
