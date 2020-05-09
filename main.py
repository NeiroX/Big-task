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
    response = requests.get(map_request, params=map_params)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    with open(map_file, "wb") as file:
        file.write(response.content)


pygame.init()
screen = pygame.display.set_mode((650, 450))
running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_PAGEDOWN, pygame.K_PAGEUP]:
                map_params['z'] += size[event.key] if 0 < map_params['z'] < 17 else -map_params['z'] + 1
            elif event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP]:
                x, y = coordinates[event.key]
                map_params['ll'][0] += x
                map_params['ll'][1] += y
            elif event.key == pygame.K_1:
                map_params['l'] = 'map'
            elif event.key == pygame.K_2:
                map_params['l'] = 'sat'
            elif event.key == pygame.K_3:
                map_params['l'] = 'sat,skl'
    create_image()
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()

os.remove(map_file)
