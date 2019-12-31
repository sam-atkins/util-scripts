#!/usr/bin/env python3
"""
Command line interface to difflib.py providing diffs in four formats:

* ndiff:    lists every line and highlights interline changes.
* context:  highlights clusters of changes in a before/after format.
* unified:  highlights clusters of changes in an inline format.
* html:     generates side by side comparison with change highlights.

Source:
https://docs.python.org/3.5/library/difflib.html#a-command-line-interface-to-difflib
"""
import argparse
from datetime import datetime, timezone
import difflib
import os
import sys


def file_mtime(path):
    time = datetime.fromtimestamp(os.stat(path).st_mtime, timezone.utc)
    return time.astimezone().isoformat()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        action="store_true",
        default=False,
        help="Produce a context format diff (default)",
    )
    parser.add_argument(
        "-u", action="store_true", default=False, help="Produce a unified format diff"
    )
    parser.add_argument(
        "-m",
        action="store_true",
        default=False,
        help="Produce HTML side by side diff " "(can use -c and -l in conjunction)",
    )
    parser.add_argument(
        "-n", action="store_true", default=False, help="Produce a ndiff format diff"
    )
    parser.add_argument(
        "-l",
        "--lines",
        type=int,
        default=3,
        help="Set number of context lines (default 3)",
    )
    parser.add_argument("fromfile")
    parser.add_argument("to_file")
    options = parser.parse_args()

    n = options.lines
    fromfile = options.fromfile
    to_file = options.to_file

    fromdate = file_mtime(fromfile)
    to_date = file_mtime(to_file)
    with open(fromfile) as ff:
        fromlines = ff.readlines()
    with open(to_file) as tf:
        to_lines = tf.readlines()

    if options.u:
        diff = difflib.unified_diff(
            fromlines, to_lines, fromfile, to_file, fromdate, to_date, n=n
        )
    elif options.n:
        diff = difflib.ndiff(fromlines, to_lines)
    elif options.m:
        diff = difflib.HtmlDiff().make_file(
            fromlines, to_lines, fromfile, to_file, context=options.c, numlines=n
        )
    else:
        diff = difflib.context_diff(
            fromlines, to_lines, fromfile, to_file, fromdate, to_date, n=n
        )

    sys.stdout.writelines(diff)


if __name__ == "__main__":
    main()
