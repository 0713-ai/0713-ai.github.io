import requests
import re
import time
f = open("top250.csv",mode="w",encoding="utf-8")

for i in range(10):
    print(f"开始提取第{i+1}页")
    url = f"https://movie.douban.com/top250?start={i*25}&filter="
    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    pageSource = resp.text

    obj = re.compile(r'<div class="item">.*?<span class="title">(?P<name>.*?)</sp'
                     r'an>.*?<p>.*?导演: (?P<dire>.*?)&nbsp;.*?<br>'
                     r'(?P<year>.*?)&nbsp;.*?<span class="rating_num" property="v:average">'
                     r'(?P<score>.*?)</span>.*?<span>(?P<num>.*?)人评价</span>',re.S)

    result = obj.finditer(pageSource)
    for item in result:
        name = item.group("name")
        dire = item.group("dire")
        year = item.group("year").strip()
        score = item.group("score")
        num = item.group("num")
        f.write(f'{name},{dire},{year},{score},{num}\n')
    resp.close()
    print(f"第{i+1}页提取完毕。")
    time.sleep(5)

f.close()
print("全部提取完毕。")
