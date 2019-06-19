import pygame, time, random
from pygame.locals import *
from datetime import datetime, timedelta

""" Initialise Pygame """
pygame.init()
#window = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame_width, pygame_height = pygame.display.get_surface().get_size()
fps = pygame.time.Clock()

#fonts = pygame.font.get_fonts()
#print(fonts)
#exit()

""" Pygame Constants """
BACKGROUND = (0x00, 0x00, 0x00)
BACKGROUND_WARN = (0xF4, 0x41, 0x41)
BACKGROUND_OVER = (0xFF, 0xFF, 0xFF)
TEXT = (0xF0, 0xF0, 0xF0)
TEXT_OVER = (0x00, 0x00, 0x00)
PAUSED = (0x80, 0x80, 0x80)
FONT_L = pygame.font.SysFont("couriernew", 400)
FONT_S = pygame.font.SysFont("couriernew", 64)

seconds_remaining = 600
clock_running = False
quit = False
epoch = datetime.now().timestamp()
epoch_last_processed = epoch

while not quit:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quit = True
            if event.key == K_r:
                clock_running = False
                seconds_remaining = 600
            if event.key == K_z:
                clock_running = False
                seconds_remaining = 0
            if event.key == K_s:
                seconds_remaining -= 60
            if event.key == K_a:
                seconds_remaining += 60
            if event.key == K_SPACE:
                clock_running = not clock_running
        elif event.type == VIDEORESIZE:
            surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            pygame_width, pygame_height = pygame.display.get_surface().get_size()

    # Calculations
    epoch = datetime.now().timestamp()
    if epoch >= (epoch_last_processed+1):
        epoch_last_processed = epoch
        if clock_running:
            seconds_remaining = seconds_remaining - 1


    m = (abs(seconds_remaining) % 3600) // 60
    s = (abs(seconds_remaining) % 60)
    clock_position = (int(pygame_width/2) - 600, int(pygame_height/2) - 200)
    text_position = (int(pygame_width/2) - 600, pygame_height - 100)

    # Draw background
    if seconds_remaining > 60: # 1 minute warning
        window.fill(BACKGROUND)
        clock_font_color = TEXT
    elif seconds_remaining >= 0:
        window.fill(BACKGROUND_WARN)
        clock_font_color = TEXT
    elif seconds_remaining < 0:
        window.fill(BACKGROUND_OVER)
        clock_font_color = TEXT_OVER

    # Draw clock foreground
    if clock_running:
        if (int(seconds_remaining) % 2 == 0):
            time_remaining = f"{m:02} {s:02}"
            window.blit(FONT_L.render(time_remaining, 1, clock_font_color), clock_position)
        else:
            time_remaining = f"{m:02}:{s:02}"
            window.blit(FONT_L.render(time_remaining, 1, clock_font_color), clock_position)
    else: # paused
        time_remaining = f"{m:02}:{s:02}"
        window.blit(FONT_L.render(time_remaining, 1, TEXT), clock_position)
        window.blit(FONT_S.render("PAUSED", 1, TEXT), text_position)

    pygame.display.update() # Actually does the screen update
    fps.tick(25) # Run the game at 25 frames per second
pygame.quit()

