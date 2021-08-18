from wordlistools.helpertest import AsStdinWordlist, AsWordlist, runtest


def test_extensions():

    runtest(
        "backup",
        args=(AsStdinWordlist(["a", "b"]),),
        kwargs={"extensions": [".bak", ".old"]},
        ret=AsWordlist(["a.bak", "a.old", "b.bak", "b.old"]),
    )


def test_add():
    runtest(
        "backup",
        args=(AsStdinWordlist(["a", "b"]),),
        kwargs={"extensions": [".bak", ".old"], "add": ["~"]},
        ret=AsWordlist(["a.bak", "a.old", "a~", "b.bak", "b.old", "b~"]),
    )


def test_remove():
    runtest(
        "backup",
        args=(AsStdinWordlist(["a", "b"]),),
        kwargs={"extensions": [".bak", ".old"], "remove": [".old"]},
        ret=AsWordlist(["a.bak", "b.bak"]),
    )


def test_not_modify_extensions():
    extensions = [".bak", ".old"]
    runtest(
        "backup",
        args=(AsStdinWordlist(["a", "b"]),),
        kwargs={"extensions": extensions, "add": ["~"]},
        ret=AsWordlist(["a.bak", "a.old", "a~", "b.bak", "b.old", "b~"]),
    )
    assert extensions == [".bak", ".old"]
