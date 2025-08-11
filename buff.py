import pygame
from constants import *
from circleshape import CircleShape

class Buff(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, BUFF_RADIUS)
        self.rotation = 0
        self.expiry = 150
    
    def apply_buff(self, player):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.square(), 2)
    
    def square(self):
        return [
            self.position.x - self.radius,
            self.position.y - self.radius,
            self.radius * 2,
            self.radius * 2
        ]

    def update(self, dt):
        self.position += self.velocity * dt





class Shield(Buff):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = "blue"

    def apply_buff(self, player):
        self.kill()
        player.shield += 1
        player.color = "blue"


class Power(Buff):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = "red"
    
    def apply_buff(self, player):
        self.kill()
        player.buff = "power"
        player.buff_timer = 10


class Speed(Buff):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = "yellow"

    def apply_buff(self, player):
        self.kill()
        player.buff = "speed"
        player.buff_timer = 10
