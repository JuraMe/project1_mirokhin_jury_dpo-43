from typing import Dict

from labyrinth_game.constants import ROOMS


# Функция отображения инвентаря
def show_inventory(game_state: Dict):
    inv = game_state.get("player_inventory", [])
    if not inv:
        print("Ваш инвентарь пуст")
        return
    print("Инвентарь:")
    for item in inv:
        print(f"  - {item}")


# Ввод пользователя
def get_input(prompt: str = "> ") -> str:
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


# Функция перемещения
def move_player(game_state, direction: str):
    current = game_state["current_room"]
    room = ROOMS.get(current, {})
    exits = room.get("exits", {})
    direction = direction.lower()

    if direction not in exits:
        print("Нельзя пойти в этом направлении.")
        return

    new_room = exits[direction]

    # Проверка перехода в комнату сокровищ
    if new_room == "treasure_room":
        if "rusty_key" not in game_state["player_inventory"]:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return
        else:
            print(
                "Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ."
            )

    # Обновляем состояние игрока
    game_state["current_room"] = new_room
    game_state["steps_taken"] += 1

    from labyrinth_game.utils import describe_current_room, random_event

    # Показываем описание новой комнаты
    describe_current_room(game_state)

    # Вызываем случайное событие
    random_event(game_state)


# Функция взятия предмета
def take_item(game_state, item_name: str):
    item_name = item_name.strip()
    current = game_state["current_room"]
    room = ROOMS.get(current, {})
    items = room.get("items", [])

    if item_name in items:
        game_state["player_inventory"].append(item_name)
        items.remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state, item_name: str):
    item_name = item_name.strip()
    inv = game_state.get("player_inventory", [])

    if item_name not in inv:
        print("У вас нет такого предмета.")
        return

    # выводит сообщение о том, что стало светлее
    if item_name == "torch":
        print("Стало светлее ")
    # сообщение об уверенности
    elif item_name == "sword":
        print("Взял меч, чувствуете себя увереннее.")
    # сообщение об открытии шкатулки
    elif item_name == "bronze_box":
        if "rusty_key" not in inv:
            print("Открыта бронзовая шкатулка")
            inv.append("rusty_key")
        else:
            print("Шкатулка пустая.")
    else:
        print("Вы не знаете, как использовать этот предмет.")
