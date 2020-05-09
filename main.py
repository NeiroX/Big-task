import os
import sys

import pygame
import requests

map_params = {
    "ll": [37.530887, 55.703118],
    "z": 15,  # from 0 to 17
    'l': 'map',  # map (схема), sat (спутник) и sat,skl (гибрид).
    'size': [650, 450]
}
map_file = "static/img/map.png"

size = {pygame.K_PAGEUP: -1, pygame.K_PAGEDOWN: 1}
coordinates = {pygame.K_DOWN: (0, -0.001),
               pygame.K_UP: (0, 0.001),
               pygame.K_LEFT: (-0.001, 0),
               pygame.K_RIGHT: (0.001, 0)}


def create_image():
    response = None

    map_request = "http://static-maps.yandex.ru/1.x/?"
    req_params = {key: (map_params[key]
                        if not isinstance(map_params[key], list)
                        else ','.join(map(str, map_params[key])))
                  for key in map_params.keys()}
    response = requests.get(map_request, params=req_params)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    with open(map_file, "wb") as file:
        file.write(response.content)


pygame.init()

create_image()
img = pygame.image.load(map_file)
screen = pygame.display.set_mode((img.get_width(), img.get_height()))
screen.blit(img, (0, 0))
running = True
while running:
    keys = pygame.key.get_pressed()
    for evnt in pygame.event.get():
        if evnt.type == pygame.QUIT:
            running = False
        elif evnt.type == pygame.KEYDOWN:
            if evnt.key in [pygame.K_PAGEDOWN, pygame.K_PAGEUP]:
                map_params['z'] += size[evnt.key] if 0 < map_params['z'] < 17 else -map_params['z'] + 1
            elif evnt.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP]:
                x, y = coordinates[evnt.key]
                map_params['ll'][0] += x
                map_params['ll'][1] += y
            create_image()
            screen.blit(pygame.image.load(map_file), (0, 0))

    pygame.display.flip()
pygame.quit()

os.remove(map_file)
