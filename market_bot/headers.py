import json
import requests


def get_headers():
    filename = "headers.json"
    with open(filename) as f:
        headers = json.load(f)
    return headers


def create_new_headers(session, headers):
    tempHeaders = headers["cookie"].split(";")
    new_cookie = ""
    for each in range(len(tempHeaders)):
        if "_tsn_session" in tempHeaders[each]:
            tempHeaders[each] = tempHeaders[each].split("=")[0] + "=" + session

        new_cookie += tempHeaders[each] + ";"

    new_cookie = new_cookie[:-1] + ""
    headers["cookie"] = new_cookie

    newHeaders = json.dumps(headers)
    filename = "headers.json"
    with open(filename, "w") as outfile:
        outfile.write(newHeaders)
