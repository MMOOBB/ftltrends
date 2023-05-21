#!/bin/python

import requests
import json
from time import sleep
import os
from getthreadreplies import updatereplies

#start = "2023-04-18"
#end = "2023-05-30"
def updatedthreads(start, end):
    page = 1
    rollover = 0
    new_threads=[]
    curr_threads = os.listdir("threads")
    curr_threads.sort()
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
            if not i["num"] in curr_threads:
                new_threads.append(i["num"])
            else:
                rollover += 1
                if rollover > 5:
                    return new_threads
        page+=1
    return new_threads

def updatethreadreplies():
    updatereplies(updatedthreads("2023-04-18","2023-05-30"))

#if __name__ == "__main__":
#    print(updatedthreads(start,end))
