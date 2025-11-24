import math
import time

class JogoDaVelha:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None 

    def print_board(self):
        print("\n")
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
        print("\n")

    @staticmethod
    def print_board_nums():
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind*3 : (row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True

        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False

class NPC:
    def __init__(self, letter):
        self.letter = letter
        self.human_letter = 'X' if letter == 'O' else 'O'

    def get_move(self, game):
        print(f"NPC ({self.letter}) está calculando (Minimax)...")
        
        if len(game.available_moves()) == 9:
            square = 4 
        else:
            square = self.minimax(game, self.letter)['position']
        
        print(f"NPC escolheu a posição: {square}")
        return square
    
    def minimax(self, state, player):
        max_player = self.letter
        opponent = 'O' if player == 'X' else 'X'

        if state.current_winner == max_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1)}
        elif state.current_winner == opponent:
            return {'position': None, 'score': -1 * (state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)

            sim_score = self.minimax(state, 'O' if player == 'X' else 'X')

            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best

def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()

    letter = 'X'
    
    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            valid_square = False
            while not valid_square:
                try:
                    square = int(input(f'Sua vez ({letter}). Escolha (0-8): '))
                    if square not in game.available_moves():
                        raise ValueError
                    valid_square = True
                except ValueError:
                    print("Jogada inválida. Tente novamente.")

        if game.make_move(square, letter):
            if print_game:
                print(f'{letter} fez uma jogada no quadrado {square}')
                game.print_board()
                print('') 

            if game.current_winner:
                if print_game:
                    print(f'{letter} venceu!')
                return letter 

            letter = 'O' if letter == 'X' else 'X'
        
        time.sleep(0.8)

    if print_game:
        print('Empate!')

if __name__ == '__main__':
    x_player = 'Human'
    o_player = NPC('O')
    t = JogoDaVelha()
    play(t, x_player, o_player, print_game=True)