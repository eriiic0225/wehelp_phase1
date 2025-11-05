import ssl 
ssl._create_default_https_context = ssl._create_unverified_context

import urllib.request as req

#! 全域儲存區
host = "https://www.ptt.cc/"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0"
all_topics = []
all_likes = []
all_times = []

#! 抓時間的小次函式
def getTime(urls):
    page_times = [] #用來儲存各頁所有的時間
    for article_url in urls:
        header_request = req.Request(article_url, headers={
        "User-Agent": UA
        })
        with req.urlopen(header_request) as resp:
            raw_data = resp.read().decode("utf-8")
        
        import bs4
        soup = bs4.BeautifulSoup(raw_data, "html.parser")
        time_box = soup.select_one('span:-soup-contains("時間") + span') #選擇「內容含有時間兩個字的<span>」的相鄰<span>(前面是bs4專屬語法，後面是css兄弟選擇器)
        #這邊不用 string="時間"，因為這樣時間前後有空格的話就沒辦法命中
        time = time_box.get_text(strip=True) if time_box else "" #time = 如果上面的選擇器有抓到東西，就把內含問字去掉頭尾空白，沒有抓到就當作是空字串
        page_times.append(time) #推到函式內的儲存區
    return page_times #return給主函式的變數儲存，之後再extended到全域儲存區


#! 主程式
def getData(url):
    request = req.Request(url, headers={
        "User-Agent": UA
    })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    import bs4
    root = bs4.BeautifulSoup(data, "html.parser") #整個頁面的原始HTML資訊

    #抓此頁全部標題
    titles = root.find_all("div", class_="title") #尋找所有 class="title" 的 div 標籤(回傳list)
    for title in titles:
        if title.a != None: #如果標題包含a標籤(沒有被刪除)
            all_topics.append(title.a.string)

    #抓此頁全部讚數
    hot = root.select("div.nrec") #找所有class=nrec的div
    for box in hot:
        like = box.select_one("span.hl") #抓裡面的第一個span
        all_likes.append(like.get_text(strip=True) if like else "0")

    #先在這邊抓全部的文章連結
    article_links = []
    links = root.select("div.title > a")
    for a in links:
        article_links.append(host+a["href"])
    #在這裡用次函式的迴圈抓各文章時間
    this_page_time = getTime(article_links)
    all_times.extend(this_page_time)

    # 抓取下一頁的連結
    nextLink = root.find("a", string="‹ 上頁") #找到內文是 ‹ 上頁 的 a 標籤
    return (nextLink["href"]) #url連結本身（nextLink的 href 屬性）#要記得接上前面的host: "https://www.ptt.cc/"

pageURL = "https://www.ptt.cc/bbs/Steam/index.html"

#!連續爬蟲迴圈
count = 0
while count < 3:
    pageURL = host+getData(pageURL)
    count += 1

#! 把全域儲存區的東西抓下來合併
combine = []
for i in range(len(all_topics)):
    combine.append((all_topics[i], all_likes[i], all_times[i]))

#! 寫進 csv
import csv
with open("articles.csv", mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    for information in combine:
        writer.writerow(information)