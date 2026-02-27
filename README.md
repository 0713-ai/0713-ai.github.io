Today's learning goals:
- Understand the basic concepts of HTTP requests
- Learn to install and use the requests library
- Successfully retrieved webpage content

Codes:
```python
import requests

# Send a GET request
url = "https://www.google.com"
resp = requests.get(url)

#Set encoding to avoid garbled characters
resp.encoding = "utf-8"

#Print webpage content
print(resp.text)

What I learned:
1. Basic usage of the requests library
- requests.get(url) can send GET requests
- The response object returned by the server contains all the information of the webpage
2. Importance of coding
- Specify the encoding with resp. encoding="utf-8" or it will return messy code
3. View response content
- Resp.text returns the HTML source code of the webpage, which is the "raw material" that scrapers can see
