from main import Board, Position
import debug_views


def main(view: debug_views.IView, board: Board):
    board[Position(2, 2)] = 1
    view.draw(board)

    board.slide_up()
    view.draw(board)

    board[Position(2, 1)] = 1
    view.draw(board)

    board.slide_up()
    view.draw(board)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--curses", "-c", action="store_true", help="Use curses display")
    args = parser.parse_args()

    board = Board(4, 4)

    if args.curses:
        import curses
        curses.wrapper(lambda scr: main(debug_views.CursesView(scr, (4, 2), (board.size.col, board.size.row)), board))

    else:
        main(debug_views.PTUIView((4, 2), (board.size.col, board.size.row)), board)
