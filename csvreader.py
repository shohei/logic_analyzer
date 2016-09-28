from pylab import *
import matplotlib.pyplot as plt
import csv 

points = []
with open('record.csv','r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        points.append(row)
plt.plot(points)
plt.show()
