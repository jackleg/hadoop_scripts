#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

if len(sys.argv) >= 2 and sys.argv[1] == "--help":
    sys.stderr.write("usage: %s <how>\n" % sys.argv[0])
    sys.stderr.write("    how: joined (default), left, right, all")
    sys.stderr.write("         joined: joined data only.")
    sys.stderr.write("         left: left outer data. (joined and left_only)")
    sys.stderr.write("         right: right outer data. (joined and right_only)")
    sys.stderr.write("         all: outer data. (joined and left/right_only)")
    sys.exit(1)

# CONSTANTS
JOINED = 0
LEFT = 1
RIGHT = 2
ALL = 3
HOW_DICT = {"joined": JOINED, "left": LEFT, "right": RIGHT, "all": ALL}

if len(sys.argv) == 1:
    how = JOINED
else:
    how = HOW_DICT[sys.argv[1]]

# prev_key와 data는 position 값이 1인 경우에만 저장된다.
prev1_key = ""
prev1_data_list = []
# join된 데이터가 있는 경우
has_joined = False

COUNTER_FORMAT="reporter:counter:JOIN,%s,%d\n"

for line in sys.stdin:
    key, position, data = line.rstrip().split("\t", 2)

    if prev1_key == key:
        if position == "1":
            prev1_data_list.append(data)
        else: # position == "2"
            has_joined = True
            for prev_data in prev1_data_list:
                sys.stdout.write("joined\t%s\t%s\t%s\n" % (key, prev_data, data))
                sys.stderr.write(COUNTER_FORMAT % ("joined", 1))
    else:
        if has_joined == False: # 앞의 데이터는 left data만 있는 경우
            sys.stderr.write(COUNTER_FORMAT % ("left_only", len(prev1_data_list)))
            if how == LEFT or how == ALL:
                for prev_data in prev1_data_list:
                    sys.stdout.write("left_only\t%s\t%s\n" % (prev1_key, prev_data))

        # 출력한 이전 데이터에 대해서 초기화
        del prev1_data_list[:]
        has_joined = False

        if position == "1":
            prev1_key = key
            prev1_data_list.append(data)
        else: # position == "2", 이번 데이터가 right only data만 있는 경우
            sys.stderr.write(COUNTER_FORMAT % ("right_only", 1))
            if how == RIGHT or how == ALL:
                sys.stdout.write("right_only\t%s\t%s\n" % (key, data))

# process last line
# 마지막 데이터가 left_only인 경우만 이 케이스가 된다.
# (2인 경우는 joined이거나 right_only이거나, 모두 for 안에서 처리된다.)
if has_joined == False:
    sys.stderr.write(COUNTER_FORMAT % ("left_only", len(prev1_data_list)))
    if how == LEFT or how == ALL:
        for prev_data in prev1_data_list:
            sys.stdout.write("left_only\t%s\t%s\n" % (prev1_key, prev_data))
