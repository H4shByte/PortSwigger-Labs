import requests
import string
import json

BASE_URL = 'https://palceholder.com/api/test/user/'
term = 'ab*'

cookie_value = 'cookie'

cookies = {
    'cookie_name': cookie_value
}

response = requests.get(BASE_URL, cookies=cookies, params={"term": term})
data = response.json()

eids = []

for item in data:
    if 'eid' in item:
        eids.append(item['eid'])

print(eids)
