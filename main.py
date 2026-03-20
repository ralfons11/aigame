from random import randint

def create_game(length):
    # Generē virkni ar skaitļiem 1, 2, 3, 4
    return [randint(1, 4) for _ in range(length)]

def make_move(numbers, choice, total, bank, action):
    new_numbers = numbers.copy()
    try:
        index = new_numbers.index(choice)
        new_numbers.pop(index)
    except ValueError:
        return numbers, total, bank

    if action == "take":
        total += choice # Pieskaita skaitli kopējam punktu skaitam
    elif action == "split" and choice == 2:
        new_numbers.extend([1, 1]) # Sadala 2 divos 1
        bank += 1 # Papildina banku par 1
    elif action == "split" and choice == 4:
        new_numbers.extend([2, 2]) # Sadala 4 divos 2
        total += 2 # Pieskaita 2 punktus kopējam skaitam

    return new_numbers, total, bank

def get_winner(total, bank):
    # Uzvaras nosacījumi
    if total % 2 == 0 and bank % 2 == 0:
        return "Uzvar spēlētājs, kurš uzsāka spēli (Pāra/Pāra)!"
    elif total % 2 != 0 and bank % 2 != 0:
        return "Uzvar otrais spēlētājs (Nepāra/Nepāra)!"
    else:
        return "Neizšķirts!"