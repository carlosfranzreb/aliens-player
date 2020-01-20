import pygame
from pygame.locals import Rect


SCREENRECT = Rect(0, 0, 640, 480)


class Compu_player(pygame.sprite.Sprite):
    """
    Position: center = self.rect.midtop
    pos. center at the beginning = 320
    left_border = center - ((self.rect.right - self.rect.left) / 2)
    right_border = center + ((self.rect.right - self.rect.left) / 2)
    left_limit = 0
    right_limit = 640
    """
    speed = 10
    bounce = 24
    gun_offset = -11
    images = []

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[1]
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.reloading = False
        self.origtop = self.rect.top
        self.facing = 1

    def move(self, bombs):
        direction = self.decide_moving(bombs)
        if direction:
            self.facing = direction
        self.rect.move_ip(direction*self.speed, 0)
        self.rect = self.rect.clamp(SCREENRECT)
        if direction < 0:
            self.image = self.images[0]
        elif direction > 0:
            self.image = self.images[1]
        self.rect.top = self.origtop - (self.rect.left//self.bounce % 2)

    def fire(self, aliens):
        return self.sharphooter(aliens)

    def sharphooter(self, aliens):
        if self.reloading:
            return False
        else:
            for a in aliens:
                if round(a.rect.bottom / 72) == 4:  # y_level
                    gunpos = self.facing * self.gun_offset + self.rect.centerx
                    dist = round(a.facing / 13) * (gunpos - a.rect.centerx)
                    if dist in range(124, 184):
                        return True

            for a in aliens:
                if round(a.rect.bottom / 72) == 3:  # y_level
                    gunpos = self.facing * self.gun_offset + self.rect.centerx
                    dist = round(a.facing / 13) * (gunpos - a.rect.centerx)
                    if dist in range(210, 270):
                        return True
        return False

    def ak_47(self):
        if self.reloading:
            return False
        else:
            return True

    def decide_moving(self, bombs):
        """
        Move if bomb over player. Try to stay in the middle.
        """
        if len(bombs) == 0:
            if self.rect.centerx > 340:
                return -1
            elif self.rect.centerx < 300:
                return 1

        for b in bombs:
            if b.pos[0] in range(self.rect.left-10, self.rect.right+10):
                if self.rect.right > 630:
                    return -1
                elif self.rect.left < 10:
                    return 1
                else:
                    return self.facing

        return 0

    def gunpos(self):
        pos = self.facing*self.gun_offset + self.rect.centerx
        return pos, self.rect.top
