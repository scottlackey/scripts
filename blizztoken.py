import requests, json
from operator import itemgetter
token_url = 'https://us.battle.net/oauth/token'
test_api_url = "https://us.api.blizzard.com/hearthstone/cards"
data = {'grant_type': 'client_credentials'}

access_token_response = requests.post(token_url, data=data, verify=True, allow_redirects=False, auth=(client_id, client_secret))

#print access_token_response.headers
#print access_token_response.text

tokens = json.loads(access_token_response.text)

#print "access token: " + tokens['access_token']

api_call_headers = {'Authorization': 'Bearer ' + tokens['access_token']}
payload = {'locale': 'en_US', 'class': 'warlock', 'rarity': 'legendary'}
r = requests.get(test_api_url, headers=api_call_headers, params=payload)

#print r.status_code
#print r.url
rdata = json.loads(r.text)

i = 0
cardlist = []
for card in rdata["cards"]:
  if i < 10:
    if card["manaCost"] >=7:
      cardlist.append({'id': card["id"], 'Name':card["name"], 'Set':card["cardSetId"], 'Type': card["cardTypeId"], 'Class': card["classId"], 'Rarity': card["rarityId"], 'Image': card["image"] })
      i += 1
sortedlist = sorted(cardlist, key=itemgetter('id'), reverse=True)
print(sortedlist)

print(json.dumps(sortedlist, indent = 4, sort_keys=True))
