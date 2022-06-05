import random

import game_2048
import views


def main(game: game_2048.Game, seed=None):
    if seed is not None:
        random.seed(seed)

    # Set slid to True for initial random placement
    slid = True
    while not game.is_game_over():
        # Insert random cell
        if slid:
            game.add_random_val()

        game.display_board()
        cmd = game.get_command()

        slid = False
        if cmd == views.Command.MV_UP:
            slid = game.slide_up()
        elif cmd == views.Command.MV_DOWN:
            slid = game.slide_down()
        elif cmd == views.Command.MV_LEFT:
            slid = game.slide_left()
        elif cmd == views.Command.MV_RIGHT:
            slid = game.slide_right()
        elif cmd == views.Command.EXIT:
            break


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--curses", "-c", action="store_true", help="Use curses display")
    parser.add_argument("--seed", "-s")
    args = parser.parse_args()

    board = game_2048.Board(4, 4)

    if args.curses:
        import curses
        curses.wrapper(lambda scr: main(game_2048.Game(board, views.CursesView(scr, (4, 2), (board.size.col, board.size.row)), 11), args.seed))

    else:
        main(game_2048.Game(board, views.PTUIView((4, 2), (board.size.col, board.size.row)), 11), args.seed)
