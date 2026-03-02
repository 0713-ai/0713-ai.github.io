Today's learning goals:
- Learn to use the urllib library to send requests
- Master file read and write operations
- Save the webpage to a local file

Codes:
```python
from urllib.request import urlopen

# Send a request to fetch the webpage
url = "https://www.google.com/"
resp = urlopen(url)

# Save the webpage content to a file
with open("mygoogle.html", mode="w", encoding="utf-8") as f:
    f.write(resp.read().decode("utf-8"))
    
print("Web page saved successfully！Document name：mygoogle.html")
```

What learned today:
1. The difference between urllib and requests
urllib:
- Python comes with it, no need to install
- Slightly cumbersome, requiring decoding
- Has basic functions
requests:
- Needs pip install
- More concise and automated processing
- More powerful (session, proxy, etc.)

2. The 'golden partner' for file manipulation
```python
with open("file name", mode, encoding) as f:
    f.write(content)
```
with: Automatic file management switch, no need to manually f. close()
mode="w": Write mode, if the file exists, it will overwrite
encoding="utf-8": Specify the code to avoid garbled characters

3. Take apart resp.read().decode("utf-8")
resp.read(): Read response content (binary format)
.decode("utf-8"): Decoding binary into strings

Today's harvest:
Having learned to 'harvest' web pages, even though it's only saved locally, I feel like I'm one step closer to a real web scraper!
