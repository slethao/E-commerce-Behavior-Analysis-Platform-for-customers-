from nicegui import ui

"""
This class is for create a dialog.
"""
class Dialog():
    __slot__ = ('user', 'pos_percent', 'neg_percent', 'neutral_percent')

    def __init__(self, user: str, pos_percent: float, neg_percent: float, neutral_percent: float):
        """
        Constructor for the class 'Dialog'

        Parameters:
            pos_percent (float): the vale to represent the ratio of how positive a reocrd is when clicked on
            neg_percent (float): the vale to represent the ratio of how negative a reocrd is when clicked on
            neutral_percent (flaot): the vale to represent the ratio of how neutral a reocrd is when clicked on
        """
        self._user = user
        self._pos_percent = pos_percent
        self._neg_percent = neg_percent
        self._neutral_percent = neutral_percent

    def create_dialog(self) -> ui.dialog:
        """
        This meethod is to create the dialog even handler for each record
        (this returns a dialog)
            Parameters:
                None
        """
        with ui.dialog() as more_info:
            with ui.column():
                ui.restructured_text(f"**{self._user}'s Comment**").style('color: white; font-size: 35px;')
                ui.restructured_text(f"**Positive:** {self._pos_percent}").style('color: #886087; font-size: 20px;')
                ui.restructured_text(f"**Negative:** {self._neg_percent}").style('color: #686088; font-size: 20px;')
                ui.restructured_text(f"**Neutral:** {self._neutral_percent}").style('color: #776088; font-size: 20px;')
        return more_info