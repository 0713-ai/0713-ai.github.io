# My Web Scraping Learning Journal 🕷️
## Day 5 - March 9, 2026
### 🎯 Learning Goals Today
- [x] Build a two-level deep crawler (main page → detail pages)
- [x] Handle missing data gracefully with error checking
- [x] Extract movie names and download links from a Chinese movie site
- [x] Learn robust scraping patterns that don't crash on unexpected pages

### 📝 Complete Program: Dytt Movie Scraper with Error Handling

```python
import requests
import re
import time

# Base URL and headers
url = "https://www.dytt8899.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
}


# Step 1: Get main page
resp = requests.get(url, headers=headers)
resp.encoding = "gbk"
print("✅ Main page loaded")

# Step 2: Extract "2026 Must-Watch Movies" section
obj1 = re.compile(r"2026必看热片.*?<ul>(?P<html>.*?)</ul>", re.S)
result1 = obj1.search(resp.text)

if not result1:
    print("❌ Could not find '2026 Must-Watch Movies' section")
    exit()

html = result1.group("html")
print("✅ Found movie list section")

# Step 3: Extract all movie detail page URLs
obj2 = re.compile(r"<li><a href='(?P<href>.*?)' title")
result2 = obj2.finditer(html)

# Step 4: Regular expression for detail page extraction
obj3 = re.compile(r'<div id="Zoom">.*?◎片　　名(?P<movie>.*?)<br />.*?<td style="WORD-WRAP: break-word"'
                  r' bgcolor="#fdfddf"><a href="(?P<download_link>.*?)">', re.S)

# Statistics
success_count = 0
fail_count = 0
movie_data = []

# Step 5: Visit each detail page and extract information
for item in result2:
    child_url = url.rstrip('/') + item.group("href")
    print(f"\n🔗 Visiting: {child_url}")
    
    try:
        # Get detail page
        child_resp = requests.get(child_url, headers=headers, timeout=10)
        child_resp.encoding = "gbk"
        
        # Extract movie info
        result3 = obj3.search(child_resp.text)
        
        # ★★★ CRITICAL: Check if regex matched before accessing groups ★★★
        if result3:
            movie = result3.group("movie")
            download_link = result3.group("download_link")
            
            print(f"  ✅ Success: {movie}")
            print(f"     Download: {download_link}")
            
            movie_data.append({
                "name": movie,
                "download": download_link,
                "url": child_url
            })
            success_count += 1
        else:
            print(f"  ❌ Failed: Could not extract movie info")
            # Optional: Save failed page for debugging
            with open(f"debug_failed_{success_count+1}.html", "w", encoding="gbk") as f:
                f.write(child_resp.text[:2000])  # Save first 2000 chars
            fail_count += 1
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Request failed: {e}")
        fail_count += 1
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        fail_count += 1
    
    # Be polite: wait between requests
    time.sleep(3)

# Final summary
print("\n" + "="*50)
print(f"📊 SCRAPING COMPLETE")
print("="*50)
print(f"✅ Successfully extracted: {success_count} movies")
print(f"❌ Failed: {fail_count} pages")
print(f"📈 Success rate: {success_count/(success_count+fail_count)*100:.1f}%")

# Optional: Save results to file
if movie_data:
    with open("dytt_movies.txt", "w", encoding="utf-8") as f:
        for movie in movie_data:
            f.write(f"{movie['name']}\n{movie['download']}\n\n")
    print(f"💾 Results saved to dytt_movies.txt")
```

📊 Sample Output
```text
✅ Main page loaded
✅ Found movie list section

🔗 Visiting: https://www.dytt8899.com/html/xxx/1.html
  ✅ Success: 流浪地球3
     Download: magnet:?xt=urn:btih:xxx...

🔗 Visiting: https://www.dytt8899.com/html/xxx/2.html
  ✅ Success: 封神第二部
     Download: magnet:?xt=urn:btih:yyy...

🔗 Visiting: https://www.dytt8899.com/html/xxx/3.html
  ❌ Failed: Could not extract movie info

...

📊 SCRAPING COMPLETE
✅ Successfully extracted: 12 movies
❌ Failed: 3 pages
```

💡 Key Lesson: The Importance of Error Handling
The Problem I Encountered:
My original code crashed with this error:
```text
AttributeError: 'NoneType' object has no attribute 'group'
```
What caused it:
```python
# Original code (problematic)
result3 = obj3.search(child_resp.text)
movie = result3.group("movie")  # ❌ Crash if result3 is None
download_link = result3.group("download_link")  # ❌ Same here
```

The Fix:
```python
# Fixed code (robust)
result3 = obj3.search(child_resp.text)
if result3:  # ★★★ Always check before accessing ★★★
    movie = result3.group("movie")
    download_link = result3.group("download_link")
    # Process successfully extracted data
else:
    # Handle the failure gracefully
    print("Could not extract movie info")
```

🔍 Why Some Pages Fail
After debugging, I discovered several reasons why some pages couldn't be parsed:
Reason	                      Example	                                              Solution
Different page template	      Some movies use "◎片名" instead of "◎片　　名"	        Make regex more flexible
Missing download section	    Page exists but no download link yet	                Skip and continue
Encoding issues	              Some pages use different character sets	              Try multiple encodings
Temporary server errors	      502 Bad Gateway	                                      Retry with backoff

📈 What I Learned About Robust Scraping
1. Always Validate Regex Results
```python
# Good practice
result = pattern.search(html)
if result:
    data = result.group("field")
else:
    # Handle missing data
    log_error(url, pattern)
```

2. Use Try-Except Blocks
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raise exception for 4xx/5xx status codes
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
    continue  # Skip to next URL
```

3. Add Progress Tracking
success_count = 0
fail_count = 0

# Later...
print(f"Progress: {success_count} success, {fail_count} failed")
```

4. Save Debug Information
```python
with open(f"debug_{url_hash}.html", "w") as f:
    f.write(page_source)  # Save for later analysis
```

💭 Reflection
"Today I learned that web scraping isn't just about writing regex patterns—it's about building robust systems that can handle the unexpected. The internet is messy, and websites are inconsistent. A good scraper doesn't crash when it finds something unexpected; it logs the issue, skips gracefully, and keeps going. This is the difference between a script and a reliable tool."

🎯 Keys
Never trust website structure - It can change at any time
Always check regex results - None.group() is a common beginner mistake
Count successes and failures - Know your scraper's effectiveness
Log debug information - Save failed pages for later analysis
Be polite - Use time.sleep() to avoid overloading servers
