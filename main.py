import matplotlib.pyplot as plt

data = open('res.csv', 'r')
data = data.readlines()
prev = 0
x = []
y = []
for i in data:
    if i[:3] != prev:
        y.append([])
        x.append([])
    a = i.split(';')
    y[-1].append(float(a[-1]))
    x[-1].append(float(a[-2]))
    prev = i[:3]
for i in range(25):
    for j in range(4):
        plt.plot(x[j + i], y[j + i])
    plt.savefig(f'{i + 1}.png')
    plt.close()
