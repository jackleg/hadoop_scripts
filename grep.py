#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import logging
import argparse

'''
데이터에서 특정 필드에서 주어진 단어가 있는 것만 grep한다.
'''

parser = argparse.ArgumentParser(description='grep data from specific field.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--field",  type=int, default=1, help="field number to grep. start from 1.")
parser.add_argument("--itself", action="store_true", help="print field only.")
parser.add_argument("--term",   action="append", default=[], help="terms to grep.")
parser.add_argument("--min_count", type=int, default=1, help="minimum term count to filter.")
parser.add_argument("--input",  type=argparse.FileType("r"), default=sys.stdin, help="input file.")
parser.add_argument("--output", type=argparse.FileType("w"), default=sys.stdout, help="output file.")
parser.add_argument("--log",    default="info", choices=["info", "debug"], help="logging level.")
args = parser.parse_args()

logging.basicConfig(level=getattr(logging, args.log.upper()))

# grep할 term이 주어지지 않은 경우.
if not args.term:
	logging.info("no terms are given.")
	sys.exit(0)

logging.info("load data from %s, grep terms %s from %d-th field." % (args.input.name, ",".join(args.term), args.field))

FIELD_INDEX=args.field - 1
all_count  = 0
grep_count = 0
for line in args.input:
	line  = line.rstrip("\n")
	data  = line.split("\t")
	field = data[FIELD_INDEX]
	logging.info("field: %s" % field)
	all_count += 1

	if sum([ x.upper() in field.upper() for x in args.term ]) >= args.min_count:
		grep_count += 1

		if args.itself:
			args.output.write("%s\n" % field)
		else:
			args.output.write("%s\n" % line)

logging.info("found %d field. from %d data." % (grep_count, all_count))	
