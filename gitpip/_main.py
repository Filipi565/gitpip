from pip._internal.cli.main import main as _main
import subprocess as sp
import tempfile
import shutil
import os
from .const import RED, RESET

def _git_argv(*args):
    yield str("git")
    yield str("clone")
    yield from map(str, args)

def _clean_dir(dir):
    # type: (str | bytes | bytearray | memoryview) -> None
    if not isinstance(dir, str):
        dir = bytes(dir)

    for _ in range(2):
        for root, dirs, files in os.walk(dir):
            for file in files:
                path = os.path.join(root, file)
                try:
                    os.remove(path)
                except OSError:
                    pass
            
            for dirname in dirs:
                path = os.path.join(root, dirname)
                shutil.rmtree(dirname, ignore_errors=True)
    
    shutil.rmtree(dir, ignore_errors=True)
            
def main(argv):
    # type: (list[str]) -> int
    if not len(argv) >= 1:
        msg = "%sError: No Argument Given%s" % (RED, RESET)
        print(msg)
        return 1

    giturl = argv.pop(0)

    if not giturl.startswith(("http://", "https://")) and not "@" in giturl:
        giturl = "https://github.com/%s" % giturl

    temp_dir = tempfile.mkdtemp(suffix=".tmp")
    
    git = sp.Popen([*_git_argv(giturl, temp_dir)], stdout=sp.PIPE, stderr=sp.PIPE, text=True)

    return_code = git.wait()

    if return_code != 0:
        _clean_dir(temp_dir)
        msg = "%sError: %s%s" % (RED, git.stderr.read(), RESET)
        print(msg)
        return return_code
    
    argv = ["install", temp_dir] + argv
    return_code = _main(argv)

    _clean_dir(temp_dir)
    return return_code