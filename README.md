# My Web Scraping Learning Journal 🕷️
🎯 Learning Goals Today
- Extract structured data from a real website (Douban Top 250)
- Master regular expressions for pattern matching
- Implement automatic pagination by finding URL patterns
- Save scraped data to CSV format for analysis

📝 Complete Program: Douban Top 250 Movie Scraper
```python
import requests
import re
import time

# Open CSV file for writing
f = open("top250.csv", mode="w", encoding="utf-8")

# Loop through all 10 pages (25 movies per page)
for i in range(10):
    print(f"Starting page {i+1}")
    
    # URL pattern: start parameter changes by 25 each page
    url = f"https://movie.douban.com/top250?start={i*25}&filter="
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
    }
    
    # Send request and get page source
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    pageSource = resp.text
    
    # Regular expression to extract movie information
    obj = re.compile(r'<div class="item">.*?<span class="title">(?P<name>.*?)</sp'
                     r'an>.*?<p>.*?导演: (?P<dire>.*?)&nbsp;.*?<br>'
                     r'(?P<year>.*?)&nbsp;.*?<span class="rating_num" property="v:average">'
                     r'(?P<score>.*?)</span>.*?<span>(?P<num>.*?)人评价</span>', re.S)
    
    # Find all matches and extract data
    result = obj.finditer(pageSource)
    for item in result:
        name = item.group("name")
        dire = item.group("dire")
        year = item.group("year").strip()
        score = item.group("score")
        num = item.group("num")
        
        # Write to CSV file
        f.write(f'{name},{dire},{year},{score},{num}\n')
    
    resp.close()
    print(f"Page {i+1} completed.")
    
    # Be polite: wait 5 seconds before next request
    time.sleep(5)

f.close()
print("All pages completed! Data saved to top250.csv")
```

📊 Sample Output (top250.csv)
```text
肖申克的救赎  弗兰克·德拉邦特 Frank Darabont  1994  9.7  3266036
霸王别姬  陈凯歌 Kaige Chen  1993  9.6  2409336
泰坦尼克号  詹姆斯·卡梅隆 James Cameron  1997  9.5  2483296
... (250 movies in total)
```

💡 Key Concepts Mastered Today
1. Regular Expressions (Regex) - The Superpower
The regex pattern I created extracts 5 different fields in one pass:
```python
r'<div class="item">.*?<span class="title">(?P<name>.*?)</sp'
r'an>.*?<p>.*?导演: (?P<dire>.*?)&nbsp;.*?<br>'
r'(?P<year>.*?)&nbsp;.*?<span class="rating_num" property="v:average">'
r'(?P<score>.*?)</span>.*?<span>(?P<num>.*?)人评价</span>'
```

What each part does:
(?P<name>.*?) - Named group "name" captures movie title
.*? - Lazy matching (match as little as possible)
re.S flag - Makes . match newlines as well
&nbsp; - HTML space character, used as a marker

Why regex is powerful:
Extracts all fields in one pass through the HTML
More precise than string methods like find() or split()
Once written, it works for all 250 movies automatically

2. URL Pattern Discovery
```python
# Page 1: start=0
# Page 2: start=25
# Page 3: start=50
# Pattern: start = (page_number - 1) * 25

url = f"https://movie.douban.com/top250?start={i*25}&filter="
```
The insight: Websites often use predictable URL patterns for pagination. By analyzing just 2-3 pages, I discovered:
First page: start=0
Second page: start=25
Therefore: start increases by 25 each page

3. Polite Scraping Practices
```python
time.sleep(5)  # Wait 5 seconds between requests
```
Why this matters:
Respects the website's server resources
Avoids being blocked (too many requests in short time = suspicious)
Good "web citizen" behavior

4. CSV Format for Data Storage
```text
name,director,year,score,ratings_count
肖申克的救赎,弗兰克·德拉邦特 Frank Darabont,1994,9.7,3266036
```
Advantages:
Universally readable (Excel, Numbers, Google Sheets)
Easy to process with pandas for analysis
Lightweight and human-readable

🔍 How I Built This

Step 1: Analyze the Website
Opened Chrome DevTools (F12)
Navigated to Network tab
Observed URL patterns across pages
Found the HTML structure containing movie info

Step 2: Find the Pattern
```html
<!-- Each movie is inside a div with class "item" -->
<div class="item">
    <span class="title">肖申克的救赎</span>
    <p>导演: 弗兰克·达拉邦特&nbsp;...</p>
    <span class="rating_num">9.7</span>
    <span>2987100人评价</span>
</div>
```

Step 3: Build Regex Piece by Piece
Started simple and gradually added fields:
```python
# Step 1: Match just the title
r'<span class="title">(?P<name>.*?)</span>'

# Step 2: Add director
r'导演: (?P<dire>.*?)&nbsp;'

# Step 3: Add year, score, and ratings count...
```

💭 Reflection: The Power of Automation
The real value of this program:
Manual Approach	                       Automated Scraper
Copy-paste 250 movies manually	       Runs in 60 seconds
Hours of boring work	                 Minutes of setup, seconds of execution
One-time use only	                     Reusable anytime
Error-prone	                           Consistent accuracy
Can't update easily	                   Run again for fresh data

📈 What This Data Enables
With this CSV file, I can now:
Analyze trends: Which years had the most top movies?
Compare directors: Who appears most frequently?
Track changes: Run again next month to see if rankings changed
Build projects: Create a movie recommendation system
Practice data visualization: Make charts of score distributions

🐛 Challenges Overcome
Regex debugging - Had to test piece by piece, using print statements to verify each field
HTML inconsistencies - Some movies had extra spaces or different formatting
Rate limiting - Added time.sleep(5) after getting temporarily blocked
Encoding issues - Set resp.encoding = "utf-8" to handle Chinese characters
