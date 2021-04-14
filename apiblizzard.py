import requests, json
myToken = "USBg074vEawfz5XaHYIreeSvvcAStzKTkK"
my_headers = {'Authorization' : 'access_token myToken'}
response = requests.get('http://httpbin.org/headers', headers=my_headers)

payload = {'access_token': myToken, 'locale': 'en_US'}
r = requests.get('https://us.api.blizzard.com/hearthstone/cards', headers = my_headers, params = payload, verify=True)

print(r.url)
print(r.status_code)
r.json()
