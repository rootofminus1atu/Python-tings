import requests


def error_thing():
    print(f"Status code: {response.status_code}")
    try:
        print(f"{response.json()['status_verbose']}")
    except:
        pass


barcode = "8076800195057"
url = f"https://off:off@ie.openfoodfacts.net/api/v2/product/{barcode}"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    try:
        packaging_info = data['product'].get('packaging')
        packagings_info = data['product'].get('packagings')
        print(data)
        print("hi")
        print(packaging_info)
        print("hi")
        print(packagings_info)
    except:
        error_thing()
else:
    error_thing()