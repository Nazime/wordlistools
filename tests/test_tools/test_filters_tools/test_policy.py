import pytest
from wordlistools.helpertest import AsStdinWordlist, AsWordlist, PolyArgument, runtest


def test_policy_simple_base_policy():
    runtest(
        "policy",
        # test lowercase
        args=("a", AsStdinWordlist(["a", "A", "AA", "aA", "abCd"])),
        ret=AsWordlist(["a", "aA", "abCd"]),
    )

    runtest(
        "policy",
        # test uppercase
        args=("A", AsStdinWordlist(["a", "A", "AA", "aA", "abCd"])),
        ret=AsWordlist(["A", "AA", "aA", "abCd"]),
    )

    runtest(
        "policy",
        # test one digit
        args=("1", AsStdinWordlist(["a", "A", "AA", "aA", "abCd"])),
        ret=AsWordlist([]),
    )

    runtest(
        "policy",
        # test one digit
        args=("1", AsStdinWordlist(["a1", "A", "A2A", "aA", "abCd", "12"])),
        ret=AsWordlist(["a1", "A2A", "12"]),
    )

    runtest(
        "policy",
        # test one special char
        args=("@", AsStdinWordlist(["a1@", "A", "A!2A", "_aA", "abCd", "12"])),
        ret=AsWordlist(["a1@", "A!2A", "_aA"]),
    )


def test_policy_mixed_base_policy():
    runtest(
        "policy",
        # test lower and upper
        args=("aA", AsStdinWordlist(["a", "A", "AA", "aA", "abCd"])),
        ret=AsWordlist(["aA", "abCd"]),
    )

    runtest(
        "policy",
        # test upper and digit
        args=("A1", AsStdinWordlist(["a1@", "A", "A!2A", "_aA", "abCd", "12"])),
        ret=AsWordlist(["A!2A"]),
    )

    runtest(
        "policy",
        # test all must be present (lower, upper, special, digit)
        args=("A@1a", AsStdinWordlist(["a1@", "A", "A!2A", "_aA", "abCd", "12"])),
        ret=AsWordlist([]),
    )

    runtest(
        "policy",
        # test all must be present (lower, upper, special, digit)
        args=("A@1a", AsStdinWordlist(["a1@", "A", "A!2Aa", "_aA", "abCd", "12"])),
        ret=AsWordlist(["A!2Aa"]),
    )


def test_policy_length():
    runtest(
        "policy",
        args=("==2", AsStdinWordlist(["a", "bb", "aBc", "abCD", "abCDe"])),
        ret=AsWordlist(["bb"]),
    )

    runtest(
        "policy",
        args=("!=2", AsStdinWordlist(["a", "bb", "aBc", "abCD", "abCDe"])),
        ret=AsWordlist(["a", "aBc", "abCD", "abCDe"]),
    )

    runtest(
        "policy",
        args=(">2", AsStdinWordlist(["a", "bb", "aBc", "abCD", "abCDe"])),
        ret=AsWordlist(["aBc", "abCD", "abCDe"]),
    )

    runtest(
        "policy",
        args=(">=4", AsStdinWordlist(["a", "bb", "aBc", "abCD", "abCDe"])),
        ret=AsWordlist(["abCD", "abCDe"]),
    )

    runtest(
        "policy",
        args=("<3", AsStdinWordlist(["a", "bb", "aBc", "abCD", "abCDe"])),
        ret=AsWordlist(["a", "bb"]),
    )

    runtest(
        "policy",
        args=("<=3", AsStdinWordlist(["a", "bb", "aBc", "abCD", "abCDe"])),
        ret=AsWordlist(["a", "bb", "aBc"]),
    )


def test_policy_complicated_policy():
    runtest(
        "policy",
        args=("aA==2", AsStdinWordlist(["a", "bb", "aBc", "abCD", "abCDe"])),
        ret=AsWordlist([]),
    )

    runtest(
        "policy",
        args=("aA==2", AsStdinWordlist(["a", "bB", "aBc", "abCD", "abCDe"])),
        ret=AsWordlist(["bB"]),
    )

    runtest(
        "policy",
        args=("1!=2", AsStdinWordlist(["a", "bB", "aBc", "abCD", "abCDe"])),
        ret=AsWordlist([]),
    )
    runtest(
        "policy",
        args=("1!=2", AsStdinWordlist(["a2", "bB1", "aB1c", "abCD", "abCDe"])),
        ret=AsWordlist(["bB1", "aB1c"]),
    )


def test_policy_error():
    with pytest.raises(ValueError):
        runtest(
            "policy",
            # wrong policy
            args=("2", AsStdinWordlist(["a", "bb", "aBc", "abCD", "abCDe"])),
            ret=AsWordlist(["bb"]),
        )

    with pytest.raises(ValueError):
        runtest(
            "policy",
            # empty policy
            args=("", AsStdinWordlist(["a", "bb", "aBc", "abCD", "abCDe"])),
            ret=AsWordlist(["bb"]),
        )


def test_policy_n_argument():
    n = 1
    n_arg = PolyArgument(api_key="n", api_value=n, cmd_args=["-n", str(n)])
    runtest(
        "policy",
        args=("aA", AsStdinWordlist(["a", "A", "1"]), n_arg),
        ret=AsWordlist(["a", "A"]),
    )

    n = 2
    n_arg = PolyArgument(api_key="n", api_value=n, cmd_args=["-n", str(n)])
    runtest(
        "policy",
        args=("aA1", AsStdinWordlist(["aA", "AAA", "12ab", "B8"]), n_arg),
        ret=AsWordlist(["aA", "12ab", "B8"]),
    )


def test_policy_n_error():
    with pytest.raises(ValueError):
        n = 0
        n_arg = PolyArgument(api_key="n", api_value=n, cmd_args=["-n", str(n)])
        runtest(
            "policy",
            args=("aA", AsStdinWordlist(["a", "A", "1"]), n_arg),
            ret=AsWordlist(["a", "A"]),
        )

    with pytest.raises(ValueError):
        n = 2
        n_arg = PolyArgument(api_key="n", api_value=n, cmd_args=["-n", str(n)])
        runtest(
            "policy",
            args=("aA", AsStdinWordlist(["a", "A", "1"]), n_arg),
            ret=AsWordlist(["a", "A"]),
        )

    with pytest.raises(ValueError):
        n = 3
        n_arg = PolyArgument(api_key="n", api_value=n, cmd_args=["-n", str(n)])
        runtest(
            "policy",
            args=("aA", AsStdinWordlist(["a", "A", "1"]), n_arg),
            ret=AsWordlist(["a", "A"]),
        )

    with pytest.raises(ValueError):
        n = -2
        n_arg = PolyArgument(api_key="n", api_value=n, cmd_args=["-n", str(n)])
        runtest(
            "policy",
            args=("aA", AsStdinWordlist(["a", "A", "1"]), n_arg),
            ret=AsWordlist(["a", "A"]),
        )
