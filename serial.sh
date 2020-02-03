#!/bin/bash

# exit if script is already running
RUNNING=`ps -ef --no-headers | grep $0 | wc -l`
SECONDS=0;

# gt 3 because of this process, the ps process and the grep
if [ ${RUNNING} -gt 3 ]; then
  echo " ____________________________________"
  echo" exiting, cannot run simultaneous processes"
  exit 1
fi

post_to_slack () {
  # format message as a code block ```${msg}```
  SLACK_MESSAGE="\`\`\`$1\`\`\`"
  SLACK_URL=https://hooks.slack.com/services/your-service-identifier-part-here
  #curl -X POST --data "payload={\"text\": \"${SLACK_MESSAGE}\"}" ${SLACK_URL}
  echo ${SLACK_MESSAGE}
}

#it would be better to get dynamic serverlist if we were pulling from AWS 
#serverlist=$(aws ec2 --region $REGION describe-instances --filters "Name=tag:aws:autoscaling:groupName,Values='SOMEAUTOSCALINGGROUP'" "Name=instance-state-name,Values=running" | jq '.Reservations[].Instances[].PrivateIpAddress' | tr -d '"' | tr "\n" " ")

serverlist=(10.12.101.247 10.12.102.181)
FAILURE=0
COMMAND='sudo ls -l /root/ansible.log'

for each in ${serverlist[*]} ; do
  if [[ $SECONDS -lt 60 && $FAILURE -eq 0 ]]; then 
    STARTTIME=$(date +%s)
    ssh -o "StrictHostKeyChecking=no" -i ~/.ssh/ctkey2017 ec2-user@$each $COMMAND
    sleep 2
    ENDTIME=$(date +%s)
    RUNTIME=$(($ENDTIME - $STARTTIME))
    #echo "check if something went wrong then FAILURE=1"
    echo "total running time for $0 is $SECONDS. This node took $RUNTIME seconds to complete"
    logger "completed $each at $(date) in $RUNTIME seconds"
    post_to_slack "completed $each at $(date) in $RUNTIME seconds"
    # datadog update through local client
    #echo -n "db_update_completion:$RUNTIME|g|#shell" >/dev/udp/localhost/8125
  fi
done;
