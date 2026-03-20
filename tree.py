import time
from main import make_move

class Node:
    def __init__(self, numbers, turn, total, bank, move=None):
        self.numbers = sorted(numbers) # Kārtojam efektivitātei
        self.turn = turn
        self.total = total
        self.bank = bank
        self.move = move
        self.children = [] # Koka struktūras glabāšana
        self.value = None

nodes_evaluated = 0

def generate_children(node):
    children = []
    next_turn = 1 if node.turn == 2 else 2
    
    # Lai izvairītos no liekiem zariem, izmantojam unikālus skaitļus gājienam
    unique_nums = set(node.numbers)
    
    for num in unique_nums:
        # Gājiens: Take
        n1, t1, b1 = make_move(node.numbers, num, node.total, node.bank, "take")
        children.append(Node(n1, next_turn, t1, b1, f"{num} (take)"))
        
        # Gājiens: Split
        if num in [2, 4]:
            n2, t2, b2 = make_move(node.numbers, num, node.total, node.bank, "split")
            children.append(Node(n2, next_turn, t2, b2, f"{num} (split)"))
    return children

def evaluate(node):
    # Heiristiskā funkcija
    # AI parasti ir Player 2, kas tiecas uz Nepāra/Nepāra
    score = 0
    if node.total % 2 != 0: score += 10
    if node.bank % 2 != 0: score += 10
    
    # Ja spēle beigusies, piešķiram lielu vērtību gala rezultātam
    if not node.numbers:
        if node.total % 2 != 0 and node.bank % 2 != 0: return 100 # AI Uzvara
        if node.total % 2 == 0 and node.bank % 2 == 0: return -100 # AI Zaudējums
        return 0
    return score

def minimax(node, depth, maximizing):
    global nodes_evaluated
    nodes_evaluated += 1
    
    if depth == 0 or not node.numbers:
        node.value = evaluate(node)
        return node.value

    node.children = generate_children(node)
    if maximizing:
        max_val = -float('inf')
        for child in node.children:
            val = minimax(child, depth - 1, False)
            max_val = max(max_val, val)
        node.value = max_val
        return max_val
    else:
        min_val = float('inf')
        for child in node.children:
            val = minimax(child, depth - 1, True)
            min_val = min(min_val, val)
        node.value = min_val
        return min_val

def alphabeta(node, depth, alpha, beta, maximizing):
    global nodes_evaluated
    nodes_evaluated += 1
    
    if depth == 0 or not node.numbers:
        node.value = evaluate(node)
        return node.value

    node.children = generate_children(node)
    if maximizing:
        val = -float('inf')
        for child in node.children:
            val = max(val, alphabeta(child, depth - 1, alpha, beta, False))
            alpha = max(alpha, val)
            if beta <= alpha: break # Atzarošana
        node.value = val
        return val
    else:
        val = float('inf')
        for child in node.children:
            val = min(val, alphabeta(child, depth - 1, alpha, beta, True))
            beta = min(beta, val)
            if beta <= alpha: break
        node.value = val
        return val

def find_best_move(numbers, total, bank, algorithm, depth=3):
    global nodes_evaluated
    nodes_evaluated = 0
    start_time = time.perf_counter()
    
    root = Node(numbers, 2, total, bank)
    
    if algorithm == "Minimax":
        best_score = minimax(root, depth, True)
    else:
        best_score = alphabeta(root, depth, -float('inf'), float('inf'), True)
        
    duration = time.perf_counter() - start_time
    
    # Atrod bērnu ar labāko vērtību
    best_move_node = None
    if root.children:
        # Atlasām bērnus, kuru vērtība sakrīt ar aprēķināto labāko
        candidates = [c for c in root.children if c.value == best_score]
        best_move_node = candidates[0] if candidates else root.children[0]

    return best_move_node, nodes_evaluated, duration