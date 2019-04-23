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
#quotes around usernames
sed -i 's/clicktripz-read-only/\"clicktripz-read-only\"/g' *
sed -i 's/domo-unload/\"domo-unload\"/g' *
sed -i 's/lambda-loader/\"lambda-loader\"/g' *
#create file with sql filenames and then order it
ls *.sql > files
../order_list.sh files > ordered

#../SimpleReplay.sh ordered
