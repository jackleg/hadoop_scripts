#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import logging
from optparse import OptionParser

'''
데이터에서 특정 필드에서 주어진 단어가 있는 것만 grep한다.
'''

parser = OptionParser()
parser.add_option("--field",  type=int, default=1, help="field number to grep. start from 1.")
parser.add_option("--itself", action="store_true", help="print field only.")
parser.add_option("--term",   action="append", default=[], help="terms to grep.")
parser.add_option("--min_count", type=int, default=1, help="minimum term count to filter.")
parser.add_option("--input",  help="input file.")
parser.add_option("--output", help="output file.")
parser.add_option("--log",    default="info", choices=["info", "debug"], help="logging level.")
options, args = parser.parse_args()

options.input  = sys.stdin if not options.input else open(options.input)
options.output = sys.stdout if not options.output else open(options.output, "w")

logging.basicConfig(level=getattr(logging, options.log.upper()))

# grep할 term이 주어지지 않은 경우.
if not options.term:
	logging.info("no terms are given.")
	sys.exit(0)

logging.info("load data from %s, grep terms %s from %d-th field." % (options.input.name, ",".join(options.term), options.field))

FIELD_INDEX=options.field - 1
all_count  = 0
grep_count = 0
for line in options.input:
	line  = line.rstrip("\n")
	data  = line.split("\t")
	field = data[FIELD_INDEX]
	logging.info("field: %s" % field)
	all_count += 1

	if sum([ x.upper() in field.upper() for x in options.term ]) >= options.min_count:
		grep_count += 1

		if options.itself:
			options.output.write("%s\n" % field)
		else:
			options.output.write("%s\n" % line)

logging.info("found %d field. from %d data." % (grep_count, all_count))	
