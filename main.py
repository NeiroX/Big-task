import os
import sys

import pygame
import requests

response = None
map_params = {
    "ll": '37.530887,55.703118',
    "spn": '0.01,0.01',
    "z": 15,  # from 0 to 17
    'l': 'map'  # map (схема), sat (спутник) и sat,skl (гибрид).
}

map_request = "http://static-maps.yandex.ru/1.x/?"
response = requests.get(map_request, params=map_params)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "static/img/map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 600))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

os.remove(map_file)
