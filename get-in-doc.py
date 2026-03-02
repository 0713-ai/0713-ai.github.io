from urllib.request import urlopen
url = "https://www.google.com/"
resp = urlopen(url)
with open("mygoogle.html",mode="w",encoding="utf-8") as f:
    f.write(resp.read().decode("utf-8"))
