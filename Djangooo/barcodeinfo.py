import requests
import json

barcode = "5099195002161"
url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}?fields=packaging.json"
response = requests.get(url)





# printing info
if response.status_code == 200:
    product_info = response.json()
    print(product_info)
    print("\n")
    print(product_info["product"]["ecoscore_data"]["adjustments"]["packaging"])
else:
    print(f"Error: {response.status_code}")

# making a file with info
if response.status_code == 200:
    product_info = response.json()
    with open(f"{barcode}.json", "w") as file:
        json.dump(product_info, file, indent=4)
else:
    print(f"Error: {response.status_code}")