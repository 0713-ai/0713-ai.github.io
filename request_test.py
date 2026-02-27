import requests
url = "https://www.google.com"
resp = requests.get(url)
resp.encoding = "utf-8"
print(resp.text)
