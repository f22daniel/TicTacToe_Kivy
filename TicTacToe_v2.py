from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.core.window import Window
from functools import partial
import sys

Builder.load_file('TicTacToe_v2.kv')
Window.size = (600, 600)

class Variables:

    def __init__(self, score_player_x=0, score_player_o=0, player_turn='X', player_x_won=False, player_o_won=False):
        self.score_player_x = score_player_x
        self.score_player_o = score_player_o
        self.player_turn = player_turn
        self.player_x_won = player_x_won
        self.player_o_won = player_o_won


variables = Variables()

class GameOverPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if variables.player_x_won:
            self.ids.popup_declare_winner.text = 'Player X won.'
        elif variables.player_o_won:
            self.ids.popup_declare_winner.text = 'Player O won.'

class MyLayout(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(1, 101):
            board_button = BoardButton()
            self.ids[f'button_{i}'] = board_button
            self.ids.playboard.add_widget(board_button)
            board_button.bind(on_release=partial(self.play, f'button_{i}'))

    def reset(self):

        for i in range(1, 101):
            self.ids[f'button_{i}'].text = ''
        variables.player_x_won = False
        variables.player_o_won = False

    def reset_score(self):
        self.reset()
        self.ids.player_x_score.text = '0'
        self.ids.player_o_score.text = '0'

    def play(self, number, state):
        print(f'Button {number} pressed.')

        if self.ids[number].text == '':
            self.ids[number].text = variables.player_turn
            self.check_winner_x(variables.player_turn)
        if variables.player_turn == 'X':
            self.ids[number].color = (0, 0, 1, 1)
            variables.player_turn = 'O'
        elif variables.player_turn == 'O':
            self.ids[number].color = (1, 0, 0, 1)
            variables.player_turn = 'X'

    def declare_winner(self, winner):

        if winner == 'X':
            variables.score_player_x += 1
            self.ids.player_x_score.text = f'{variables.score_player_x}'
        elif winner == 'O':
            variables.score_player_o += 1
            self.ids.player_o_score.text = f'{variables.score_player_o}'
        open_popup = GameOverPopup()
        open_popup.open()
        self.reset()

    def check_winner_x(self, symbol):
        self.check_row(symbol)
        self.check_column(symbol)
        self.check_down(symbol)
        self.check_up(symbol)

    def check_row(self, symbol):
        for n in range(0, 10):
            x = 10*n
            iterator = 0
            for i in range(1, 11):
                if self.ids[f'button_{i+x}'].text == symbol:
                    iterator += 1
                else:
                    iterator = 0
                if iterator == 5:
                    if symbol == 'X':
                        variables.player_x_won = True
                        self.declare_winner(symbol)
                        break
                    elif symbol == 'O':
                        variables.player_o_won = True
                        self.declare_winner(symbol)
                        break

    def check_column(self, symbol):

        for i in range(1, 11):
            iterator = 0
            for n in range(0, 10):
                x = 10*n
                if self.ids[f'button_{x+i}'].text == symbol:
                    iterator += 1
                else:
                    iterator = 0
                if iterator == 5:
                    if symbol == 'X':
                        variables.player_x_won = True
                        self.declare_winner(symbol)
                        break
                    elif symbol == 'O':
                        variables.player_o_won = True
                        self.declare_winner(symbol)
                        break

    def check_down(self, symbol):

        for n in range(0, 11):
            if n in [0, 1, 2, 3, 4, 5]:
                x = 10*n
            else:
                x = n - 5
            iterator = 0
            for i in range(0, 10):
                try:
                    # print(x+1+(11*i))
                    if self.ids[f'button_{x+1+(11*i)}'].text == symbol:
                        iterator += 1
                    else:
                        iterator = 0
                except KeyError:
                    pass
                if iterator == 5:
                    if symbol == 'X':
                        variables.player_x_won = True
                        self.declare_winner(symbol)
                        break
                    elif symbol == 'O':
                        variables.player_o_won = True
                        self.declare_winner(symbol)
                        break

    def check_up(self, symbol):

        for n in range(1, 7):
            iterator = 0
            for i in range(0, 10):
                try:
                    if self.ids[f'button_{(10*n)+(i*9)}'].text == symbol:
                        iterator += 1
                    else:
                        iterator = 0
                except KeyError:
                    pass
                if iterator == 5:
                    if symbol == 'X':
                        variables.player_x_won = True
                        self.declare_winner(symbol)
                        break
                    elif symbol == 'O':
                        variables.player_o_won = True
                        self.declare_winner(symbol)
                        break
        iterator_2 = 0
        for n in range(1, 6):
            iterator = 0
            for i in range(0, (9-iterator_2)):
                try:
                    if self.ids[f'button_{(10-n)+(i*9)}'].text == symbol:
                        iterator += 1
                    else:
                        iterator = 0

                except KeyError:
                    pass
                if iterator == 5:
                    if symbol == 'X':
                        variables.player_x_won = True
                        self.declare_winner(symbol)
                        break
                    elif symbol == 'O':
                        variables.player_o_won = True
                        self.declare_winner(symbol)
                        break
            iterator_2 += 1

    @staticmethod
    def exit_program():
        sys.exit()

class BoardButton(Button):
    pass

class TicTacToeApp(App):
    mainlayout = MyLayout()

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return MyLayout()

if __name__ == '__main__':
    TicTacToeApp().run()
