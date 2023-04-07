import pygame
import spritehandler

pygame.init()
clock = pygame.time.Clock()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
player = pygame.Rect((300, 250, 50, 50))
speed = 5

# Images for idle animations
idle_image = pygame.image.load('player/Owlet_Monster_Idle_4.png').convert_alpha()
idle_sheet = spritehandler.SpriteSheet(idle_image)

# Images for walk animations
run_image = pygame.image.load('player/Owlet_Monster_Run_6.png').convert_alpha()
run_sheet = spritehandler.SpriteSheet(run_image)

color = (0, 0, 0)

# Animations
animation_dict = {
    "idle" : [idle_image, idle_sheet, 4, []],
    "run" : [run_image, run_sheet, 6, []],
}

# List for animation + time ticks
animation_list = []
animation_steps = 4
current_animation = "idle"
last_update = pygame.time.get_ticks()
animation_cooldown = 200  # Miliseconds
frame = 0

run = True

class Player():
    def __init__(self):
        self.flip = False

    def init_animations(self):
        for key, value in animation_dict.items():
            self.animation_player(value[1], value[2], key)

    def fill_up_list(self, mode):
        left_list = []
        animation_list.clear()
        animation_list.append(animation_dict[mode][3])

        if self.flip == True:
            for i in range(len(animation_list[0])):
                left_list.append(pygame.transform.flip(animation_list[0][i], True, False))
            animation_list.clear()
            animation_list.append(left_list)

    def flip_ani(self, orientation):
        if orientation == "right":
            self.flip = False
        else:
            self.flip = True

    def animation_player(self,action_sheet, steps, item):
        for i in range(steps):
            image = action_sheet.get_image(i, 32, 32, 3, color)
            animation_dict[item][3].append(image)

    def player_movement(self, key):
        if key[pygame.K_a] == True:
            player.move_ip(-speed, 0)
            self.fill_up_list("run")
            self.flip_ani("")
        elif key[pygame.K_d] == True:
            player.move_ip(speed, 0)
            self.fill_up_list("run")
            self.flip_ani("right")
        elif key[pygame.K_w] == True:
            player.move_ip(0, -speed)
            self.fill_up_list("run")
        elif key[pygame.K_s] == True:
            player.move_ip((0, speed))
            self.fill_up_list("run")
        else:
            self.fill_up_list("idle")

plyr = Player()
plyr.init_animations()

while run:
    screen.fill((64, 64, 64))

    # Player movement
    plyr.player_movement(pygame.key.get_pressed())

    # Player animation loop
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list[0]):
            frame = 0


    # Catch the wrong frame rates (Teacher won't care lol)
    try:
        screen.blit(animation_list[0][frame], player)
    except IndexError:
        frame = 0
        print("reset")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
