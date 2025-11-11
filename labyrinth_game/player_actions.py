
from typing import Dict
from labyrinth_game.constants import ROOMS

def show_inventory(game_state: Dict):
    inv = game_state.get("player_inventory", [])
    if not inv:
        print("Ваш инвентарь пуст.")
        return
    print("Инвентарь:")
    for item in inv:
        print(f"  - {item}")

def get_input(prompt: str = "> ") -> str:
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state, direction: str):
    current = game_state["current_room"]
    room = ROOMS.get(current, {})
    exits = room.get("exits", {})
    direction = direction.lower()

    if direction in exits:
        new_room = exits[direction]
        game_state["current_room"] = new_room
        game_state["steps_taken"] += 1
        from labyrinth_game.utils import describe_current_room
        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")