from pylab import *
import matplotlib.pyplot as plt
import csv 

x = []
y = []
z = []
with open('record.csv','r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        x.append(row[0])
        y.append(row[1])
        z.append(row[2])


# fig = plt.figure

plt.figure(num=None, figsize=(16, 4), dpi=80, facecolor='w', edgecolor='k')

plt.subplot(131)
plt.title('x')
plt.plot(x)

plt.subplot(132)
plt.title('y')
plt.plot(y)

plt.subplot(133)
plt.title('z')
plt.plot(z)

plt.show()
