import chess
from game.gui import ChessGUI
import PySimpleGUI as sg


def main():
    sg.theme('Python')
    sg.set_options(font="Cambria 15")
    # sg.theme_background_color('#262421')

    window = ChessGUI('Chess')

    print(window.board.legal_moves)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        print(values)
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
        if event == "-CENTER-":
             window.update_board(window.board.head_pointer[0])
    
         
        if event == "-LEFT-":
            var = window.board.head_pointer[0]
            if var[0] > 0:
                new_var = (var[0]-1, var[1])
                window.board.head_pointer[0] = new_var
        
            
        if event == "-RIGHT-":
            var = window.board.head_pointer[0]
            if var[0] < 7:
                new_var = (var[0]+1, var[1])
                window.board.head_pointer[0] = new_var

        if event == "-UP-":
            var = window.board.head_pointer[0]
            if var[1] < 7:
                new_var = (var[0], var[1]+1)
                window.board.head_pointer[0] = new_var
            
        if event == "-DOWN-":
            var = window.board.head_pointer[0]
            if var[1] > 0:
                new_var = (var[0], var[1]-1)
                window.board.head_pointer[0] = new_var


        window.update_board(event)
        window.update_status()
        window.refresh()

    window.close()


if __name__ == '__main__':
    main()

