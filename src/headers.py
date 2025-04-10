import json
import requests


def get_headers(headers_path):
    filepath = headers_path
    with open(filepath) as f:
        headers = json.load(f)
    return headers


def create_new_headers(session, headers, headers_path):
    temp_headers = headers["cookie"].split(";")
    new_cookie = ""
    for each in range(len(temp_headers)):
        if "_tsn_session" in temp_headers[each]:
            temp_headers[each] = temp_headers[each].split("=")[0] + "=" + session

        new_cookie += temp_headers[each] + ";"

    new_cookie = new_cookie[:-1] + ""
    headers["cookie"] = new_cookie

    new_headers = json.dumps(headers)
    filepath = headers_path
    with open(filepath, "w") as outfile:
        outfile.write(new_headers)
