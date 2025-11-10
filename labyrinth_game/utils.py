from typing import Dict
from labyrinth_game.constants import ROOMS

def describe_current_room(game_state: Dict):
    room_key = game_state["current_room"]
    room = ROOMS.get(room_key)
    if not room:
        print("Неизвестная локация.")
        return

    # Заголовок
    print(f"\n== {room_key.upper()} ==")
    # Описание
    print(room["description"])

    # Предметы
    items = room.get("items", [])
    if items:
        print("\nЗаметные предметы:")
        for it in items:
            print(f"  - {it}")

    # Выходы
    exits = room.get("exits", {})
    if exits:
        print("\nВыходы:")
        print("  " + ", ".join(exits.keys()))

    # Загадка
    if room.get("puzzle"):
        print("\nКажется, здесь есть загадка (используйте команду solve).")