#def ana(str1, str2):
#  list1 = list(str1)
#  list2 = list(str2)
#  list1.sort()
#  list2.sort()
#  return (list1 == list2)

#print(ana('anagram', 'nagaram'))
#print(ana('cat', 'rat'))

def count(str):
  d = {}
  for i in str:
    if i in d:
      d[i] += 1
    else:
      d[i] = 1
      print ("i is", i)
  return(d)

def cmp(d1, d2):
  for key in d1:
    if key not in d2:
      return False
    if d1[key] != d2[key] or len(d1) != len(d2):
      return False
  return True
   
d1 = count("testa")
print ("count of d1", d1)
d2 = count("setta")
print ("count of d2", d2)
print(cmp(d1, d2))
