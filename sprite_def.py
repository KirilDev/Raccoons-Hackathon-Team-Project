import pygame
player_sprite=pygame.transform.flip(pygame.image.load("Resources\\Sprites\\Remove_background_project_1.png"),1,0)
player_map_sprite=pygame.transform.scale(player_sprite,(100,100))
cubican_sprite=pygame.image.load("Resources\\Sprites\\cube.png")
def center(surface,sprite,x,y):
    surface.blit(sprite,(x-sprite.get_width()/2,y-sprite.get_height()/2))
fonts={}
texts={}
def render_text(text="PLACEHOLDER TEXT, YOU SHOULD FIX THIS",size=20,color=(255,255,255),font="Napoli.ttf",bold=False,italic=False):
    font_key=str(font)+str(size)+str(int(bold))+str(int(italic))
    text_key=str(text)+str(color)+str(font_key)
    if not font_key in fonts:
        fonts[font_key]=pygame.font.Font(f"Resources\\Fonts\\{font}",size=int(size))
    if not text_key in texts:
        texts[text_key]=fonts[font_key].render(str(text),1,color)
    return texts[text_key]
