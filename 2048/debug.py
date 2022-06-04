from main import Board, Position
import debug_views
import random


def main(view: debug_views.IView, board: Board, seed = None):
    board[Position(2, 2)] = 1

    if seed is not None:
        random.seed(seed)

    while board.get_max_value() < 11:
        view.draw(board)
        cmd = view.get_command()

        if cmd == debug_views.Command.MV_UP:
            board.slide_up()
        elif cmd == debug_views.Command.MV_DOWN:
            board.slide_down()
        elif cmd == debug_views.Command.MV_LEFT:
            board.slide_left()
        elif cmd == debug_views.Command.MV_RIGHT:
            board.slide_right()
        elif cmd == debug_views.Command.EXIT:
            break

        # Insert random cell
        empty_pos = random.choice(board.get_empty_positions())
        val = random.choices([1, 2], weights=[0.9, 0.1], k=1)[0]
        board[empty_pos] = val



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--curses", "-c", action="store_true", help="Use curses display")
    parser.add_argument("--seed", "-s")
    args = parser.parse_args()

    board = Board(4, 4)

    if args.curses:
        import curses
        curses.wrapper(lambda scr: main(debug_views.CursesView(scr, (4, 2), (board.size.col, board.size.row)), board, args.seed))

    else:
        main(debug_views.PTUIView((4, 2), (board.size.col, board.size.row)), board, args.seed)
