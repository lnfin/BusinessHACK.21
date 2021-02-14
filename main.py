import os
import matplotlib.pyplot as pl

PATH_TO_FILES = r'data/'


def task_1():
    fields = ['day;HH:MM:SS;gru\n']
    for file in os.listdir(PATH_TO_FILES):
        with open(PATH_TO_FILES + file, 'r', encoding="ISO-8859-1") as f:
            data = [el.split() for el in f.readlines()[2:]]
            res = []
            for fd in data:
                if fd[1][0:2] in ["00", "01"]:
                    res.append([fd[1], fd[2]])
            res = [[el[0], float(el[1])] for el in res]
            res.sort(key=lambda x: x[1], reverse=True)
            for el in res:
                fields.append(f'{file[-6:-4]};{el[0]};{el[1]}\n')

    file = open('task_1.csv', 'w')
    file.writelines(fields)

    print('Successful!')


def task_2():
    fields = ['day;HH:MM:SS;gru\n']
    cur = {}
    others = [{}]

    files = os.listdir(PATH_TO_FILES)
    for file in files:
        with open(PATH_TO_FILES + file, 'r', encoding="ISO-8859-1") as f:
            data = [el.split() for el in f.readlines()[2:]]
            if "10" == file[-6:-4]:
                for fd in data:
                    if fd[1] not in others[-1].keys():
                        cur[fd[1]] = float(fd[2])
            else:
                others.append({})
                for fd in data:
                    if fd[1] not in others[-1].keys():
                        others[-1][fd[1]] = float(fd[2])

    res = [{} for i in range(len(others))]
    time = [{} for i in range(len(others))]
    last = '00:00:00'
    for i, other in enumerate(others):
        key = other.keys()
        for k in key:
            res[i][k] = other[k] - cur[k]
        for k in key:
            time[i][k] = other[k] - other[last]
            last = k
    del res[0]
    del time[0]
    for i in res:
        a = [j for j in range(0, 3600 * 24, 30)]
        b = [i[j] for j in i.keys()]
        pl.plot(a, b)
    pl.xlabel('Time (sec)')
    pl.ylabel('GRU delta')
    pl.savefig('res.png')
    pl.close()
    for i in time:
        a = [j for j in range(0, 3600 * 24, 30)]
        b = [i[j] for j in i.keys()]
        pl.plot(a, b)
    pl.xlabel('Time (sec)')
    pl.ylabel('GRU speed')
    pl.savefig('time.png')
    pl.close()

    print('Successful!')


if __name__ == '__main__':
    task_2()
