import datetime as dt
from getthreadreplies import updatereplies
from updatethreads import updatedthreads
from makedatabymin import makedatalist
import os

new_threads = updatedthreads("2023-04-18","2023-05-30")
updatereplies(new_threads)
print("writing to last_time")

last_time = dt.datetime.now().timestamp()
names = os.listdir("data")

for name in names:
    makedatalist(name,new_threads)

with open("last_time","w") as f:
        f.write(str(last_time))
