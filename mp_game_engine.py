from components import initialise_board, create_battleships, place_battleships
from random import randint
from game_engine import cli_coordinates_input, attack

#Creating the Player dictionary
global players
players = {}

def all_sunk_ships(ships):
    return all(size == 0 for size in ships.values())

#Generating the AI attack coordinates
def generate_attack(board_size, previous_hits = None):

    """
    Generates the AI's attack coordinates.
    If any previous hit exists, it will attempt to target neighbouring cells logically,
    Otherwise it will choose a random valid coordinate
    """
    if previous_hits:
        row, col = previous_hits.pop(0)
        neighbors = [
            (row - 1, col), (row + 1, col),
            (row, col- 1 ), (row, col + 1)
        ]
        valid_neighbors = [
            (r,c) for r, c in neighbors if 0 <= r < board_size and 0 <= c < board_size
        ]
        if valid_neighbors:
            return valid_neighbors[randint(0, len(valid_neighbors) - 1)]


    #Generates a random attack coordinate when there's no previous hit
    return randint(0,board_size-1), randint(0,board_size-1)

def display_board_ascii(board):
    print("  " + " ".join(map(str, range(len(board)))))
    for idx, row in enumerate(board):
        print(f"{idx} " + " ".join( 'X' if cell == 'X' else 'O' if cell == 'O' else '_' for cell in row
        ))

#AI Opponent Game Loop
def ai_opponent_game_loop():
    print('Welcome to Battleship with an AI opponent!')

    global players

    #Initializes the players with boards and battleships
    players = {
        'User':
            {'board': initialise_board(),
             'ships':create_battleships()
             },
        'AI':
            {'board': initialise_board(),
             'ships':create_battleships()}
    }

    #Placing the ships
    players['User']['board'] = place_battleships(
        players['User']['board'], players['User']['ships'], algorithm = 'custom'
    )
    players['AI']['board'] = place_battleships(players['AI']['board'], players['AI']['ships'], algorithm = 'random'
    )

    board_size = len(players['User']['board'])
    ai_previous_hits = []

    while not all_sunk_ships(players['User']['ships']) and not all_sunk_ships(players['AI']['ships']):
        print("Your Turn:")
        print("AI'S BOARD")
        display_board_ascii(players['AI']['board'])
        user_coordinates = cli_coordinates_input()
        user_hit = attack(user_coordinates, players['AI']['board'], players['AI']['ships'])
        print(f"{"That's a Hit!" if user_hit else 'Oof you missed :P'} at {user_coordinates}")

        if all_sunk_ships(players['AI']['ships']):
            print(f"Congratulations! You've won!")
            break

        #The AI's Turn
        print("AI's Turn")
        print('YOUR BOARD')
        ai_coordinates = generate_attack(board_size, ai_previous_hits)
        ai_hit = attack(ai_coordinates, players['User']['board'], players['User']['ships'])
        print(f"AI attacked {ai_coordinates} and {"That's a Hit!" if ai_hit else 'They missed! :P'}")
        display_board_ascii(players['User']['board'])

        if all_sunk_ships(players['User']['ships']):
            print(f"Game Over! The AI wins")
            break

    print('Thanks for playing!')

if __name__ == '__main__':
    ai_opponent_game_loop()