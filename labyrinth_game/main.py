#!/usr/bin/env python3
from copy import deepcopy

from labyrinth_game import player_actions, utils
from labyrinth_game.constants import COMMANDS

game_state_template = {
    "player_inventory": [],  # Инвентарь игрока
    "current_room": "entrance",  # Текущая комната
    "game_over": False,  # Значения окончания игры
    "steps_taken": 0,  # Количество шагов
}


def process_command(game_state, command):
    # Обработка введённой пользователем команды
    parts = command.strip().lower().split()
    if not parts:
        print("Введите команду. (help — список команд)")
        return

    cmd = parts[0]
    arg = parts[1] if len(parts) > 1 else None

    #  короткие команды направления
    directions = ("north", "south", "east", "west")
    if cmd in directions:
        player_actions.move_player(game_state, cmd)
        return

    # разбор стандартных команд
    match cmd:
        case "go":
            if arg:
                player_actions.move_player(game_state, arg)
            else:
                print("Укажите направление: north/south/east/west.")

        case "look":
            utils.describe_current_room(game_state)

        case "take":
            if arg:
                player_actions.take_item(game_state, arg)
            else:
                print("Укажите предмет, который хотите взять.")

        case "use":
            if arg:
                player_actions.use_item(game_state, arg)
            else:
                print("Укажите предмет, который хотите использовать.")

        case "inventory":
            player_actions.show_inventory(game_state)

        case "solve":
            if game_state["current_room"] == "treasure_room":
                utils.attempt_open_treasure(game_state)
            else:
                utils.solve_puzzle(game_state)

        case "help":
            utils.show_help(COMMANDS)

        case "quit" | "exit":
            print("Вы покидаете лабиринт. Игра окончена.")
            game_state["game_over"] = True

        case _:
            print("Неизвестная команда. Введите 'help' для списка.")


def main():
    game_state = deepcopy(game_state_template)
    print("Добро пожаловать в Лабиринт сокровищ!")
    utils.describe_current_room(game_state)

    while not game_state["game_over"]:
        cmd = player_actions.get_input("> ")
        process_command(game_state, cmd)


if __name__ == "__main__":
    main()
