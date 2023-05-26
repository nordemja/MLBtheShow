import json

def get_headers():
    filename = 'headers.json'
    with open(filename) as f:
        headers = json.load(f)
    return headers

headers = get_headers()

def create_new_headers(session, headers):
    tempHeaders = headers['cookie'].split(';')
    for each in range(len(tempHeaders)):
        if "_tsn_session" in tempHeaders[each]:
            tempHeaders[each] = tempHeaders[each].split("=")[0] + "=" + session
            

    headers['cookie'] = tempHeaders

    newHeaders = json.dumps(headers)
    filename = 'headers.json'
    with open(filename, 'w') as outfile:
        outfile.write(newHeaders)

create_new_headers("JUSTIN", headers)