#!/usr/bin/env python
# -*- coding: utf8 -*-

'''
uniq -c 와 동일한 작업을 수행.
'''

import sys

count     = 0
prev_data = ""
for line in sys.stdin:
	data = line.rstrip()

	# 새로운 데이터가 들어오면,
	# 기존 데이터와 카운터를 출력 후 초기화.
	if prev_data != "" and prev_data != data:
		sys.stdout.write("%s\t%d\n" % (prev_data, count))
		count = 0
		
	count    += 1
	prev_data = data

# 마지막 데이터 처리
sys.stdout.write("%s\t%d\n" % (prev_data, count))
