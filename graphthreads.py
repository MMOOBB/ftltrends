import pandas as pd
import matplotlib.pyplot as plt
import csv

x = []
y = []

with open('fishtankthreadssorted.csv','r') as data:
    plots = csv.reader(data, delimiter = ',')

    for row in plots:
        if int(row[1]) < 50:
            continue
        x.append(int(row[0]))
        y.append(int(row[1]))

plt.plot(x, y, color = 'g')
plt.xlabel('Thread')
plt.ylabel('Replies')
plt.title('Replies per time(threads)')
plt.show()
