import random
import pygame

pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("MINION Game")

clock = pygame.time.Clock()

background = pygame.image.load("C:/Users/shw46_000/Desktop/pythonProject1/pygame_basic/background_minions.png")

stage = pygame.image.load("C:/Users/shw46_000/Desktop/pythonProject1/pygame_basic/stage.png")
stage_size = stage.get_rect().size
stage_height = stage_size[1]

character = pygame.image.load("C:/Users/shw46_000/Desktop/pythonProject1/pygame_basic/minion.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

character_to_x = 0

character_speed = 5

weapon = pygame.image.load("C:/Users/shw46_000/Desktop/pythonProject1/pygame_basic/weapon.png")
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

weapons = []

weapon_speed = 10

enemy_images = [
    pygame.image.load("C:/Users/shw46_000/Desktop/pythonProject1/pygame_basic/evil_minion_1.png"),
    pygame.image.load("C:/Users/shw46_000/Desktop/pythonProject1/pygame_basic/evil_minion_2.png"),
    pygame.image.load("C:/Users/shw46_000/Desktop/pythonProject1/pygame_basic/evil_minion_3.png"),
    pygame.image.load("C:/Users/shw46_000/Desktop/pythonProject1/pygame_basic/evil_minion_4.png")
]

enemy_speed_y = [-18, -15, -12, -9]

enemies = []

enemies.append({
    "pos_x" : 50,
    "pos_y" : 50,
    "img_idx" : 0,
    "to_x" : 3,
    "to_y" : -6,
    "init_spd_y" : enemy_speed_y[0]
})

weapon_to_remove = -1
enemy_to_remove = -1

game_font = pygame.font.Font(None, 50)

game_result = "Game Over"

total_time = 100

start_ticks = pygame.time.get_ticks()

running = True
while running:
    dt = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]

    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    for enemy_idx, enemy_val in enumerate(enemies):
        enemy_pos_x = enemy_val["pos_x"]
        enemy_pos_y = enemy_val["pos_y"]
        enemy_img_idx = enemy_val["img_idx"]

        enemy_size = enemy_images[enemy_img_idx].get_rect().size
        enemy_width = enemy_size[0]
        enemy_height = enemy_size[1]

        if enemy_pos_x < 0 or enemy_pos_x > screen_width - enemy_width:
            enemy_val["to_x"] = enemy_val["to_x"] * -1

        if enemy_pos_y >= screen_height - stage_height - enemy_height:
            enemy_val["to_y"] = enemy_val["init_spd_y"]
        else:
            enemy_val["to_y"] += 0.5

        enemy_val["pos_x"] += enemy_val["to_x"]
        enemy_val["pos_y"] += enemy_val["to_y"]


    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for enemy_idx, enemy_val in enumerate(enemies):
        enemy_pos_x = enemy_val["pos_x"]
        enemy_pos_y = enemy_val["pos_y"]
        enemy_img_idx = enemy_val["img_idx"]

        enemy_rect = enemy_images[enemy_img_idx].get_rect()
        enemy_rect.left = enemy_pos_x
        enemy_rect.top = enemy_pos_y

        if character_rect.colliderect(enemy_rect):
            running = False
            break

        for weapon_idx,  weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            if weapon_rect.colliderect(enemy_rect):
                weapon_to_remove = weapon_idx
                enemy_to_remove = enemy_idx

                if enemy_img_idx < 3:

                    enemy_width = enemy_rect.size[0]
                    enemy_height = enemy_rect.size[1]

                    small_enemy_rect = enemy_images[enemy_img_idx + 1].get_rect()
                    small_enemy_width = small_enemy_rect.size[0]
                    small_enemy_height = small_enemy_rect.size[1]

                    enemies.append({
                        "pos_x": enemy_pos_x + (enemy_width / 2) - (small_enemy_width / 2),
                        "pos_y": enemy_pos_y + (enemy_height / 2) - (small_enemy_height / 2),
                        "img_idx": enemy_img_idx + 1,
                        "to_x": -3,
                        "to_y": -6,
                        "init_spd_y": enemy_speed_y[enemy_img_idx + 1]
                    })

                    enemies.append({
                        "pos_x": enemy_pos_x + (enemy_width / 2) - (small_enemy_width / 2),
                        "pos_y": enemy_pos_y + (enemy_height / 2) - (small_enemy_height / 2),
                        "img_idx": enemy_img_idx + 1,
                        "to_x": 3,
                        "to_y": -6,
                        "init_spd_y": enemy_speed_y[enemy_img_idx + 1]
                    })
                break
        else:
            continue
        break

    if enemy_to_remove > -1:
        del enemies[enemy_to_remove]
        enemy_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    if len(enemies) == 0:
        game_result = "Mission Complete"
        running = False


    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(enemies):
        enemy_pos_x = val["pos_x"]
        enemy_pos_y = val["pos_y"]
        enemy_img_idx = val["img_idx"]
        screen.blit(enemy_images[enemy_img_idx], (enemy_pos_x, enemy_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))



    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update()

msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)

pygame.display.update()

pygame.time.delay(2000)

pygame.quit()