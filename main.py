import cv2
from PIL import Image
from constants import *
import os
import csv

DELTA = 25


def frame_capture(path) -> None:
    video_obj = cv2.VideoCapture(path)
    success = True
    count = 0
    while success:
        count += 1
        success, image = video_obj.read()
        try:
            cv2.imwrite(f'frames/frame_{count}.jpg', image)
        except cv2.error as e:
            print(e)
            pass
    return count


def get_laser_point(name):
    image = Image.open('frames/' + name)
    pixels = image.load()
    width, height = image.size

    pixels_cost = set()
    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j][0:3]
            pixels_cost.add((i, j, r + g + b))

    laser_pix = set()
    q = max(*pixels_cost, key=lambda x: x[2])[2]
    for i in pixels_cost:
        if q - DELTA <= i[2] <= q + DELTA:
            laser_pix.add(i)

    x, y = 0, 0
    length = 0
    for i in laser_pix:
        length += 1
        x += i[0]
        y += i[1]

    x //= length
    y //= length

    for i in laser_pix:
        pixels[i[0], i[1]] = (0, 0, 255)

    pixels[x, y] = (255, 0, 0)
    return x, y
    # image.save('output/' + name)


def save_data(data, name='frames_data_.csv'):
    with open(name, mode='ab') as file:
        for line in data:
            file.write(bytes(', '.join(map(str, line)) + '\n', encoding='UTF-8'))


"""def get_positions_from_csv(name='frames_data_.csv'):
    with open(name, mode='r') as file:
        min_x, min_y = -1, -1
        max_x, max_y = -1, -1
        for line in file:
            x, y = map(int, line.split(', '))"""





if __name__ == '__main__':
    """print('Start to frames video')
            count = frame_capture('video.mp4')
            print('Done!\n Laser position detection begins...')"""
    count = 2143
    min_x, min_y = 99999999999, 9999999999999
    max_x, max_y = -1, -1
    for file in range(1, count + 1):
        print(f'{file}/{count}', end=': ')
        file = 'frame_' + str(file) + '.jpg'
        x, y = get_laser_point(file)
        print(x, y)
        save_data(((x, y),))
        min_x, min_y = 99999999999, 9999999999999
        max_x, max_y = -1, -1
        if min_x > x:
            min_x = x
        elif max_x < x:
            max_x = x
        if min_y > y:
            min_y = y
        elif max_y < y:
            max_y = y

    print('\n')
    print(max_x, max_y)
    print(min_x, min_y)
    file = open('answer.csv', mode='w')
    file.write(', '.join(map(str, (X_ZERO, Y_ZERO, max_x, max_y, MIKROMETR, abs((max_y - Y_TEN) / MIKROMETR)))))
