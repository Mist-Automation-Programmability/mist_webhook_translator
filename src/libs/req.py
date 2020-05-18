import requests
from requests.exceptions import HTTPError

import json

try:
    from config import log_level
except:
    log_level = 6
finally:
    from .debug import Console
    console = Console(log_level)


def _response( resp, uri="", multi_pages_result=None):
    if resp.status_code == 200 or resp.status_code == 201 :
        if multi_pages_result == None:
            result = resp.json()
        else: 
            result = multi_pages_result
        error = ""
        console.debug("Response Status Code: %s" % resp.status_code)
    else:
        result = ""
        error = resp.json()
        console.info("Response Status Code: %s" % resp.status_code)
        console.debug("Response: %s" % error)
    return {"result": result, "headers":resp.headers, "status_code": resp.status_code, "error": error, "uri":uri}

def get(url, headers={}, query={}):
    """GET HTTP Request
    Params: uri, HTTP query
    Return: HTTP response"""
    try:
        html_query = "?"
        if not query == {}:
            for query_param in query:
                html_query += "%s=%s&" %(query_param, query[query_param])
        console.debug("Request > GET %s" % url)
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
        console.debug("Request > POST %s" % url)
        console.debug("Request body: \r\n%s" % body)
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
        console.debug("Request > PUT %s" % url)
        console.debug("Request body: \r\n%s" % body)
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
        console.debug("Request > DELETE %s" % url)
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
        console.info("Request > POST %s" % url)
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
