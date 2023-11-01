import requests

def get_pwned(account):

    url = "https://haveibeenpwned.com/api/v3/breachedaccount/" + account
    hibp_api_key = '<key>'
    payload={}
    headers = {
        'hibp-api-key': str(hibp_api_key),
        'format': 'application/json',
        'timeout': '2.5',
        'HIBP': str(hibp_api_key),
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)