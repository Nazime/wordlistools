import pytest
from koalak.utils import temp_str2filename
from wordlistools.helpertest import AsStdin, AsWordlist, runtest

data = """/images (Status: 301)
/index.php (Status: 200)
/media (Status: 301)
/templates (Status: 301)
/modules (Status: 301)
/bin (Status: 301)
/plugins (Status: 301)
/includes (Status: 301)
/language (Status: 301)
"""


# TODO: fixme
@pytest.mark.skip
def test_2simple():
    with temp_str2filename(data) as filename:
        runtest(
            "parse",
            args=("gobuster", AsStdin(filename)),
            ret=AsWordlist(
                [
                    "images",
                    "index.php",
                    "media",
                    "templates",
                    "modules",
                    "bin",
                    "plugins",
                    "includes",
                    "language",
                ]
            ),
        )
