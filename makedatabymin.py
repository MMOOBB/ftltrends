import json
import datetime as dt
import os
import numpy as np
import pandas as pd
import heapq


def remdown(num, mod): #return the number minus the remanider of what's set
    rem = num%mod
    return num - rem

def makedata(name):
    timep = 1 #in minutes

    filename = f"{name}"
    if filename == "_":
        filename="_"
    path = f"data/{filename}"

    start=dt.datetime(2023,4,18,0,0,0)
    end=dt.datetime(2023,5,30,0,0,0)

    timelist = np.arange(start.timestamp(), end.timestamp(), 60)

    threads = os.listdir("threads")
    threads.sort()

    data = {int(i):0 for i in timelist}

    for thread in threads:
        with open(f"threads/{thread}", "r") as raw:
            jraw = json.load(raw)
            try:
                posts = jraw[thread]["posts"]
            except KeyError:
                continue
            for tpost in posts:
                post = jraw[thread]["posts"][tpost]
                timeslot = remdown(post["timestamp"],60*timep)
                #if not timeslot in data[name]:
                #    data[timeslot] = 0
                if name == "_":
                    data[timeslot] += 1
                    continue
                if not post["comment"] == None:
                    if name.casefold() in post["comment"].casefold():
                        data[timeslot] += 1

    val=[]
    for i,v in sorted(data.items()):
        val.append(v)


    pdata={
        'time':pd.date_range(start=start , end=end , freq='1min',inclusive='left'),
        name:val
            }


    df = pd.DataFrame(pdata)
    df.set_index('time', inplace=True)

    df.to_csv(path)

    #with open(path,"w") as newdata:
    #    newdata.write(json.dumps(data, sort_keys=True, indent=4))


def popwords(top, start, end, ignorelist):

    filename = "allwords"
    if filename == "_":
        filename="_"
    path = f"{filename}"

    start = start.timestamp()
    end = end.timestamp()

    threads = os.listdir("threads")
    threads.sort()

    data = {}

    for thread in threads:
        with open(f"threads/{thread}", "r") as raw:
            jraw = json.load(raw)
            try:
                posts = jraw[thread]["posts"]
            except KeyError:
                continue
            for tpost in posts:
                post = jraw[thread]["posts"][tpost]
                if not (start < post["timestamp"] < end):
                    continue
                if not post["comment"] == None:
                    wordlist = post["comment"].split()
                    wordlist = [i.strip(".,?!()\"\';:#*") for i in wordlist]
                    for word in wordlist:
                        word = word.casefold()
                        if word in ignorelist:
                            continue
                        if not word in data:
                            data[word] = 0
                        data[word] += 1
    highest =  heapq.nlargest(top, data.items(), key=lambda item: item[1])


    return highest

def popmedia(top, start, end):

    filename = "allmedia"
    if filename == "_":
        filename="_"
    path = f"{filename}"

    start = start.timestamp()
    end = end.timestamp()

    threads = os.listdir("threads")
    threads.sort()

    data = {}

    for thread in threads:
        with open(f"threads/{thread}", "r") as raw:
            jraw = json.load(raw)
            try:
                posts = jraw[thread]["posts"]
            except KeyError:
                continue
            for tpost in posts:
                post = jraw[thread]["posts"][tpost]
                if not (start < post["timestamp"] < end):
                    continue
                try:
                    post["media"]
                except KeyError:
                    continue
                if not post["media"] == None:
                    safe_hash = post["media"]["safe_media_hash"]
                    if not safe_hash in data:
                        data[safe_hash] = {}
                        data[safe_hash]["filename"] = post["media"]["media_filename"]
                        data[safe_hash]["link"] = post["media"]["media_link"]
                        data[safe_hash]["count"] = 0
                    data[safe_hash]["count"] += 1
    highest =  sorted(data.items(), key=lambda x: x[1]["count"], reverse=True)[:top]
    return highest




if __name__ == "__main__":
    #makedata("_")
    popmedia(10 ,dt.datetime(2023,4,18,0,0,0),dt.datetime(2023,5,30,0,0,0))
    #popwords(20 ,dt.datetime(2023,4,18,0,0,0),dt.datetime(2023,5,30,0,0,0),['the', 'to', 'a', 'and', 'is', 'i', 'of', 'you', 'in', 'it', 'this', 'that', 'for', 'he', 'her', 'on', 'she', 'was', 'with', 'they', 'just', 'be', 'are', 'like', 'so', 'not', 'have', 'but', 'what', 'all', 'his', 'him', 'about','if', 'out', 'do', "it's", 'at', 'has', 'get', 'no', 'as', 'or', 'how', 'will', 'now', 'them', 'my', 'would', 'when', 'can', 'me', 'because', 'from', "he's", 'even', 'who', 'an', 'did', 'think', 'why', 'your', 'going', 'more', "don't", 'by', 'being', "she's", 'only', "i'm", 'we', 'know', 'been', 'there', 'really', 'some', 'too', 'got', 'go', 'their', 'make', 'its', 'than', 'want', 'into', 'had', 'still', 'after', 'then', 'said', 'see', 'these', 'much', "can't", 'does', "you're", 'here', 'way', 'got', 'go', 'their', 'make', 'its', 'than', 'want', 'into', 'had', 'still', 'after', 'then', 'said', 'see', 'these', 'much', "can't", 'does', "you're", 'here', 'way', 'should', 'someone', "that's", 'any', "doesn't", 'were', 'getting', 'other', 'everyone', 'something', 'gonna', 'thing', 'doing', 'guy', "they're", 'again', 'where', "didn't"])


def makedatalist(name, threads):
    timep = 1 #in minutes
    threads.sort()
    with open("last_time", "r") as lol:
        last_time = int(lol.readline().split(".")[0])


    filename = f"{name}"
    if filename == "_":
        filename="_"
    path = f"data/{filename}"

    start=dt.datetime(2023,4,18,0,0,0)
    end=dt.datetime(2023,5,30,0,0,0)

    #timelist = np.arange(start.timestamp(), end.timestamp(), 60)


    #data = {int(i):0 for i in timelist}

    with open(f"data/{name}", "r") as fdata:
        fdata.readline()
        data = {}
        for line in fdata:
            line = line.split(",")
            data[int(dt.datetime.fromisoformat(line[0]).timestamp())]=int(line[1])

    for thread in threads:
        with open(f"threads/{thread}", "r") as raw:
            jraw = json.load(raw)
            try:
                posts = jraw[thread]["posts"]
            except KeyError:
                continue
            for tpost in posts:
                post = jraw[thread]["posts"][tpost]
                timeslot = remdown(post["timestamp"],60*timep)
                #if not timeslot in data[name]:
                #    data[timeslot] = 0
                if last_time > int(post["timestamp"]):
                    continue
                if name == "_":
                    data[timeslot] += 1
                    continue
                if not post["comment"] == None:
                    if name.casefold() in post["comment"].casefold():
                        data[timeslot] += 1

    val=[]
    for i,v in sorted(data.items()):
        val.append(v)


    pdata={
        'time':pd.date_range(start=start , end=end , freq='1min',inclusive='left'),
        name:val
            }


    df = pd.DataFrame(pdata)
    df.set_index('time', inplace=True)

    df.to_csv(path)
