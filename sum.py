#!/usr/bin/env python
# -*- coding: utf8 -*-

'''
정렬된 (key, score) 데이터가 stdin으로 입력되면,
(key, sum(score))를 출력한다.
'''

import sys

score_sum = 0
prev_key = ""

for line in sys.stdin:
    key, score_str = line.rstrip().split("\t")

    # 새로운 데이터가 들어오면,
    # 기존 데이터와 카운터를 출력 후 초기화.
    if prev_key != "" and prev_key != key:
        sys.stdout.write("%s\t%d\n" % (prev_key, score_sum))
        score_sum = 0
    
    score_sum += int(score_str)
    prev_key = key

# 마지막 데이터 처리
sys.stdout.write("%s\t%d\n" % (prev_key, score_sum))
