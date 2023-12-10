import chess
from game.gui import ChessGUI
import PySimpleGUI as sg


def main():
    sg.theme('Python')
    sg.set_options(font="Cambria 15")

    window = ChessGUI('Chess')

    print(window.board.legal_moves)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        # Move from input
        if event == "Send move":
            try: 
                move = chess.Move.from_uci(values[0])
                if move in window.board.legal_moves:
                    window.board.push(move)
                else:
                    print("Hell nah stop trying to cheat dude")

            except chess.InvalidMoveError:
                print("This is an invalid move")
            
            except ValueError:
                print("This is not a move")
                
        window.update_board(event)
        window.update_status()
        window.refresh()

    window.close()


if __name__ == '__main__':
    main()
