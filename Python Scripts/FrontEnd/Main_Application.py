from nicegui import ui
import FrontEnd.Charts as chart
import FrontEnd.Record_Prob as a_prob

class Main_Application:
    def __init__(self, background_color, line_color, given_color, pos_percent, neg_percent, neutral_percent):
        self._background_color = background_color
        self._line_color = line_color
        self._given_color = given_color
        self._pos_percent = pos_percent
        self._neg_percent = neg_percent
        self._neutral_percent = neutral_percent

    def show_comments(self):
        # start part
        with ui.card().classes('w-[700px] h-[475px] text-white').style('border: 2.5px solid #7b5e7b; background-color: #170f18; border-radius: 20px;'): #NOTE background-color: #271727
            ui.label("Sentimental Comments From 2013 and 2014").style("font-size: 25px; color: #c495ad; font-weight: bold;").classes('font-bold italic justify-center')
            ui.separator().style("background-color: #7b5e7b;")
            chart_obj = chart.Charts('#b39db7', '#9083a3', '#7e5479')
            chart_obj.make_highlight_charts(self._background_color, self._line_color, self._given_color)

    def set_line_color(self, new_line_color):
        self._line_color = new_line_color

    def set_given_color(self, new_given_color):
        self._given_color = new_given_color

    def show_star_review(self):
        # start part
        with ui.card().classes('w-[700px] h-[475px] no-border no-shadow').style('background-color: #170f18; border-radius: 20px;'): #NOTE #261b2a # border border: 2.5px solid #57435e;
            with ui.column().classes('w-full justify-center'):
                with ui.row().classes('items-center justify-between'): # .classes('justify-center')
                    ui.label("Overall Star Rating: 3.5").style('font-weight: bold; color: #c3b6fd; font-size: 25px;').classes('italic mt-[-10px]')
                    ui.rating(value=3.5, max=5,icon_selected='star',color="violet-300", size="40px").classes('mt-[-15px]') # .classes('w-full justify-center') # size='48px'
                chart_obj = chart.Charts('#9086ba', '#868bba', '#86a0ba')
                self.set_line_color('#c3b6fd')
                self.set_given_color('#7b6582')
                chart_obj.make_highlight_charts(self._background_color, self._line_color, self._given_color)

    def show_record_sentiment_prob(self):
        # start part 
        with ui.card().classes('w-full h-[250px]').style('border: 2.5px solid #88607c; background-color: #170f18; border-radius: 20px;'): #NOTE background #291624
            with ui.column().classes('w-full'):
                with ui.row().classes('mt-[-10px]'):
                    ui.label("This is the veidct box").style('color: #606688; font-size: 20px;').classes('mt-[10px]')
                    reaction_obj = a_prob.Record_Prob('#886087', self._pos_percent , self._neg_percent, self._neutral_percent) # mood_color, pos_percent, neg_percent, neutral_percent
                    reaction_obj.display_satisfied()
                    reaction_obj.set_mood_color('#776088')
                    reaction_obj.display_neutral()
                    reaction_obj.set_mood_color('#686088')
                    reaction_obj.display_dissatisfied()
                with ui.row().classes('w-full'):
                    with ui.scroll_area().classes('h-40 border').style(f'background-color: {self._background_color}; border-radius: 20px; border: 2px solid #47243e; font-size: 20px;'): # #291624 #47243e #6e4162
                        ui.label('I scroll. I scroll. I scroll. I scroll. I scroll. I scroll. I scroll. I scroll. I scroll.' * 20).style("color: #8680ad;")
        # end part

    def build_app(self):
        ui.query('body').style(f'background-color: {self._background_color};')
        with ui.row().classes('w-full justify-between items-center'):
            ui.label("Amozon Customer Sentimental Analysis on Reviews and Comments").style("font-weight: bold; font-size: 20px; color: #8a627e;")
            with ui.button(color='#6e2c5d'):
                with ui.row():
                    ui.icon('done').classes('bg-[#b5539c] p-1 rounded-full').style('color: #6e2c5d')
                    ui.label('transfer status').classes('mt-[5px]').style('color: #b5539c')
        ui.separator().style("background-color: #8a627e;")
        with ui.column():
            with ui.row().classes('w-full'):
                self.show_comments()
                self.show_star_review() 
        self.show_record_sentiment_prob()
        ui.run(port=5434)
        