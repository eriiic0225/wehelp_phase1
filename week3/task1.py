import ssl 
ssl._create_default_https_context = ssl._create_unverified_context

import urllib.request as request
import json
hotels_ch = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
hotels_eng = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"

with request.urlopen(hotels_ch) as response:
    json_cn = json.load(response)

with request.urlopen(hotels_eng) as response_en:
    json_eng = json.load(response_en)

data_cn = json_cn["list"]
data_eng = json_eng["list"]

#print(data_cn, data_eng)

cn_list = {hotel["_id"]:hotel for hotel in data_cn}
eng_list = {eng_hotel["_id"]:eng_hotel for eng_hotel in data_eng}
print(cn_list)
sorted_ids = sorted(cn_list.keys())

combine = []

for hid in sorted_ids:
    cn = cn_list[hid]
    eng = eng_list[hid]
    chinese_name = cn["旅宿名稱"]
    english_name = eng["hotel name"]
    chinese_addr = cn["地址"]
    english_addr = eng["address"]
    phone = (cn["電話或手機號碼"] or eng["tel"])
    room = int(cn["房間數"])
    combine.append((chinese_name, english_name, chinese_addr, english_addr, phone, room))

#print(combine)


import csv
with open("hotels.csv", mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    for information in combine:
        writer.writerow(information)

total_count ={
    "大安區":[0,0], "中正區":[0,0], "大同區":[0,0], "內湖區":[0,0], 
    "萬華區":[0,0], "松山區":[0,0], "北投區":[0,0], "南港區":[0,0],
    "信義區":[0,0], "中山區":[0,0], "文山區":[0,0], "士林區":[0,0],}
# for hotel in combine:
#     if "大安區" in hotel[2]:
#         total_count["大安區"][0] += 1
#         total_count["大安區"][1] += hotel[-1]
#     elif "中正區" in hotel[2]:
#         total_count["中正區"][0] += 1
#         total_count["中正區"][1] += hotel[-1]
#     elif "大同區" in hotel[2]:
#         total_count["大同區"][0] += 1
#         total_count["大同區"][1] += hotel[-1]
#     elif "內湖區" in hotel[2]:
#         total_count["內湖區"][0] += 1
#         total_count["內湖區"][1] += hotel[-1]
#     elif "萬華區" in hotel[2]:
#         total_count["萬華區"][0] += 1
#         total_count["萬華區"][1] += hotel[-1]
#     elif "松山區"in hotel[2]:
#         total_count["松山區"][0] += 1
#         total_count["松山區"][1] += hotel[-1]
#     elif "北投區" in hotel[2]:
#         total_count["北投區"][0] += 1
#         total_count["北投區"][1] += hotel[-1]
#     elif "南港區" in hotel[2]:
#         total_count["南港區"][0] += 1
#         total_count["南港區"][1] += hotel[-1]
#     elif "信義區" in hotel[2]:
#         total_count["信義區"][0] += 1
#         total_count["信義區"][1] += hotel[-1]
#     elif "中山區" in hotel[2]:
#         total_count["中山區"][0] += 1
#         total_count["中山區"][1] += hotel[-1]
#     elif "文山區" in hotel[2]:
#         total_count["文山區"][0] += 1
#         total_count["文山區"][1] += hotel[-1]
#     elif "士林區" in hotel[2]:
#         total_count["士林區"][0] += 1
#         total_count["士林區"][1] += hotel[-1]
districts = ["大安區","中正區","大同區","內湖區","萬華區","松山區",
             "北投區","南港區","信義區","中山區","文山區","士林區"]

for name, eng_name, addr, eng_addr, tel, rooms in combine:
    for dist in districts:
        if dist in addr:
            total_count[dist][0] += 1
            total_count[dist][1] += rooms

result = [(key, value[0], value[1])for key, value in total_count.items()]




with open("districts.csv", mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    for district in result:
        writer.writerow(district)