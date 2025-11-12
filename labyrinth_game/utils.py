import math
from typing import Dict
from labyrinth_game.constants import ROOMS

def pseudo_random(seed: int, modulo: int) -> int:
# генератор случайного числа на основе синуса
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional = x - math.floor(x)
    return int(fractional * modulo)

# Константы для ловушек
MODULO = 10
THRESHOLD = 3

def trigger_trap(game_state):

    print("Ловушка активирована! Пол стал дрожать")

    inv = game_state.get("player_inventory", [])
    steps = game_state.get("steps_taken", 0)

# Если у игрока есть предметы, то он теряет один случайный

    if inv:
        lost_index = pseudo_random(steps, len(inv))
        lost_item = inv.pop(lost_index)
        print(f"Вы потеряли предмет: {lost_item}")
    else:
        outcome = pseudo_random(steps, MODULO)
        if outcome < THRESHOLD:
            print("Пол внезапно проваливается под вами... Вы погибли.")
            game_state["game_over"] = True
        else:
            print("Вы чудом удержались на краю и выжили!")

# Константы для случайных событий
PROBABILITY = 10
VARIANTS = 3

def random_event(game_state):
# Случайное событие при перемещении игрока
    steps = game_state.get("steps_taken", 0)

    # Определяем, произойдет ли событие
    if pseudo_random(steps, PROBABILITY) != 0:
        return  # ничего не происходит

    # Выбираем тип события
    event_type = pseudo_random(steps + 1, VARIANTS)
    current_room = game_state["current_room"]
    room = ROOMS.get(current_room, {})
    inv = game_state["player_inventory"]

    if event_type == 0:
        # Сценарий 1: находка
        print("Монета ваша!")
        room.setdefault("items", []).append("coin")

    elif event_type == 1:
        # Сценарий 2: испуг
        print("Алярм! Шорох")
        if "sword" in inv:
            print("У тебя меч, шорох пропадает")

    elif event_type == 2:
        # Сценарий 3: ловушка
        if current_room == "trap_room" and "torch" not in inv:
            print("В темноте вы наступили на подозрительную плиту...")
            trigger_trap(game_state)




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



def solve_puzzle(game_state):
    current = game_state["current_room"]
    room = ROOMS.get(current, {})

    if not room.get("puzzle"):
        print("Загадок здесь нет.")
        return

    question, correct = room["puzzle"]
    print(question)

    from labyrinth_game.player_actions import get_input
    answer = get_input("Ваш ответ: ").strip().lower()



    if answer in valid_answers:
        print("Верно! Загадка решена.")
        room["puzzle"] = None

        # Награда за решение
        if current == "hall":
            print("Вы открыли сундук и нашли ключ от сокровищницы!")
            game_state["player_inventory"].append("treasure_key")
        elif current == "library":
            print("Вы находите старинный свиток с подсказками.")
            game_state["player_inventory"].append("ancient_scroll")
        else:
            print("Вы чувствуете прилив уверенности и желания идти дальше!")

    else:
        print("Неверно. Попробуйте снова.")
        # Если это ловушка — активируем её
        if current == "trap_room":
            from labyrinth_game.utils import trigger_trap
            trigger_trap(game_state)

def attempt_open_treasure(game_state):
    current = game_state["current_room"]
    if current != "treasure_room":
        print("Здесь нет сундука.")
        return

    room = ROOMS.get(current, {})
    items = room.get("items", [])

    if "treasure_chest" not in items:
        print("Сундук уже открыт или отсутствует.")
        return

    inv = game_state.get("player_inventory", [])

    if "treasure_key" in inv:
        print("Сундук открыт!")
        items.remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    # Предложить ввести код
    from labyrinth_game.player_actions import get_input
    ans = get_input(
        "Сундук заперт. Хотите ввести код? (да/нет) "
        ).strip().lower()
    if ans in ("да", "yes", "y"):
        puzzle = room.get("puzzle")
        if not puzzle:
            print("Нет подсказки к этому сундуку.")
            return
        _, correct = puzzle
        code = get_input("Введите код: ").strip()
        if code.lower() == correct.lower():
            print("Код верный! Сундук открыт.")
            items.remove("treasure_chest")
            print("В сундуке сокровище! Вы победили!")
            game_state["game_over"] = True
        else:
            print("Неверный код.")
    else:
        print("Вы отступаете от сундука.")

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")