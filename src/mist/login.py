import requests

def login(host, username, password, two_factor_code):
    url = f"https://{host}/api/v1/login"
    data = {
        "email": username,
        "password": password
    }
    if two_factor_code:
        data["two_factor"] = two_factor_code
    res = requests.post(url, json=data)
    if not res.status_code == 200:
        return res.json(), res.status_code
    else:
        return _self(host, res.cookies)

def _self(host, cookies):
    url = f"https://{host}/api/v1/self"
    res = requests.get(url, cookies=cookies.get_dict())

    return res.json(), res.status_code, cookies



