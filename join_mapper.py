#!/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import urlparse

if len(sys.argv) < 3:
	sys.stderr.write("usage: %s <input_dir_1> <input_dir_2>\n" % sys.argv[0])
	sys.stderr.write("    size of input_dir_1 would be less than input_dir_2's.\n")
	sys.stderr.write("\n")
	sys.exit(1)

MAP_INPUT_FILE = urlparse.urlparse(os.getenv("map_input_file")).path

INPUT_DIR_1 = sys.argv[1]
INPUT_DIR_2 = sys.argv[2]

if MAP_INPUT_FILE.startswith(INPUT_DIR_1):
    input_key = "1"
elif MAP_INPUT_FILE.startswith(INPUT_DIR_2):
    input_key = "2"
else:
    raise ValueError("%s does not match neither %s nor %s." % (MAP_INPUT_FILE, INPUT_DIR_1, INPUT_DIR_2))

for line in sys.stdin:
    tokens = line.rstrip().split("\t")
    tokens.insert(1, input_key)
    sys.stdout.write("%s\n" % "\t".join(tokens))
