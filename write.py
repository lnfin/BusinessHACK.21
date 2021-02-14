data = open('data\\gamma_observ_dat.csv', 'r')
data = data.readlines()
lst = []
data = data[1:]
for i in data:
    a = ''
    b = i.split(',')
    a += ';'.join(b[1:4])
    dt = open(f'data\{b[-1][:-1]}', 'r')
    for j in dt:
        lst.append(a + ';' + ';'.join(j.split()) + '\n')
file = open('res.csv', 'w')
file.writelines(lst)
