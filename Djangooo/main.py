import pyqrcode

# creating a qr code
link = "www.wikipedia.com"
url = pyqrcode.create(link)
url.png('wikipediaqrcode.png', scale=6)

print("hi")
