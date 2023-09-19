#!/usr/bin/env python3

import sys
import argparse
import srt
import fileinput
from datetime import timedelta

CHAIN_GAP_THERESHOLD = timedelta(milliseconds=500)
CHAIN_GAP = timedelta(milliseconds=67)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

parser = argparse.ArgumentParser()
parser.add_argument('--fix', action='store_true', help='print the fixed file to stdout')
parser.add_argument('file', help='file to lint')
args = parser.parse_args()

with open(args.file, 'r') as f:
    src = f.read()

srtstr = srt.parse(src)

subs = []
last_sub = None

failure = False

for sub in srtstr:
    if last_sub is not None:
        diff = sub.start - last_sub.end

        if (sub.start < last_sub.end):
            Failure = True
            eprint(f'Invalid sub #{sub.index}: overlapping')
            last_sub.end = sub.start - CHAIN_GAP
        elif (diff < CHAIN_GAP_THERESHOLD):
            if (diff != CHAIN_GAP):
                Failure = True
                eprint(f'Invalid sub #{sub.index}: unchained ({int(diff.microseconds / 1000)}ms gap)')
                last_sub.end = sub.start - CHAIN_GAP

    last_sub = sub
    subs.append(sub)


if args.fix:
    print(srt.compose(subs))
elif failure:
    sys.exit(1)

sys.exit(0)
