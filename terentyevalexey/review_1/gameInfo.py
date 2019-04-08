import pygame
import os
from enum import Enum
from singleton import singleton


class GameStatus(Enum):
    menu = 0
    options = 1
    loop = 2


class Animations(Enum):
    idle = [
        pygame.image.load(
            os.path.join('data', 'cat', 'idle_{}.png'.format(i)))
        for i in range(1, 5)]
    dead = [
        pygame.image.load(
            os.path.join('data', 'cat', 'dead_{}.png'.format(i)))
        for i in range(1, 8)]
    kick = [
        pygame.image.load(
            os.path.join('data', 'cat', 'kick_{}.png'.format(i)))
        for i in range(1, 9)]
    punch = [
        pygame.image.load(
            os.path.join('data', 'cat', 'punch_{}.png'.format(i)))
        for i in range(1, 7)]
    walk = [
        pygame.image.load(
            os.path.join('data', 'cat', 'walk_{}.png'.format(i)))
        for i in range(1, 9)]
    walk_left = [
        pygame.image.load(
            os.path.join('data', 'cat', 'walk_left_{}.png'.format(i)))
        for i in range(1, 9)]
    sleep = [
        pygame.image.load(
            os.path.join('data', 'cat', 'sleep_{}.png'.format(i)))
        for i in range(1, 8)]


@singleton
class GameInfo:
    def __init__(self):
        pygame.init()
        self.background = pygame.image.load(
            os.path.join('data', 'background.jpg'))
        self.arrow = pygame.image.load(os.path.join('data', 'arrow.png'))
        self.bamboo = pygame.image.load(os.path.join('data', 'bamboo.jpg'))
        self.display_inf = pygame.display.Info()
        self.logic_size = 10
        self.reduction_ratio = 2
        self.width = self.display_inf.current_w // \
            self.logic_size // self.reduction_ratio
        self.height = self.display_inf.current_h // \
            self.logic_size // self.reduction_ratio
        self.window_width = self.logic_size * self.width
        self.window_height = self.logic_size * self.height
        self.full_screen = False
        self.tick_rate = 30
        self.screen = pygame.display.set_mode((self.window_width,
                                               self.window_height))


@singleton
class Cat:
    def __init__(self):
        self.name = 'Kitty'
        game_info = GameInfo()
        self.x = game_info.width * 4
        self.y = game_info.height * 5
        self.anim_time = 0
        self.idle_time = 0
        self.status = Animations.idle
        self.cardio = 0
        self.muscle = 0
        self.tired = 0
        self.sleepy = 0

    def reset(self):
        self.name = "Kitty"
        game_info = GameInfo()
        self.x = game_info.width * 4
        self.y = game_info.height * 5
        self.anim_time = 0
        self.idle_time = 0
        self.cardio = 0
        self.muscle = 0
        self.tired = 0
        self.sleepy = 0

    def update_stats(self, event):
        if event.type == pygame.USEREVENT + 1:
            self.sleepy += 1
        if event.type == pygame.USEREVENT + 2:
            if self.muscle > 0:
                self.muscle -= 1
        if event.type == pygame.USEREVENT + 3:
            if self.cardio > 0:
                self.cardio -= 1

    def draw(self):
        game_info = GameInfo()
        if self.anim_time >= game_info.tick_rate:
            self.anim_time = 0

        cur_frame = self.anim_time // (
                game_info.tick_rate //
                len(self.status.value))
        self.anim_time += 1

        if cur_frame >= len(self.status.value):
            self.anim_time = 0
            return
        game_info.screen.blit(
            pygame.transform.scale(self.status.value[cur_frame],
                                   (game_info.width * 4, game_info.height * 4)),
            (self.x, self.y))
        pygame.display.update()
