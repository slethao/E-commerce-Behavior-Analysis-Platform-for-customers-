from nicegui import ui

class Record_Prob:
    def __init__(self, mood_color, pos_percent, neg_percent, neutral_percent):
        self._mood_color = mood_color
        self._pos_percent = pos_percent
        self._neg_percent = neg_percent
        self._neutral_percent = neutral_percent

    def set_mood_color(self, new_mood):
        self._mood_color = new_mood

    def display_satisfied(self):
        with ui.row():
            ui.icon('sentiment_satisfied_alt', size='xl', color=self._mood_color)
            ui.label(f"{self._pos_percent}%").style(f'color: {self._mood_color}; font-size: 20px;').classes('mt-[10px]')

    def display_neutral(self):
        with ui.row():
            ui.icon('sentiment_neutral', size='xl', color=self._mood_color)
            ui.label(f'{self._neutral_percent}%').style(f'color: {self._mood_color}; font-size: 20px;').classes('mt-[10px]')

    def display_dissatisfied(self):
        with ui.row():
            ui.icon('sentiment_dissatisfied', size='xl', color=self._mood_color)
            ui.label(f"{self._neg_percent}%").style(f'color: {self._mood_color}; font-size: 20px;').classes('mt-[10px]')