import requests
from requests.exceptions import HTTPError

from .logger import Console
console = Console("req")

def generate_headers(apitoken=None, cookies=None):
    '''
    Generate Mist Request Headers from the apitoken or the session cookies
    params:
        apitoken    str     optional
        cookies     obj     optional    cookies from the login request
    return:
        headers     obj
    '''
    headers = {
        'Content-Type': 'application/json'
    }
    if apitoken:
        headers["Authorization"] = f"Token {apitoken}"
    elif cookies:
        for entry in cookies.split(';'):
            cookie = entry.split("=")
            if cookie[0].startswith("csrftoken"):
                headers["X-CSRFToken"] = cookie[1]
    return headers

def _response( resp, uri="", multi_pages_result=None):
    if resp.status_code == 200 or resp.status_code == 201 :
        if multi_pages_result is None:
            result = resp.json()
        else: 
            result = multi_pages_result
        error = ""
        console.debug(f"Response Status Code: {resp.status_code}")
    else:
        result = ""
        error = resp.json()
        console.info(f"Response Status Code: {resp.status_code}")
        console.debug(f"Response: {error}")
    return {"result": result, "headers":resp.headers, "status_code": resp.status_code, "error": error, "uri":uri}

def get(url, headers={}, query={}):
    """GET HTTP Request
    Params: uri, HTTP query
    Return: HTTP response"""
    try:
        html_query = "?"
        if not query == {}:
            for query_param in query:
                html_query += f"{query_param}={query[query_param]}&"
        console.debug(f"Request > GET {url}")
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
    except HTTPError as http_err:
        console.error(f'HTTP error occurred: {http_err}')  # Python 3.6
        console.error(f'HTTP error description: {resp.json()}')
    except Exception as err:
        console.error(f'Other error occurred: {err}')  # Python 3.6
    else:             
        return _response(resp, url)

def post(url, headers={}, body=None):
    """POST HTTP Request
    Params: uri, HTTP body
    Return: HTTP response"""
    try: 
        if not "Content-Type" in headers:
            headers['Content-Type'] = "application/json"
        console.debug(f"Request > POST {url}")
        console.debug(f"Request body: \r\n{body}")
        if type(body) == str:
            resp = requests.post(url, data=body, headers=headers)
        elif type(body) == dict:
            resp = requests.post(url, json=body, headers=headers)
        else: 
            resp = requests.post(url, json=body, headers=headers)
        resp.raise_for_status()
    except HTTPError as http_err:
        console.error(f'HTTP error occurred: {http_err}')  # Python 3.6
        console.error(f'HTTP error description: {resp.json()}')
    except Exception as err:
        console.error(f'Other error occurred: {err}')  # Python 3.6
    else: 
        return _response(resp, url)

def put(url, headers={}, body={}):
    """PUT HTTP Request
    Params: uri, HTTP body
    Return: HTTP response"""
    try:
        console.debug(f"Request > PUT {url}")
        console.debug(f"Request body: \r\n{body}")
        if type(body) == str:
            resp = requests.put(url, headers=headers, data=body)
        elif type(body) == dict:
            resp = requests.put(url, headers=headers, json=body)
        else: 
            resp = requests.put(url, json=body)
        resp.raise_for_status()
    except HTTPError as http_err:
        console.error(f'HTTP error occurred: {http_err}')  # Python 3.6
        console.error(f'HTTP error description: {resp.json()}')
    except Exception as err:
        console.error(f'Other error occurred: {err}')  # Python 3.6
    else: 
        return _response(resp, url)

def delete(url, headers={}):
    """DELETE HTTP Request
    Params: uri
    Return: HTTP response"""
    try: 
        console.debug(f"Request > DELETE {url}")
        resp = requests.delete(url, headers=headers)
        resp.raise_for_status()
    except HTTPError as http_err:
        console.error(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        console.error(f'Other error occurred: {err}')  # Python 3.6
    else: 
        return _response(resp, url)


def post_file(url, headers={}, files=None):
    """POST HTTP Request
    Params: uri, HTTP body
    Return: HTTP response"""
    try:                 
        console.debug(f"Request > POST {url}")
        resp = requests.post(url, headers=headers, files=files)
        resp.raise_for_status()
    except HTTPError as http_err:
        console.error(f'HTTP error occurred: {http_err}')  # Python 3.6
        console.error(f'HTTP error description: {resp.json()}')
        return resp
    except Exception as err:
        console.error(f'Other error occurred: {err}')  # Python 3.6
    else: 
        return _response(resp, url)
