import requests
import csv
import os
from math import floor

STEP = 1


class DataBase:
    def __init__(self, path, dm=';'):
        self.table = []
        with open(path, encoding='utf-8') as csv_file:
            lines = csv.reader(csv_file, delimiter=dm)
            columns = next(lines)
            for line in lines:
                dct = {}
                for i in range(len(columns)):
                    dct[columns[i]] = line[i]
                self.table.append(dct)


class DataBaseNPP(DataBase):
    def __init__(self):
        super().__init__(os.path.join('archive', 'data', 'csv', 'denormalized', 'nuclear_power_plants.csv'))

    def get_points(self):
        points = []
        for line in self.table:
            lat, lon = line['Latitude'], line['Longitude']
            if lat and lon:
                points.append((lat, lon))
        return points

    def get_grid(self):
        npps = self.get_points()
        npp_table = dict()
        for n in npps:
            n = tuple(map(lambda x: floor(float(x)), n))
            npp_table[n] = npp_table.get(n, 0) + 1
        return npp_table


class DataBaseP(DataBase):
    def __init__(self):
        super().__init__(os.path.join('cities', 'worldcities.csv'), dm=",")

    def get_cities(self):
        cities = []
        for line in self.table:
            d = dict()
            try:
                d['lat'], d['lng'] = line['lat'], line['lng']
                d['population'] = int(line['population'])
                cities.append(d)
            except KeyError:
                pass
            except ValueError:
                pass
        return cities

    def get_grid(self):
        cities = self.get_cities()
        pp_table = dict()
        for c in cities:
            coord = floor(float(c['lat'])), floor(float(c['lng']))
            pp_table[coord] = pp_table.get(coord, 0) + c['population']
        return pp_table


db_pp = DataBaseP()
pp_grid = db_pp.get_grid()
db_npp = DataBaseNPP()
npp_grid = db_npp.get_grid()

averages_grid = dict()
for el in npp_grid:
    if el in pp_grid:
        averages_grid[el] = pp_grid[el] / npp_grid[el]
averages = []
for v in averages_grid.values():
    averages.append(v)
averages.sort()
md = averages[len(averages) // 2]
needable_grid = dict()
for el in pp_grid:
    npp_n = npp_grid.get(el, 0)
    pp = pp_grid[el] - npp_n * md
    needable_grid[el] = pp / md
lst = [i for i in needable_grid.items()]
lst.sort(key=lambda x: x[1], reverse=True)
lst = lst[:5]

points = []
for el in lst:
    points.append(",".join([str(i) + ".0" for i in el[0][::-1]]) + ",flag")
req = "https://static-maps.yandex.ru/1.x/?size=450,450&l=map" + "&pt=" + "~".join(points)
print(req)
response = requests.get(req)
with open("map.png", "wb") as image:
    image.write(response.content)
