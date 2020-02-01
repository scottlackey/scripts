#!/usr/local/bin/python3
#livongo coding example
import os, operator
from datetime import datetime, timedelta
path = "logs/"

d = []
c = 0
keys = ['uid','ip', 'date', 'timezone', 'op', 'uri', 'pro', 'statuscode']
for filename in os.listdir(path):
  with open(os.path.join(path, filename),'r') as f:
    for line in f:
      #split ws
      l = line.split()
      l.remove('-')
      l.remove('-')
      uri_string = l[4].split('/')
      if (len(uri_string) >= 4):
      #if no uid, don't add it to the dict.
        uid = uri_string[3]
        l.insert(0,uid) 
        d.append(dict(zip(keys, l)))

def pageviews(d):
  matched = {}
  uniques = 0
  for dic in d:
    if dic['uid'] in matched:
      matched[dic['uid']] += 1
    else:
      matched[dic['uid']] = 1
      uniques += 1
  print("Total unique users:",  uniques )
  print("Top users:")
  print( "UserID  Pageviews")

  pv = sorted(matched.items(), key=operator.itemgetter(1))
  i = 0
  j = 1
  while i < 5:
    print(' '.join(map(str, pv[len(pv) - j]))) 
    j += 1
    i += 1

def sessions(d):
  sess = timedelta(seconds=0)
  pt = 0
  session_counter = 0
  for dic in d:
    if (dic['uid'] == '489f3e87'):
      rawdate = dic['date']
      if (pt == 0):
        pt = datetime.strptime(rawdate,"%d/%b/%Y:%H:%M:%S")
        ct = datetime.strptime(rawdate,"%d/%b/%Y:%H:%M:%S")
      else:
        pt = ct
        ct = datetime.strptime(rawdate,"%d/%b/%Y:%H:%M:%S")
        dt = ct - pt
#        print(dt.total_seconds())
        if (dt.total_seconds() <= 600):
          sess += dt
        else:
          print ("############# Session ###############")
          print(sess.total_seconds())
          sess = timedelta(seconds=0)
          session_counter += 1
  print(sess / timedelta(minutes=1))
  print ("sessions", session_counter + 1)

pageviews(d)
sessions(d)

