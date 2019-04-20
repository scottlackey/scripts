#!/bin/bash
source replay_secrets

fulldate=$(date +"%Y%m%d")
date=$(expr $fulldate - 1)
today=$(date +"%d")
yesterday=$(expr $today - 1)

mkdir $date
cd $date
aws s3 cp s3://prod-redshift.audit.clicktripz.com/AWSLogs/048300154415/redshift/us-west-2/2019/04/$yesterday/ . --recursive --exclude "*" --include "048300154415_redshift_us-west-2_prod-redshift_useractivitylog_2019-04-$yesterday*"
gunzip *.gz
for i in $(ls 0483*); do ../ParseUserActivityLog.py -c 'aws_iam_role=arn:aws:iam::048300154415:role/RedshiftProdCopy' $i; done
for i in $(ls 0483*); do rm -rf $i; done
ls *.sql > files
../order_list.sh files > ordered
sed -i 's/UNLOAD.*$//g' *

../SimpleReplay.sh ordered
