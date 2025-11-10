#!/usr/bin/env python3
from copy import deepcopy

from labyrinth_game.constants import ROOMS
from labyrinth_game import player_actions, utils

game_state = {
    'player_inventory': [],  # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната
    'game_over': False,  # Значения окончания игры
    'steps_taken': 0  # Количество шагов
}

def main():
    game_state = deepcopy(game_state_template)
    print("Добро пожаловать в Лабиринт сокровищ!")
    utils.describe_current_room(game_state)

    while not game_state["game over"]:
        cmd = player_actions.get_input("> ")
        process_command(game_state, cmd)


if __name__ == "__main__":
    main()