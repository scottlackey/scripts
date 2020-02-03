#!/usr/bin/python
import time, datetime, sys, os, paramiko, syslog
from slackclient import SlackClient
from datadog import initialize, api
#from datadog import api

#datadog auth
options = {'api_key': '<YOUR_API_KEY>',
           'app_key': '<YOUR_APP_KEY>'}
initialize(**options)

hostnames = ['192.168.17.212']
username = 'ec2-user'
key = '/home/scott/.ssh/ctkey2017'
start_time = round(time.time())
command = "sudo ls /root/ansible.log"
slacktoken = "slacktoken"
slackchannel = "ops"

def datadog_message(title, message):
  api.Event.create(title=title, text=message, tags="db_updater")

def slack_message(message, channel):
  token = slacktoken
  sc = SlackClient(token)
  sc.api_call('chat.postMessage', channel=channel, 
    text=message, username='bot',
    icon_emoji=':robot_face:')

def check_err(ssh_stderr,hostname):
    outlines=ssh_stderr.readlines()
    resp=''.join(outlines)
    message = "error %s while processinig on host %s" % (resp,hostname)
    return message

def cycle(hostname):
  host_start = round(time.time())
  start = str(datetime.datetime.now()).split('.')[0]
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh.connect(hostname, username=username, key_filename=key)
  ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
  time.sleep(2)
  if ssh_stdout.channel.recv_exit_status() >0:
    message = check_err(ssh_stderr,hostname)
  else:
    host_complete = round(time.time())
    complete = str(datetime.datetime.now()).split('.')[0]
    host_total = round(host_complete - host_start)
    message = "DB update completed on %s in %s starting %s finishing %s" % (hostname,host_total,start,complete)
#  slack_message(message, slackchannel)   
  syslog.syslog(message)
#  datadog_message("db_updates", message)
  outlines=ssh_stdout.readlines()
  resp=''.join(outlines)
  print(resp)
  print message
  ssh.close()

#main
for hostname in hostnames:
  elapsed_time = round(time.time()) - start_time
  if elapsed_time < 60:
    cycle(hostname)
  else:
    print "timout exceeded while processing %s" % (hostname)
    sys.exit(1)

