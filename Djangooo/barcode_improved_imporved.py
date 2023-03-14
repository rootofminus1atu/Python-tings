import requests


def error_thing(response):
    print(f"Status code: {response.status_code}")
    try:
        print(f"{response.json()['status_verbose']}")
    except:
        pass

def print_barcode_info(barcode):

    url = f"https://off:off@ie.openfoodfacts.net/api/v2/product/{barcode}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        try:
            packaging_info = data['product'].get('packaging')
            packagings_info = data['product'].get('packagings')
            print(packaging_info)
            print(packagings_info)
        except:
            error_thing(response)
    else:
        error_thing(response)
