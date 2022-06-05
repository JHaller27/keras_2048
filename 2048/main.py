import random

from board import Board, Position
import views



def main(view: views.IView, board: Board, seed = None):
    if seed is not None:
        random.seed(seed)

    # Set slid to True for initial random placement
    slid = True
    while board.get_max_value() < 11:
        # Insert random cell
        if slid:
            empty_pos = random.choice(board.get_empty_positions())
            val = random.choices([1, 2], weights=[0.9, 0.1], k=1)[0]
            board[empty_pos] = val

            # Reset slid
            slid = False

        view.draw(board)
        cmd = view.get_command()

        slid = False
        if cmd == views.Command.MV_UP:
            slid = board.slide_up()
        elif cmd == views.Command.MV_DOWN:
            slid = board.slide_down()
        elif cmd == views.Command.MV_LEFT:
            slid = board.slide_left()
        elif cmd == views.Command.MV_RIGHT:
            slid = board.slide_right()
        elif cmd == views.Command.EXIT:
            break



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--curses", "-c", action="store_true", help="Use curses display")
    parser.add_argument("--seed", "-s")
    args = parser.parse_args()

    board = Board(4, 4)

    if args.curses:
        import curses
        curses.wrapper(lambda scr: main(views.CursesView(scr, (4, 2), (board.size.col, board.size.row)), board, args.seed))

    else:
        main(views.PTUIView((4, 2), (board.size.col, board.size.row)), board, args.seed)
