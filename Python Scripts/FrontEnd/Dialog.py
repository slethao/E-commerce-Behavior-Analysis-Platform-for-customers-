from nicegui import ui

class Dialog():
    def __init__(self, user, pos_percent, neg_percent, neutral_percent):
        self._user = user
        self._pos_percent = pos_percent
        self._neg_percent = neg_percent
        self._neutral_percent = neutral_percent

    def create_dialog(self):
        with ui.dialog() as more_info:
            with ui.column():
                ui.restructured_text(f"**{self._user}'s Comment**").style('color: white; font-size: 35px;')
                ui.restructured_text(f"**Positive:** {self._pos_percent}").style('color: #886087; font-size: 20px;')
                ui.restructured_text(f"**Negative:** {self._neg_percent}").style('color: #686088; font-size: 20px;')
                ui.restructured_text(f"**Neutral:** {self._neutral_percent}").style('color: #776088; font-size: 20px;')
        return more_info