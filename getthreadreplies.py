import requests
import csv
import json
from time import sleep
import datetime as dt

def updatereplies(threads):
    for thread in threads:
        print(thread)
        link = f"https://archive.4plebs.org/_/api/chan/thread/?board=tv&num={thread}"
        while True:
            try:
                page = requests.get(link, headers={'User-Agent': 'Foo bar'})
                jdata = json.loads(page.text)
                print(jdata[str(thread)]["op"]["title"])
            except:
                sleep(1)
                continue
            break
        remove = ["board","capcode","comment_processed","comment_sanitized","deleted","doc_id","email","email_processed","exif","extra_data","formatted","locked","name_processed","nimages","nreplies","poster_country","poster_country_name","poster_country_name_processed","poster_hash","poster_hash_processed","since4pass","sticky","subnum","timestamp_expired","title_processed","trip_processed","troll_country_code","troll_country_name","op", "fourchan_date","thread_num","num"]
        for rem in remove:
            jdata[str(thread)]["op"].pop(rem)
        mremove = ["banned","exif","media_filename_processed","media_h","media_size","media_status","media_w","ocr","ocr_processed","preview_h","preview_op","preview_orig","preview_reply","preview_w","remote_media_link","spoiler","thumb_link","total", "media_hash","media_id","media_orig"]
        for mrem in mremove:
            jdata[str(thread)]["op"]["media"].pop(mrem)
        num_media = 0
        num_replies = 0

        try:
            num_replies = len(jdata[str(thread)]["posts"])
            for postnum in jdata[str(thread)]["posts"]:
                post = jdata[str(thread)]["posts"][postnum]
                for rem in remove:
                    post.pop(rem)
                post.pop("unique_ips")
                post.pop("title")
                if post["media"] != None:
                    num_media += 1
                    for mrem in mremove:
                        post["media"].pop(mrem)
                else:
                    post.pop("media")
        except:
            print("No replies")
        print(num_replies)
        print(num_media)
        jdata[str(thread)]["op"]["nreplies"]=num_replies
        jdata[str(thread)]["op"]["nimages"]=num_media
        json_obj = json.dumps(jdata, sort_keys=True, indent=4)
        with open(f"threads/{thread}","w") as file:
            file.write(json_obj)
        sleep(1)

if __name__ == "__main__":
    with open("nnewfishtankthreads.csv",'r') as data:
        ldata = csv.reader(data)
        threads_list=[]
        for i in ldata:
            print(i)
            threads_list.append(i[0])
        threads_list.sort()
        updatereplies(threads_list)
