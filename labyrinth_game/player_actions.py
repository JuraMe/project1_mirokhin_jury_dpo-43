
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