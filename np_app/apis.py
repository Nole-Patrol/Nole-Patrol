import requests

account = 'cgrim.wa@gmail.com'
def get_pwned(account):

    url = "https://haveibeenpwned.com/api/v3/breachedaccount/" + account
    hibp_api_key = '71113c7ccb05453fbeb9d79b1121b2ef'
    payload={}
    headers = {
        'hibp-api-key': str(hibp_api_key),
        'format': 'application/json',
        'timeout': '2.5',
        'HIBP': str(hibp_api_key),
    }
    print(url)
    response = requests.request("GET", url, headers=headers, data=payload)

    #print(response.text)

    response_string = response.text
    print(response_string)
    for i in response_string:
        response_string = response_string.replace(
            '"', "").replace(
                '[', "").replace(']', "").replace(
                    '{', "").replace(
                        '}', "").replace(
                            'Name:', account+":NULL:")
    print(response_string)

if __name__ == '__main__':
    get_pwned(account)