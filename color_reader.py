import pygame
path=pygame.image.load("Resources/Maps/Test_Map/The Interface.png")
unique_colors=set()
for x in range(path.get_width()):
    for y in range(path.get_height()):
        new_color=path.get_at((x,y))[:-1]
        unique_colors.add(new_color)
for i in unique_colors:
    print(i)