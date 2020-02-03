#!/usr/bin/python
# This gathers all the inline policies (and regular policies) from IAM. 
# Dump output to a file for inspection with iam_policies.py [user|role|group|policy] | jq '.' > filename
# Scott Lackey

import json, boto3, getopt, sys
iam = boto3.client('iam')

def getInlineGroupPolicies():
  groups =iam.list_groups(
    MaxItems=1000
  )
  group_list = groups['Groups']
  for group in group_list:
    group_policies = iam.list_group_policies(
      GroupName = group['GroupName'],
      MaxItems = 1000
    )
    for group_policy in group_policies['PolicyNames']:
      group_policy_contents = iam.get_group_policy(
        GroupName = group['GroupName'],
        PolicyName = group_policy
      )
      print(json.dumps(group['GroupName']))
      print(json.dumps(group_policy_contents['PolicyName']))
      print(json.dumps(group_policy_contents['PolicyDocument']['Statement']))

def getInlineUserPolicies():
  users =iam.list_users(
    MaxItems=1000
  )
  user_list = users['Users']
  for user in user_list:
    user_policies = iam.list_user_policies(
      UserName = user['UserName'],
      MaxItems = 1000
    )
    for user_policy in user_policies['PolicyNames']:
      user_policy_contents = iam.get_user_policy(
        UserName = user['UserName'],
        PolicyName = user_policy
      )
      print(json.dumps(user['UserName']))
      print(json.dumps(user_policy_contents['PolicyName']))
      print(json.dumps(user_policy_contents['PolicyDocument']['Statement']))


def getInlineRolePolicies():
  roles =iam.list_roles(
    MaxItems=1000
  )
  role_list = roles['Roles']
  for role in role_list:
    policies = iam.list_role_policies(
      RoleName = role['RoleName'],
      MaxItems = 1000
    )
    for policy in policies['PolicyNames']:
      role_policy = iam.get_role_policy(
        RoleName = role['RoleName'],
        PolicyName = policy
      )
      print(json.dumps(role['RoleName']))
      print(json.dumps(role_policy['PolicyDocument']['Statement']))

# get regular policies
def getPolicies():
  policies = iam.list_policies(
    MaxItems=1000
  )
  for policy in policies['Policies']:
    vers = iam.get_policy_version(
      PolicyArn = policy['Arn'],
      VersionId = policy['DefaultVersionId']
    )
    print(json.dumps(policy['Arn']))
    print(json.dumps(vers['PolicyVersion']['Document']['Statement']))

if sys.argv[1] in ("-h", "--help"):
  print 'Usage: iam_policies.py user|group|role|policy'
if sys.argv[1] == 'user':
  getInlineUserPolicies()
elif sys.argv[1] == 'group':
  getInlineGroupPolicies() 
elif sys.argv[1] == 'role':
  getInlineRolePolicies() 
elif sys.argv[1] == 'policy':
  getPolicies() 
