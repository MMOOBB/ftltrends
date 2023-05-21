from datetime import datetime
import csv
import re

with open("fishtankthreadssorted.csv","r") as data:
    lines = csv.reader(data)

    with open("fishtankthreadstimefix.csv","w") as f:
        for row in lines:
            ldate=re.split("/|:|\(|\)",row[3])
            ldate.pop(3)
            ldate=[int(i) for i in ldate]
            ndate=datetime(2000+ldate[2],ldate[0],ldate[1],ldate[3],ldate[4])
            row[3] = str(ndate)
            f.write(','.join(row))
            f.write("\n")
