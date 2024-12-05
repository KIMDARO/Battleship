from flask import Flask, render_template, request, jsonify

from components import initialise_board, create_battleships, place_battleships
from mp_game_engine import generate_attack, attack, all_sunk_ships
import logging
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

#Adding the Global Variables for the game state
players = {}
board_size = 10
ai_previous_hit = []

@app.route('/placement', methods=['GET', 'POST'])
def placement_interface():
    """
    This handles the ship placements for both the user and the AI.
    - GET request: Serves the placement sage to the user
    - POST request: Will process the ship placement data from the User.
    """
    global players

    if request.method == 'GET':
        #Generates and sends the initial placement page to the user
        ships = create_battleships()
        return render_template('placement.html', ships=ships, board_size=board_size)
    elif request.method == 'POST':
        try:
            #Parsing JSON data from the POST request
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Invalid JSON data'}), 400


            #Initializing the player's and AI's boards and ships
            players['User'] = {
                'board': initialise_board(board_size),
                'ships': create_battleships()
            }
            players['AI'] = {
                'board': initialise_board(board_size),
                'ships': create_battleships()
            }

            #Validation and placing each ship according to the provided data
            for ship, placements in data.items():
                try:
                    x, y = map(int, (placements[0], placements[1]))
                    orientation = placements[2].lower()
                except (IndexError, ValueError):
                    return jsonify({'error': 'Invalid ship placement'}), 400

                ship_length = players['User']['ships'][ship]


                #Checking the placement validity based on orientation and board numbers
                if orientation == 'h':
                    if x + ship_length <= board_size:
                        for i in range(ship_length):
                            players['User']['board'][y][x + i] = ship
                    else:
                        return jsonify({'error': 'Ship placement out of bounds'}), 400

                elif orientation == 'v':
                    if y + ship_length <= board_size:
                        for i in range(ship_length):
                           players['User']['board'][y + i][x] = ship
                    else:
                        return jsonify({'error': 'Ship placement out of bounds'}), 400

            #lacing the AI's ships using the Random algorithm
            place_battleships(players['AI']['board'], players['AI']['ships'], algorithm='random')

            #Testing out the current game state for debugging proposes
            logging.debug('Current state of players: %s', players)  # Debugging print statement
            return jsonify({'status': 'Placement received and processed'}), 200

        except (TypeError, ValueError):
            return jsonify({'error': 'Invalid data format'}), 400


@app.route('/', methods=['GET'])
def main():
    """
    This serves as the main page with the initial game board for the user.
    It also initializes the game state if it hasn't been set up yet.
    """
    global players

    #Initializing the game state if it hasn't been set up
    if 'User' not in players or 'board' not in players.get('User',{}):
        players['User'] = {
            'board': initialise_board(board_size),
            'ships': create_battleships()
                           }
        players['AI'] = {
            'board': initialise_board(board_size),
            'ships': create_battleships()
                         }

        #Placing the AI's ships randomly

        place_battleships(players['AI']['board'], players['AI']['ships'], algorithm='random')
        logging.debug('Initialized state of players: %s', players)

    player_board = players['User']['board']#Gets the updated board of the User
    return render_template('main.html', player_board=player_board)#This with render the current state of the user's board

@app.route('/attack', methods=['GET'])
def process_attack():
    """
    This will handle attacks from the user and process the responses from the AI.
    :return:
    -Checks if the coordinates are valid.
    - Processes the user's attack and returns the result
    -Will generate the Ai's attack and check if it wins
    """
    global players, ai_previous_hit

    try:
        x = int(request.args.get('x', -1))
        y = int(request.args.get('y', -1))

        if x < 0 or x >= board_size or y < 0 or y >= board_size:
            return jsonify({'error': 'Invalid attack coordinates:'}), 400

        #User's move
        user_hit = attack((y, x), players['AI']['board'], players['AI']['ships'])
        user_miss = 'Oof you missed :/' if not user_hit else 'Great shot! You hit a ship!'

        if user_hit:
            players['AI']['board'][y][x] = 'X'
        else:
            players['AI']['board'][y][x] = 'O'

        if all_sunk_ships(players['AI']['ships']):#Checking if the user won
            return jsonify({'User attack':
                                {"coordinates": (x, y),
                                 "hit": user_hit, 'miss':user_miss},
                            'finished': "Congratulations! YOU WON! SO COOL!"
                            })

        # AI's moves
        ai_coordinates = generate_attack(board_size, ai_previous_hit)
        ai_hit = attack(ai_coordinates, players['User']['board'], players['User']['ships'])
        ai_miss = 'The AI missed!' if not ai_hit else "You've been hit!"


        if ai_hit:
            ai_previous_hit.append(ai_coordinates)
            players['User']['board'][ai_coordinates[0]][ai_coordinates[1]]= 'X'
        else:
            players['User']['board'][ai_coordinates[0]][ai_coordinates[1]] = 'O'

        # Checking if the AI won
        if all_sunk_ships(players['User']['ships']):
            return jsonify({'User attack':
                                {"coordinates": (x, y),
                                 "hit": user_hit, 'miss':user_miss},
                           "AI attack": {'coordinates': ai_coordinates,
                                         'hit': ai_hit},'miss':ai_miss,
                           'finished': "Sorry you lost :<"})



        return jsonify({
            'hit': user_hit,
            'AI Turn': ai_coordinates
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()