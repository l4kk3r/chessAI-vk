import board, pieces, ai, random
import vk_api
transforming = {"0": "A", "1": "B", "2": "C", "3": "D", "4": "E", "5": "F", "6": "G", "7": "H"}
# Returns a move object based on the users input. Does not check if the move is valid.
def get_user_move(api, uid, move_str):
    #move_str = move_str[0] + str(9 - int(move_str[1])) + move_str[2] + str(9 - int(move_str[3]))
    move_str = move_str.replace(" ", "")
    try:
        xfrom = letter_to_xpos(move_str[0:1])
        yfrom = 8 - int(move_str[1:2]) # The board is drawn "upside down", so flip the y coordinate.
        xto = letter_to_xpos(move_str[2:3])
        yto = 8 - int(move_str[3:4]) # The board is drawn "upside down", so flip the y coordinate.
        return ai.Move(xfrom, yfrom, xto, yto, False)
    except ValueError:
        print("Invalid format. Example: A2 A4")
        return 1 

# Returns a valid move based on the users input.
def get_valid_user_move(board, api, uid, request):
    while True:
        move = get_user_move(api, uid, request)
        valid = False
        possible_moves = board.get_possible_moves(pieces.Piece.WHITE)
        # No possible moves
        if (not possible_moves):
            return 0

        for possible_move in possible_moves:
            if (move.equals(possible_move)):
                move.castling_move = possible_move.castling_move
                valid = True
                break

        if (valid):
            break
        else:
            break
    return move

# Converts a letter (A-H) to the x position on the chess board.
def letter_to_xpos(letter):
    letter = letter.upper()
    if letter == 'A':
        return 0
    if letter == 'B':
        return 1
    if letter == 'C':
        return 2
    if letter == 'D':
        return 3
    if letter == 'E':
        return 4
    if letter == 'F':
        return 5
    if letter == 'G':
        return 6
    if letter == 'H':
        return 7

    raise ValueError("Invalid letter.")

#
# Entry point.
#
def make_move(api, uid, request):
    global board
    move = get_valid_user_move(board, api, uid, request)
    if (move == 0):
        if (board.is_check(pieces.Piece.WHITE)):
            print("Checkmate. Black Wins.")
            
        else:
            print("Stalemate.")
            

    board.perform_move(move)

    ai_move = ai.AI.get_ai_move(board, [])
    if (ai_move == 0):
        if (board.is_check(pieces.Piece.BLACK)):
            print("Checkmate. White wins.")
            
        else:
            print("Stalemate.")
            

    board.perform_move(ai_move)
    chessmove = ai_move.to_string()
    chessmove = chessmove.replace(' ', '').replace(',', '').replace('(', '').replace(')', '').replace('->', '')
    chessmove = transforming[chessmove[0]] + str(8 - int(chessmove[1])) + ' ' + transforming[chessmove[2]] + str(8 - int(chessmove[3]))
    api.messages.send(user_id=uid, message=chessmove, random_id=random.randint(-9999999999, 999999999))

def start_ai():
    global board
    import board
    board = board.Board.new()