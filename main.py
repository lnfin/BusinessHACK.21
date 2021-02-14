import os

PATH_TO_FILES = r'data/'

fields = ['day;HH:MM:SS;gru\n']
for file in os.listdir(PATH_TO_FILES):
    with open(PATH_TO_FILES + file, 'r', encoding="ISO-8859-1") as f:
        data = [el.split() for el in f.readlines()[2:]]
        res = []
        for fd in data:
            if fd[1][0:2] in ["00","01","02"]:
                res.append([fd[1], fd[2]])
        res = [[el[0], float(el[1])] for el in res]
        res.sort(key=lambda x: x[1], reverse=True)
        print(res)
        for el in res:
            fields.append(f'{file[-6:-4]};{el[0]};{el[1]}\n')

file = open('task_1.csv', 'w')
file.writelines(fields)

print('Successful!')
