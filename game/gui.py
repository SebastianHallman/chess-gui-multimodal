import PySimpleGUI as sg
from game.board import ChessBoard

class ChessGUI(sg.Window):
    def __init__(self, title):
        self.board = ChessBoard()
        self.status_msg = 'None'
        super().__init__(title, self.get_layout())

    def get_layout(self):
        layout = [[sg.Text('Chess ', auto_size_text=True,
                           key='-STATUS-', font='Default 20')]]
        layout += self.board.get_layout()
        layout += [[sg.Button('New Game', size=(8, 1), key='-RESTART-')]]
        layout += [[sg.Input()]]
        
        layout += [[sg.Button('Send move')]]
        layout += [[sg.Button('Record Audio', size=(10, 1), key='-RECORD-' )]]  # Button for recording audio
        layout += [[sg.Button('Perform move', size=(10, 1))]]  # Button for replaying audio
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

        if event == '-RECORD-':
            if self['-RECORD-'].get_text() == 'Record Audio':
                self['-RECORD-'].update('Recording...')
            # If the button text is 'Recording...', change it back to 'Record Audio'
            else:
                self['-RECORD-'].update('Record Audio') 
                    

        self.board.update_display()