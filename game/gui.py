import PySimpleGUI as sg
from game.board import ChessBoard

class ChessGUI(sg.Window):
    def __init__(self, title):
        self.board = ChessBoard()
        self.status_msg = 'None'
        super().__init__(title, self.get_layout())

    def get_layout(self):
        left_column = [[sg.Text('Chess ', auto_size_text=True, key='-STATUS-', font='Default 20')]]
        left_column += self.board.get_layout()
        left_column += [[sg.Button('New Game', size=(8, 1), key='-RESTART-')]]
        left_column += [[sg.Input()]]
        left_column += [[sg.Button('Send move')]]

        right_column = [[sg.Push(), sg.Text('Press any button to navigate', auto_size_text=True, font='Default 20'), sg.Push()],[sg.Push(), sg.Button("up", size=(6, 2), key='-UP-'), sg.Push()], [sg.Button("left", size=(6, 2), key='-LEFT-'), sg.Button("enter" , size=(6, 2), key='-CENTER-'), sg.Button("right" , size=(6, 2), key='-RIGHT-')], [sg.Push(), sg.Button("down", size=(6, 2), key='-DOWN-'), sg.Push()] ]

        layout = [
            [sg.Column(left_column),
            sg.VSeperator(),
            sg.Column(right_column),]
        ]                                                                                                            
        return layout

    def update_status(self):
        msg = f'{"WHITE" if self.board.turn else "BLACK"} to move..'

        if self.board.is_game_over():
            if self.board.is_checkmate():
                winner = 'WHITE' if self.board.outcome().winner else 'BLACK'
                msg = f'CHECKMATE!!! {winner} wins!'
            elif self.board.is_stalemate():
                msg = 'Draw by STALEMATE!'
            elif self.board.is_insufficient_material():
                msg = 'Draw by INSUFFICIENT MATERIAL!'

        self.status_msg = msg
        self['-STATUS-'].update(self.status_msg)

    def update_board(self, event):
        if event == '-RESTART-':
            self.board.reset()
        for rank in self.board.table:
            for tile in rank:
                if tile.key == event:
                    self.board.handle_move(tile)
       

        self.board.update_display()