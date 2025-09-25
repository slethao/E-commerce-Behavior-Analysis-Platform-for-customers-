from nicegui import ui
import FrontEnd.Charts as chart
import FrontEnd.Dialog as dia
class Main_Application:
    def __init__(self, background_color, line_color, given_color, pos_percent, neg_percent, neutral_percent):
        self._background_color = background_color
        self._line_color = line_color
        self._given_color = given_color
        self._pos_percent = pos_percent
        self._neg_percent = neg_percent
        self._neutral_percent = neutral_percent
        self._button_trigger = False
        self._change_content = "this works"
        self.toggle_state = True
        self.options_on = {True: 'ON'}
        self.options_off = {False: 'OFF'}

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

    def show_record_sentiment_prob(self, content, classify_tool):
        # start part 
        with ui.card().classes('w-full h-[250px]').style('border: 2.5px solid #88607c; background-color: #170f18; border-radius: 20px;'): #NOTE background #291624
            with ui.column().classes('w-full'):
                with ui.row().classes('mt-[-10px]'):
                    ui.label("This is the veidct box").style('color: #606688; font-size: 20px;').classes('mt-[10px]')
                with ui.row().classes('w-full'):
                    with ui.scroll_area().classes('h-40 border').style('border-radius: 20px; border: 2px solid #47243e; font-size: 20px;'): 
                        for i in range(len(content['reviewerName'])): # content['reviewerName'] # content['reviewText']
                            review_txt = content['reviewText'][i]
                            name = content['reviewerName'][i]
                            overall_prob = classify_tool.prob_classify(review_txt)
                            pos_prob = round(overall_prob.prob("pos") , 2)
                            neutral_prob = round(overall_prob.prob("neutral") , 2)
                            neg_prob = round(overall_prob.prob("neg") , 2)
                            dialog_obj = dia.Dialog(name, pos_prob, neg_prob, neutral_prob)
                            a_dialog = dialog_obj.create_dialog()
                            with ui.button(color=self._background_color, on_click=lambda d=a_dialog: d.open()).classes('w-full').style('color: #6E93D6;') as item:
                                ui.restructured_text(f'**User:** {name}').classes('w-full text-left').style("color: #8091ad;")
                                ui.restructured_text(f'**Review Text:** {review_txt}').classes('w-full text-left').style("color: #8680ad;")
                            ui.separator().style("background-color: #88607c;")
        # end part

    def build_app(self, content, classify_tool):
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
        self.show_record_sentiment_prob(content, classify_tool)
        ui.run(port=5434)
        