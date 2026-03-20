from random import randint


def create_game(length):
    numbers = []
    for _ in range(length):
        numbers.append(randint(1, 4))
    return numbers


def make_move(numbers, choice, total, bank, action):
    numbers = numbers.copy()
    index = numbers.index(choice)

    numbers.pop(index)

    # 🔹 vienkārši paņem
    if action == "take":
        total += choice

    # 🔹 sadala 2
    elif action == "split" and choice == 2:
        numbers.insert(index, 1)
        numbers.insert(index + 1, 1)
        bank += 1

    # 🔹 sadala 4
    elif action == "split" and choice == 4:
        numbers.insert(index, 2)
        numbers.insert(index + 1, 2)
        total += 2

    return numbers, total, bank


def get_winner(total, bank):
    if total % 2 == 0 and bank % 2 == 0:
        return "Uzvar pirmais spēlētājs!"

    elif total % 2 == 1 and bank % 2 == 1:
        return "Uzvar otrais spēlētājs!"

    else:
        return "Neizšķirts!"