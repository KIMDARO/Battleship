def initialise_board(size = 10):
    return [[None] * size for _ in range(size)]


def create_battleships(filename = 'battleships.txt'):
    battleships = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                name, size = line.strip().split(":")
                battleships[name] = int(size)
    except FileNotFoundError:
        #The default battleships
        battleships = {
            'Aircraft_Carrier': 5,
            'Battleship': 4,
            'Cruiser': 3,
            'Submarine': 3,
            'Destroyer': 2
        }
    return battleships

def place_battleships(board, ships, algorithm ='simple'):
    import random
    import json
    size = len(board)

    if algorithm == 'simple':
        row = 0
        for name, ship_size in ships.items():
            if row < size and ship_size <= size:
                for col in range(ship_size):
                    board[row][col] = name
                row += 1

    elif algorithm == 'random':
        for name, ship_size in ships.items():
            placed = False
            while not placed:
                orientation = random.choice(['H','V']) # 0: horizontal, 1: vertical
                if orientation == 'H':  # Horizontal placement
                    row = random.randint(0, size - 1)
                    col = random.randint(0, size - ship_size)

                    if all(board[row][col + i] is None for i in range(ship_size)):
                        for i in range(ship_size):
                            board[row][col + i] = name
                        placed = True
                else:  # Vertical placement
                    row = random.randint(0, size - ship_size)
                    col = random.randint(0, size - 1)
                    if all(board[row + i][col] is None for i in range(ship_size)):
                        for i in range(ship_size):
                            board[row + i][col] = name
                        placed = True

    elif algorithm == 'custom':
        try:
            with open('placement.json', 'r') as f:
                placement_data = json.load(f)

            for name, positions in placement_data.items():
                if name in ships:
                    for row, col in positions:
                        if 0 <= row < size and 0 <= col < size:
                            board[row][col] = name
        except FileNotFoundError:
            print("Custom Placement configuration file 'placement.json' not found")
        except json.decoder.JSONDecodeError:
            print("Custom Placement configuration file 'placement.json' is invalid")

    else: print(f'Unknown algorithm: {algorithm}')

    return board

