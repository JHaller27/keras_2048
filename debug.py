from game_2048 import Game, Board, Position
import views


def main(game: Game):
    board[Position(2, 1)] = 2
    board[Position(2, 2)] = 1
    board[Position(2, 3)] = 1

    def _slide():
        game.slide_down()

    game.display_board()
    game.get_command()

    _slide()
    game.display_board()
    game.get_command()

    _slide()
    game.display_board()
    game.get_command()

    _slide()
    game.display_board()
    game.get_command()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--curses", "-c", action="store_true", help="Use curses display")
    args = parser.parse_args()

    board = Board(4, 4)

    if args.curses:
        import curses
        curses.wrapper(lambda scr: main(Game(board, views.CursesView(scr, (4, 2), (board.size.col, board.size.row)), 11)))

    else:
        main(Game(board, views.PTUIView((4, 2), (board.size.col, board.size.row)), 11))
