#!/usr/bin/env python

import sys

std_input = []

if sys.stdin.isatty():
    sys.stderr.write('パイプあるいはリダイレクトで標準入力を渡してください。\n')
else:
    for l in sys.stdin:
        std_input.append(str(l))
    print(std_input)

