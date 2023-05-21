import os
import json

threads = os.listdir("threads")
threads.sort()


for thread in threads:
    print(thread)
    with open(f"threads/{thread}", "r") as raw:
        jdata = json.load(raw)

    remove = ["fourchan_date","thread_num","num"]
    for rem in remove:
        jdata[str(thread)]["op"].pop(rem)
    mremove = ["media_hash","media_id","media_orig"]
    for mrem in mremove:
        jdata[str(thread)]["op"]["media"].pop(mrem)

    try:
        for postnum in jdata[str(thread)]["posts"]:
            post = jdata[str(thread)]["posts"][postnum]
            for rem in remove:
                post.pop(rem)
            try:
                if post["media"] != None:
                    for mrem in mremove:
                        post["media"].pop(mrem)
            except KeyError:
                print("No media")
    except KeyError:
        print("No replies")
    json_obj = json.dumps(jdata, sort_keys=True, indent=4)
    with open(f"threads2/{thread}","w") as file:
        file.write(json_obj)
