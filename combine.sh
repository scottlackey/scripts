#!/usr/bin/python
# This gathers all the policies from IAM. Dump output to a file with | jq '.' > filename
# Scott Lackey
import json, boto3
iam = boto3.client('iam')
arns = iam.list_policies()

for x in range(len(arns['Policies'])):
  vers = iam.get_policy_version(
    PolicyArn = arns['Policies'][x]['Arn'],
    VersionId = arns['Policies'][x]['DefaultVersionId']
  )
  print(json.dumps(vers['PolicyVersion']['Document']))
  print(json.dumps(vers['PolicyVersion']['Document']['Statement']))
