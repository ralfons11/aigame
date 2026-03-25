import time
from main import make_move


class Node:
    def __init__(self, numbers, turn, total, bank, move=None):
        self.numbers = sorted(numbers)
        self.turn = turn
        self.total = total
        self.bank = bank
        self.move = move
        self.children = []
        self.value = 0

nodes_generated = 0
nodes_evaluated = 0

def is_game_over(numbers):
    return len(numbers) == 0


def generate_children(node):
    global nodes_generated

    if node.children:
        return node.children
    
    for num in set(node.numbers):
        next_turn = 1 if node.turn == 2 else 2

        # vienmēr var paņemt
        new_numbers, new_total, new_bank = make_move(
            node.numbers,
            num,
            node.total,
            node.bank,
            "take"
        )
        node.children.append(
            Node(new_numbers, next_turn, new_total, new_bank, f"{num} (take)")
        ) 
        nodes_generated += 1

        # 2 un 4 var arī sadalīt
        if num == 2 or num == 4:
            new_numbers, new_total, new_bank = make_move(
                node.numbers,
                num,
                node.total,
                node.bank,
                "split"
            )
            node.children.append(
                Node(new_numbers, next_turn, new_total, new_bank, f"{num} (split)")
            )
            nodes_generated += 1

    return node.children


def evaluate(node, starter_type):
    global nodes_evaluated
    nodes_evaluated += 1

    if is_game_over(node.numbers):
        if node.total % 2 == 0 and node.bank % 2 == 0:
            return 100 if starter_type == 2 else -100

        if node.total % 2 == 1 and node.bank % 2 == 1:
            return 100 if starter_type == 2 else -100
        
        return 0

    score = 0

    if node.total % 2 == 1:
        score += 10
    if node.bank % 2 == 1:
        score += 10

    if starter_type == 1:
        return score 
    else:
        return -score


def minimax(node, depth, maximizing, starter_type):
    if depth == 0 or is_game_over(node.numbers):
        return evaluate(node, starter_type)

    children = generate_children(node)

    if maximizing:
        best = -float('inf')
        for child in children:
            best = max(best, minimax(child, depth - 1, False, starter_type))
        return best
    else:
        best = float('inf')
        for child in children:
            best = min(best, minimax(child, depth - 1, True, starter_type))
        return best


def alphabeta(node, depth, alpha, beta, maximizing, starter_type):
    if depth == 0 or is_game_over(node.numbers):
        return evaluate(node, starter_type)

    children = generate_children(node)

    if maximizing:
        value = -float('inf')
        for child in children:
            value = max(value, alphabeta(child, depth - 1, alpha, beta, False, starter_type))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for child in children:
            value = min(value, alphabeta(child, depth - 1, alpha, beta, True, starter_type))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value


def find_best_move(numbers, total, bank, algorithm, starter_type, depth):
    global nodes_generated, nodes_evaluated
    nodes_generated = 0
    nodes_evaluated = 0

    start_time = time.perf_counter()

    root = Node(numbers, 2, total, bank)
    children = generate_children(root)

    if not children:
        return None, 0, 0, 0

    best = children[0]
    best_value = -float('inf')

    for child in children:
        if algorithm == "Minimax":
            value = minimax(child, depth - 1, False, starter_type)
        else:
            value = alphabeta(child, depth - 1, -float('inf'), float('inf'), False, starter_type)

        if value > best_value:
            best_value = value
            best = child

    end_time = time.perf_counter()
    duration = end_time - start_time

    return best, nodes_generated, nodes_evaluated, duration
