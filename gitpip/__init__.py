"""git pip moduule

module to install modules from git repositories"""

from ._main import main as _main1
import sys

__version__ = "1.0.0"

def main(*argv):
    # type: (str) -> int
    """
    main function

    :param argv: argv strings
    """
    if not all(map(lambda v: isinstance(v, str), argv)):
        raise TypeError("expected all argv as str object")

    if len(argv) == 0:
        argv = sys.argv[1:]

    if not isinstance(argv, list):
        argv = list(argv) # type: list[str]

    return _main1(argv)