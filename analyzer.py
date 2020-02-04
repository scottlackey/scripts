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
  for dic in d:
    if (dic['uid'] == '43a81873'):
      rawdate = dic['date']
      if (pt == 0):
        pt = datetime.strptime(rawdate,"%d/%b/%Y:%H:%M:%S")
        ct = datetime.strptime(rawdate,"%d/%b/%Y:%H:%M:%S")
      else:
        pt = ct
        ct = datetime.strptime(rawdate,"%d/%b/%Y:%H:%M:%S")
        dt = ct - pt
#        print("current time", ct)
#        print("minus")
#        print("previous time", pt)
#        print("equals")
#        print("dt total_Seconds", dt.total_seconds())
        if (dt.total_seconds() <= 600):
          sess += dt
        else:
          sess += dt
          print ("############# Session ###############")
          print("session in seconds", sess.total_seconds())
          total_sess = sess.total_seconds() / 60.0
          session_counter += 1
          print("session in minutes", round(total_sess,2)) 
  print ("sessions", session_counter + 1)

uniques, top = pageviews(d)
print("Total unique users:",  uniques )
print("Top users:")
print( "UserID  Pageviews")
for each in top:
  print(each)
#for each in top:
#  each = each.split()
#  print(each[0])
#  sessions(d, each[0])
sessions(d, 'user')


