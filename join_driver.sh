#!/bin/bash

if [ $# -lt 3 ]; then
	echo "usage: $0 <join_dir1> <join_dir2> <output_dir> [how]"
    echo "    how: joined, left, right, all"
	exit 1
fi

JOIN_DIR1=$1
JOIN_DIR2=$2
OUTPUT_DIR=$3
HOW=$4

JAR_DIR="/data1/cdh/opt/cloudera/parcels/CDH-5.4.3-1.cdh5.4.3.p0.6/jars"
STREAMING_JAR="hadoop-streaming-2.6.0-cdh5.4.3.jar"

LIB_JARS=/data1/users/jay.han/opt/hadoop_lib/quality.jar

# move given directory to tmporary name.
function move_to_tmp {
	ORG_DIR=$1
	TMP_DIR=$ORG_DIR.$RANDOM

	hadoop dfs -mv ${ORG_DIR} ${TMP_DIR} && echo "[`date`] move [$ORG_DIR] to [$TMP_DIR]"
	return $?
}

# check output directory
hadoop dfs -test -e ${OUTPUT_DIR} && (move_to_tmp ${OUTPUT_DIR} || exit 1)

hadoop jar ${JAR_DIR}/${STREAMING_JAR} \
	-files ./join_mapper.py,./join_reducer.py \
    -libjars ${LIB_JARS} \
	-D mapreduce.job.name="[jay] join ${JOIN_DIR1} and ${JOIN_DIR2}" \
    -D mapreduce.partition.keypartitioner.options="-k1,1" \
    -D stream.num.map.output.key.fields=2 \
    -D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
    -D mapreduce.partition.keycomparator.options="-k1 -k2n" \
	-input ${JOIN_DIR1} \
	-input ${JOIN_DIR2} \
	-output ${OUTPUT_DIR} \
	-mapper "join_mapper.py ${JOIN_DIR1} ${JOIN_DIR2}" \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
	-reducer "./join_reducer.py ${HOW}" \
    -outputformat com.kakao.quality.web.KeyMultipleOutputFormat
