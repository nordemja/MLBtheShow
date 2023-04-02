import json
import requests

def get_headers():
    filename = 'headers.json'
    with open(filename) as f:
        headers = json.load(f)
    return headers

headers = get_headers()
s = requests.Session()

def create_new_headers(playerLink, headers):
    results = requests.get(playerLink,headers=headers)
    newCookie = results.headers['Set-Cookie'].split(';')[0]
    tempHeaders = headers['cookie'].split(';')
    tempHeaders[1] = newCookie
    headers['cookie'] = tempHeaders[0]+';'+tempHeaders[1]+';'+tempHeaders[2]

    newHeaders = json.dumps(headers)
    filename = 'C:\\Users\\justi\\OneDrive\\Documents\\Python Programming\\MLBtheShow\\headers.json'
    with open(filename, 'w') as outfile:
        outfile.write(newHeaders)