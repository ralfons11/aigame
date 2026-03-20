from main import make_move


class Node:
    def __init__(self, numbers, turn, total, bank, move=None):
        self.numbers = numbers
        self.turn = turn
        self.total = total
        self.bank = bank
        self.move = move


def is_game_over(numbers):
    return len(numbers) == 0


def generate_children(node):
    children = []

    for num in node.numbers:
        next_turn = 1 if node.turn == 2 else 2

        # vienmēr var paņemt
        new_numbers, new_total, new_bank = make_move(
            node.numbers,
            num,
            node.total,
            node.bank,
            "take"
        )
        children.append(
            Node(new_numbers, next_turn, new_total, new_bank, f"{num} (take)")
        )

        # 2 un 4 var arī sadalīt
        if num == 2 or num == 4:
            new_numbers, new_total, new_bank = make_move(
                node.numbers,
                num,
                node.total,
                node.bank,
                "split"
            )
            children.append(
                Node(new_numbers, next_turn, new_total, new_bank, f"{num} (split)")
            )

    return children


def evaluate(node):
    score = 0

    if node.total % 2 == 1:
        score += 1
    else:
        score -= 1

    if node.bank % 2 == 1:
        score += 1
    else:
        score -= 1

    # AI ir spēlētājs 2
    if node.turn == 1:
        score = -score

    return score


def minimax(node, depth, maximizing):
    if depth == 0 or is_game_over(node.numbers):
        return evaluate(node)

    children = generate_children(node)

    if maximizing:
        best = -999
        for child in children:
            best = max(best, minimax(child, depth - 1, False))
        return best
    else:
        best = 999
        for child in children:
            best = min(best, minimax(child, depth - 1, True))
        return best


def alphabeta(node, depth, alpha, beta, maximizing):
    if depth == 0 or is_game_over(node.numbers):
        return evaluate(node)

    children = generate_children(node)

    if maximizing:
        value = -999
        for child in children:
            value = max(value, alphabeta(child, depth - 1, alpha, beta, False))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = 999
        for child in children:
            value = min(value, alphabeta(child, depth - 1, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value


def find_best_move(numbers, total, bank, algorithm):
    root = Node(numbers, 2, total, bank)
    children = generate_children(root)

    if not children:
        return None

    best = children[0]
    best_value = -999

    for child in children:
        if algorithm == "Minimax":
            value = minimax(child, 3, False)
        else:
            value = alphabeta(child, 3, -999, 999, False)

        if value > best_value:
            best_value = value
            best = child

    return best