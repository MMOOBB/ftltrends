#!/bin/python

import requests
import json
from time import sleep

page = 1
start = "2023-05-19"
end = "2023-05-22"

while True:
    link=f'https://archive.4plebs.org/_/api/chan/search/?boards=tv&start={start}&end={end}&subject=ftl%7Cfish&type=op&page={page}'
    r = requests.get(link, headers={'User-Agent': 'Foo bar'})
    scode = r.status_code
    data = r.text
    jdata = json.loads(r.text)
    if scode == 429:
        wait_time = int(jdata["error"].split(" ")[5])
        print(jdata["error"])
        sleep(wait_time)
        continue
    if jdata == {"error":"No results found."}:
        print("no more pages")
        break
    print(jdata["0"]["posts"][0]["num"])
    for i in jdata["0"]["posts"]:
        #print(i["num"])
        num=i["num"]
        replies=i["nreplies"]
        ips=i["unique_ips"]
        date=i["fourchan_date"]
        with open("nnewfishtankthreads.csv", "a") as f:
            f.write(f"{num},{replies},{ips},{date}\n")
    page+=1
    print(f"page:{page}")
