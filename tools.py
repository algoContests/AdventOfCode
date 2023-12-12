import sys


def debug(*args):
    # return
    print(*args, file=sys.stderr)
    sys.stderr.flush()