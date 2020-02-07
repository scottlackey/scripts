#!/usr/local/bin/python3
#livongo coding example Scott Lackey scottlackey@gmail.com
import os, operator, sys
from datetime import datetime, timedelta
path = sys.argv[1] 

def readlogs():
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
  return d

def pageviews(d):
  matched = {}
  uniques = 0
  top_users = 5
  for dic in d:
    if dic['uid'] in matched:
      matched[dic['uid']] += 1
    else:
      matched[dic['uid']] = 1
      uniques += 1
  pv = sorted(matched.items(), key=operator.itemgetter(1))
  i = 0
  j = 1
  top = []
  while i < top_users:
    top.append(' '.join(map(str, pv[len(pv) - j])))
    j += 1
    i += 1
  return uniques, top

def sessions(d, user):
  sess = timedelta(seconds=0)
  pt = 0
  session_counter = 0
  session_list = []
  for dic in d:
    if (dic['uid'] == user):
      rawdate = dic['date']
      if (pt == 0):
        pt = datetime.strptime(rawdate,"%d/%b/%Y:%H:%M:%S")
        ct = datetime.strptime(rawdate,"%d/%b/%Y:%H:%M:%S")
      else:
        pt = ct
        ct = datetime.strptime(rawdate,"%d/%b/%Y:%H:%M:%S")
        dt = ct - pt
        if (dt.total_seconds() <= 600):
          sess += dt
        else:
          total_sess = sess.total_seconds() / 60.0
          session_counter += 1
#          print("session in minutes", round(total_sess,2)) 
          session_list.append(round(total_sess,2))
          sess += dt
  #final session, or one that never had a 10 minute delta
  total_sess = sess.total_seconds() / 60.0
  session_list.append(round(total_sess,2))
  session_counter += 1
  session_list.sort()
  return session_counter, session_list

#main function block
d = readlogs()
uniques, top = pageviews(d)
print("Total unique users:",  uniques )
print("Top users:")
print( "id       #pages #sess longest shortest")
for each in top:
  each = each.split()
  session_count, session_list = sessions(d, each[0])
  print(each[0], each[1], '  ', session_count, '  ', session_list[len(session_list) -1], ' ', session_list[0])
