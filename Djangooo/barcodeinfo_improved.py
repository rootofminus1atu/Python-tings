import requests

# ?fields=packagings,packaging

barcode = "8076800195057"
url = f"https://off:off@ie.openfoodfacts.net/api/v2/product/{barcode}?fields=packagings,packaging"
response = requests.get(url)


def error_thing():
    print(f"Status code: {response.status_code}")
    try:
        print(f"{response.json()['status_verbose']}")
    except:
        pass


if response.status_code == 200:
    data = response.json()
    print(f"Prod info {data}")
    try:
        print(data['product']['packagings'])
    except:
        error_thing()
else:
    error_thing()
