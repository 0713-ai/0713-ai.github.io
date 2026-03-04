#Learning Goals Today
- Build interactive programs with user input
- Learn to bypass basic anti-scraping measures
- Fetch data from functional websites (search engine & translation API)
- Understand the difference between GET and POST requests

#Code Example 1: Sogou Search with Headers
```python
import requests

# Get search query from user
content = input("Enter your content: ")
url = f"https://www.sogou.com/web?query={content}"

# Add headers to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
}

resp = requests.get(url, headers=headers)
print(resp.text)
```

#Code Example 2: Baidu Translation API (POST Request)
```python
import requests

url = "https://fanyi.baidu.com/sug"
data = {
    "kw": input("请输入文本: ")  # "Please enter text: "
}

resp = requests.post(url, data=data)
print(resp.json())  # The response is in JSON format
```

#🔍 What I Learned Today
1. The Importance of User-Agent Headers
Without headers, the output contained this obvious error message:
```text
<!DOCTYPE html>
<html lang="en">
<head><title>403 Forbidden</title></head>
<body>
<center><h1>403 Forbidden</h1></center>
<hr><center>nginx/1.8.1</center>
</body>
</html>
```
With headers, I successfully got the actual search results! This is because:

Many websites check the User-Agent to identify bots
By mimicking Chrome/Firefox, I convinced the server I'm a real user

2. How to Find Headers and Request Data
In Chrome (press F12 to open DevTools):
Network tab → Click on any request
Headers section: See all request headers (User-Agent, Cookie, Referer, etc.)
Payload/Form Data section: See POST request data
Preview/Response section: See the server's response

3. GET vs POST Requests
Method	    GET	                          POST
Purpose	    Retrieve data	                Send data to server
Parameters	In URL (?key=value)	          In request body
Visibility	Visible in browser history	  Not visible
Use case	  Search, page navigation	      Login, form submission, API
```python
# GET: parameters in URL
requests.get("https://sogou.com/web?query=python")

# POST: parameters in data
requests.post("https://fanyi.baidu.com/sug", data={"kw": "hello"})
```

4. Interactive Programs
Using input() makes the program interactive:
```python
content = input("Enter your content: ")  # User types something
# Program then uses that input to fetch data
```
#Sample Outputs
For Sogou Search:
```text
Enter your content: python tutorial
[HTML content of search results page appears here...]
```
For Baidu Translation:
```text
请输入文本: hello
{'errno': 0, 'data': [{'k': 'hello', 'v': 'int. 喂；哈罗，你好；<表示问候>；<用于打招呼>'}]}
```

#Important Tips
1. Always add headers - Many websites will block requests without proper User-Agent
2. Check the Network tab in Chrome DevTools (F12) to see exactly what data websites send and receive
3. Choose the right HTTP method:
GET for retrieving information
POST for sending data (like translation queries)
4. Interactive programs are more flexible and useful

#Problems Encountered
Error 403 Forbidden → Solved by adding User-Agent header
Google blocked me again → Switched to Sogou (more beginner-friendly)
Baidu returned weird characters → Used .json() instead of .text
