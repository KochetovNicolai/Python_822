import pygame
import field
"""Обрабатывает события в игре"""


class EventHandler:
    def __init__(self):
        self.evolution_tick = 6

    def event_handler(self, events, mode_, d, gamefield_, menu_):
        """Обработчик событий игры"""

        done_ = d

        # Должен вернуть пару из mode, done

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if (mode_ == 'draw' or mode_ == 'pause') \
                        and mouse_pos[1] < gamefield_.field_size[1] - field.Field.menu_height:
                    gamefield_.click(mouse_pos)

                if mouse_pos[1] > gamefield_.field_size[1] - field.Field.menu_height:
                    mode_ = menu_.click(mouse_pos, mode_)
            if event.type == pygame.QUIT or mode_ == 'quit':
                done_ = True
            elif event.type == pygame.KEYDOWN and mode_ == 'draw':
                if event.key == pygame.K_RETURN:
                    mode_ = 'evolution'  # начало эволюции
                    print('evolution mode on')

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done_ = True
                if event.key == pygame.K_SPACE:
                    if mode_ == 'evolution':
                        mode_ = 'pause'
                    elif mode_ == 'pause':
                        mode_ = 'evolution'

                # Управление скорростью игры клавишами
                if event.key == pygame.K_UP:
                    self.evolution_tick = min(30, self.evolution_tick + 1)
                if event.key == pygame.K_DOWN:
                    self.evolution_tick = max(1, self.evolution_tick - 1)

        return mode_, done_
