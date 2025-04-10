import json
import requests


def get_headers():
    filename = "headers.json"
    with open(filename) as f:
        headers = json.load(f)
    return headers


def create_new_headers(session, headers):
    temp_headers = headers["cookie"].split(";")
    new_cookie = ""
    for each in range(len(temp_headers)):
        if "_tsn_session" in temp_headers[each]:
            temp_headers[each] = temp_headers[each].split("=")[0] + "=" + session

        new_cookie += temp_headers[each] + ";"

    new_cookie = new_cookie[:-1] + ""
    headers["cookie"] = new_cookie

    new_headers = json.dumps(headers)
    filename = "headers.json"
    with open(filename, "w") as outfile:
        outfile.write(new_headers)
