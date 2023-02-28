import requests

# ?fields=packaging
# ?fields=packagings

barcode = "7622300735838"
url = f"https://off:off@ie.openfoodfacts.net/api/v2/product/{barcode}?fields=packagings"
response = requests.get(url)

if response.status_code == 200:
    product_info = response.json()
    print(product_info)
    print(product_info['product']['packagings'])
else:
    print(f"Error: {response.status_code}")
