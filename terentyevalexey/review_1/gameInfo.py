from singleton import singleton
import pygame
import os
from enum import Enum


@singleton
class GameInfo:
    def __init__(self):
        pygame.init()
        self.background = pygame.image.load(
            os.path.join('data', 'background.jpg'))
        self.arrow = pygame.image.load(os.path.join('data', 'arrow.png'))
        self.bamboo = pygame.image.load(os.path.join('data', 'bamboo.jpg'))
        self.display_inf = pygame.display.Info()
        self.width = self.display_inf.current_w // 20
        self.height = self.display_inf.current_h // 20
        self.full_screen = False
        self.tick_rate = 30
        self.screen = pygame.display.set_mode(
            (self.width * 10, self.height * 10))


@singleton
class Cat:
    def __init__(self):
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
