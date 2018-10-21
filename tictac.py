# TicTacToe Two 7/23/2018 by Alleluid
from dataclasses import dataclass
import random


class InvalidMoveError(ValueError):
    pass


class TakenMoveError(InvalidMoveError):
    pass


class InvalidBoardError(ValueError):
    pass


class TicTac:
    ref_board = [i + 1 for i in range(9)]

    def __init__(self):
        # self.play_board = list(self.ref_board)
        self.play_board = [self.Globals.FILL] * 9
        self.player = True  # True = X, False = O
        self.is_ai_game = True

    def ask_if_ai_game(self):
        print("Would you like to play against AI?")
        resp = input("[Y/n]> ").lower()
        if resp == 'y' or not resp:
            self.is_ai_game = True
        elif resp == 'n':
            self.is_ai_game = False
        else:
            self.ask_if_ai_game()

    def reset_board(self):
        self.play_board = list(self.ref_board)

    def display_board(self, board="both"):
        if board == "both":
            p, r = self.play_board, self.ref_board
            print(" Play        Ref")
            for i in (0, 3, 6):
                print(f"|{p[i]}|{p[i+1]}|{p[i+2]}|    |{r[i]}|{r[i+1]}|{r[i+2]}|")

        elif isinstance(board, list):
            for i, s in enumerate(board):
                print(f"|{s}", end='')
                if (i + 1) % 3 == 0:
                    print('|')
        else:
            raise InvalidBoardError(f"Not a list obj: {board}")

    @dataclass
    class Globals:
        HELP_STR1: str = "Type a number to make a move.\nFormat: [1-9]"
        HELP_INVALID: str = "Location already taken."
        P1_CHR: str = 'X'
        P2_CHR: str = 'O'
        FILL: str = '~'

    def make_move(self, move_int, is_ai=False):
        # Move has to be convertible to an int
        try:
            move_int = int(move_int)
        except ValueError as err:
            print(type(err))
            raise InvalidMoveError(err)

        # and between 1-9
        if move_int not in range(1, 10):
            raise InvalidMoveError(f"Move must be from 1 to 9, was: {move_int}")

        # and not already taken.
        move_chr = self.play_board[move_int - 1]
        if move_chr in (self.Globals.P1_CHR, self.Globals.P2_CHR):
            raise TakenMoveError(f"Coordinate already taken by '{move_chr}' at {move_int}")

        if self.player and not is_ai:
            set_char = self.Globals.P1_CHR
        else:
            set_char = self.Globals.P2_CHR

        self.play_board[move_int - 1] = set_char

    def ai_move(self):
        attempts = 0
        while attempts < 9:
            try:
                self.make_move(random.randint(1, 9), is_ai=True)
            except InvalidMoveError as err:
                if isinstance(err, TakenMoveError):
                    attempts += 1
                    continue
                else:
                    raise err
            break

    def check_win_state(self):
        win_states = (
            # Rows
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            # Cols
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            # Diagonals
            [0, 4, 8],
            [2, 4, 6]
        )
        p = self.play_board
        for lst in win_states:
            play_0, play_1, play_2 = p[lst[0]], p[lst[1]], p[lst[2]]
            if play_0 == play_1 == play_2 and play_0 != self.Globals.FILL:
                return play_0
            # Checks if there is any space left
            elif self.Globals.FILL not in self.play_board:
                return self.Globals.FILL


def game_loop():
    running = True
    while running:
        ttt = TicTac()
        ai_choice = input("Play against AI? [Y/n/q] ").lower()
        # If there was a choice, and it was Y.
        if ai_choice and ai_choice[0] == 'n':
            ttt.is_ai_game = False
        elif ai_choice == 'q':
            running = False
            break

        print(TicTac.Globals.HELP_STR1)
        # noinspection PyTypeChecker
        ttt.display_board(board=TicTac.ref_board)
        while True:
            user_input = input("> ")

            try:
                ttt.make_move(user_input)
            except InvalidMoveError:
                print(TicTac.Globals.HELP_INVALID)
                continue

            is_win_chr = ttt.check_win_state()
            if is_win_chr:
                ttt.display_board()
                if is_win_chr == ttt.Globals.FILL:
                    print("It's a tie!")
                    break
                print(f"{is_win_chr} wins!")
                break

            if not ttt.is_ai_game:
                ttt.player = not ttt.player
            else:
                ttt.ai_move()

            ttt.display_board()



if __name__ == '__main__':
    game_loop()
