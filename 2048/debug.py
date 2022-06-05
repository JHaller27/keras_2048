from board import Board, Position
import views


def main(view: views.IView, board: Board):
    pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--curses", "-c", action="store_true", help="Use curses display")
    args = parser.parse_args()

    board = Board(4, 4)

    if args.curses:
        import curses
        curses.wrapper(lambda scr: main(views.CursesView(scr, (4, 2), (board.size.col, board.size.row)), board, args.seed))

    else:
        main(views.PTUIView((4, 2), (board.size.col, board.size.row)), board, args.seed)
