# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
import random
import time
from constants import *
from circleshape import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *
from buff import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PyAsteroids")
    clock = pygame.time.Clock()
    dt = 0
    score = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    buffs = pygame.sprite.Group()
    gameover = pygame.sprite.Group()

    Player.containers = (updatable, drawable, gameover)
    Shot.containers = (shots, updatable, drawable, gameover)
    Buff.containers = (buffs, updatable, drawable, gameover)
    Asteroid.containers = (asteroids, updatable, drawable, gameover)
    AsteroidField.containers = (updatable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    main_font = pygame.font.Font("freesansbold.ttf", 32)

    title_a = main_font.render("Welcome to PyAsteroids!", True, "white")
    title_rect_a = title_a.get_rect()
    title_rect_a.center = (SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 4)
    
    title_b = main_font.render("Press Space to begin", True, "white")
    title_rect_b = title_b.get_rect()
    title_rect_b.center = (SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 2)

    game_over_a = main_font.render("Game over!", True, "white")
    game_over_a_rect = game_over_a.get_rect()
    game_over_a_rect.center = (SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 4)

    game_over_b = main_font.render(f"You survived {str(score)} seconds!", True, "white")
    game_over_b_rect = game_over_b.get_rect()
    game_over_b_rect.center = (SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 2)


    mode = "menu"

    while True:
        while mode == "menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            screen.fill("black")           
            screen.blit(title_a, title_rect_a)
            screen.blit(title_b, title_rect_b)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                mode = "game"
                score_start = time.time()

            pygame.display.flip()
            dt = clock.tick(60) / 1000

        while mode == "game":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            screen.fill("black")

            updatable.update(dt)
            
            for ast in asteroids:
                if ast.check_for_collision(player):
                    if player.shield > 0:
                        player.shield -= 1
                        ast.kill()
                        if player.shield == 0:
                            player.color = "white"
                    else:
                        score_end = time.time()
                        score = round(score_end - score_start)
                        game_over_a = main_font.render("Game over!", True, "white")
                        game_over_a_rect = game_over_a.get_rect()
                        game_over_a_rect.center = (SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 4)
                        game_over_b = main_font.render(f"You survived {str(score)} seconds!", True, "white")
                        game_over_b_rect = game_over_b.get_rect()
                        game_over_b_rect.center = (SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 2)
                        for item in gameover:
                            item.kill()
                        screen.blit(game_over_a, game_over_a_rect)
                        screen.blit(game_over_b, game_over_b_rect)
                        pygame.display.flip()
                        time.sleep(2.5)
                        mode = "menu"
                    
                for shot in shots:
                    if ast.check_for_collision(shot):
                        if shot.color == "red":
                            ast.kill()
                        else:
                            ast.split()
                        shot.kill()
                        if random.randint(1, 5) == 5:
                            buff = globals()[random.choice(["Shield", "Power", "Speed"])](ast.position.x, ast.position.y)


            for bf in buffs:
                if bf.check_for_collision(player):
                    bf.apply_buff(player)
                if bf.expiry == 0:
                    bf.kill()
                else:
                    bf.expiry -= 1

            for obj in drawable:
                obj.draw(screen)



            pygame.display.flip()
            dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
