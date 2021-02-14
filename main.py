import os
import csv
import pandas as pd

PATH_TO_FILES = r'data/'

fields = ['day;HH:MM:SS;gru\n']
for file in os.listdir(PATH_TO_FILES):
    with open(PATH_TO_FILES + file, 'r', encoding="ISO-8859-1") as f:
        data = [el.split() for el in f.readlines()[2:]]
        for fd in data:
            fields.append(f'{file[-6:-4]};{fd[1]};{fd[2]}\n')

file = open('task_1.csv', 'w')
file.writelines(fields)

print('Successful!')
