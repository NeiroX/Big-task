import os
import sys

import pygame
import requests

map_params = {
    "ll": '37.530887,55.703118',
    "z": 15,  # from 0 to 17
    'l': 'map',  # map (схема), sat (спутник) и sat,skl (гибрид).
    'size': '650,450'
}
map_file = "static/img/map.png"


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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN:
                map_params['z'] -= 1 if map_params['z'] > 0 else 0
            if event.key == pygame.K_PAGEUP:
                map_params['z'] += 1 if map_params['z'] < 17 else 0
    create_image()
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()

os.remove(map_file)
