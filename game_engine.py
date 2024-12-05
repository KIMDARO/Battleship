from components import initialise_board, create_battleships, place_battleships


#Attack function
def attack(coordinates, board, battleships):
    row, col = coordinates

    if not (0 <= row < len(board)and 0 <= col < len(board[0])):
        print('Invalid coordinates!')
        return False


    if board[row][col] and board[row][col] not in {'X', 'O'}:
        ship_name = board[row][col]
        board[row][col] = 'X'
        battleships[ship_name] -= 1
        if battleships[ship_name] == 0:
            print(f"You've sunken the {ship_name}")
        return True
    elif board[row][col] == 'X' or board[row][col] == 'O':
        print("You've already attacked this spot!")
        return False
    else:
        board[row][col] = 'O'#Marks as a miss
        print("That's a miss")
        return False
#Command-line input for coordinates
def cli_coordinates_input():
    while True:
        try:
            coordinates = input("Enter coordinates(row,column): ")
            row, col = map(int, coordinates.split(","))
            return (row, col)
        except ValueError:
            print("Invalid coordinates. Please enter coordinates in the format 'row, column")

def display_board(board):
    print("\n".join(" ".join(cell if cell in {'X', 'O'} else '.' for cell in row) for row in board))

#Simple game loop
def simple_game_loop():#This should run a simple text-based game loop
    print('Welcome to Battleship!')



    board = initialise_board(size = 10)
    battleships = create_battleships()
    board = place_battleships(board, battleships, algorithm='simple')

    while True:
        display_board(board)
        coordinates = cli_coordinates_input()
        hit = attack(coordinates, board, battleships)

        if all(size == 0 for size in battleships.values()):
            print('Congratulations! You sunk all the ships!')
            break

        if hit:
            print(f"Hit at {coordinates}!")

        else: print(f" You missed!")

    print('Game Over! Thanks for playing!')
if __name__ == '__main__':
    simple_game_loop()