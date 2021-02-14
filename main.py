import cv2
from PIL import Image
import os

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
            break


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
    print(x, y)
    #image.save('output/' + name)


if __name__ == '__main__':
    print('Start to frames video')
    frame_capture('дилатометр 2.mp4')
    print('Done!\n Laser position detection begins...')

    files = os.listdir('frames/')
    for i, file in enumerate(files):
        print(f'{i}/{len(files)}: ' + file)
        get_laser_point(file)
