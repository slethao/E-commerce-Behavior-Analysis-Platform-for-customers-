from nicegui import ui
import FrontEnd.Charts as chart
import FrontEnd.Dialog as dia
import Processing_Layer as pl
import os
"""
This class contains teh main appliation (the dashboard)
"""
class Main_Application:
    __slots__ = ('background_color', 'line_color', 'given_color')

    def __init__(self, background_color: str, line_color: str, given_color: str):
        """
        Constructor for the class 'Main_Application'

        Parameters:
            background_color (str): the hexacode that is used for the background color
            line_color (str): the hexacode that is used for the gird color
            given_color (str): the hexacode that is used for the axis and the graph descriptions
        """
        self._background_color = background_color
        self._line_color = line_color
        self._given_color = given_color

    def show_comments(self, comments_senti_data: dict[str, int]) -> None:
        """
        This method display the sentimental analysis for the amozon review comments
        in 2013 - 2014 (this returns nothing)
            Parameter:
                comments_senti_data (dict[str, int]): a dictionary with a key-value pair
                            key: is the group of sentimental analysis teh value belongs
                                    example: postive or negative
                            vale: is the number of occurances found in the dataset
        """
        with ui.card().classes('w-[700px] h-[475px] text-white').style('border: 2.5px solid #7b5e7b; background-color: #170f18; border-radius: 20px;'): #NOTE background-color: #271727
            ui.label("Sentimental Comments From 2013 and 2014").style("font-size: 25px; color: #c495ad; font-weight: bold;").classes('font-bold italic justify-center')
            ui.separator().style("background-color: #7b5e7b;")
            chart_obj = chart.Charts('#b39db7', '#9083a3', '#7e5479')
            chart_obj.make_highlight_charts(self._background_color, self._line_color, self._given_color, comments_senti_data)

    def set_line_color(self, new_line_color: str) -> None:
        """
        This method is to modify the line color in the appliation
        (this returns nothing)
            Parameter:
                new_line_color (str): the new hexacode that the program wants to use
        """
        self._line_color = new_line_color

    def set_given_color(self, new_given_color: str) -> None:
        """
        This method is to modify the given color in the appliation
        (this returns nothing)
            Parameter:
                new_given_color (str): the new hexacode that the program wants to use
        """
        self._given_color = new_given_color

    def show_star_review(self, mapped_data: dict[str, list[str]], sentiment_star_data: list[str]) -> None:
        """
        This method is used to display the 5-star reviews of the sentimental analysis
        (this returns nothing)
            Parameter:
                mapped_data (dict[str, list[str]]): each key contains a group in from the filtered dataset that refernces 
                                                    the data associated with that group
                                                        example:
                                                            mapped_data['reviewText'] = [all data related to reviewText/commnets]
                                                            NOTE reviewText = the group in the filtered datset
                sentiment_star_data (list[str]): a list of the sentimentla 5-star analysis of the overall dataset
                                                    index 0: is the positive
                                                    index 1: is the neutral
                                                    index 2: is the negative 
        """
        with ui.card().classes('w-[700px] h-[475px] no-border no-shadow').style('background-color: #170f18; border-radius: 20px;'): #NOTE #261b2a # border border: 2.5px solid #57435e;
            with ui.column().classes('w-full justify-center'):
                with ui.row().classes('items-center justify-between'): # .classes('justify-center')
                    process_obj = pl.Processing_layer(mapped_data)
                    csv_format = process_obj.get_csv_format()
                    ui.label(f"Overall Star Rating: {process_obj.overall_review_product(csv_format)}").style('font-weight: bold; color: #c3b6fd; font-size: 25px;').classes('italic mt-[-10px]')
                    ui.rating(value=process_obj.overall_review_product(csv_format), max=5,icon_selected='star',color="violet-300", size="40px").classes('mt-[-15px]') # .classes('w-full justify-center') # size='48px'
                chart_obj = chart.Charts('#9086ba', '#868bba', '#86a0ba')
                self.set_line_color('#c3b6fd')
                self.set_given_color('#7b6582')
                chart_obj.make_highlight_charts_1(self._background_color, 
                                                self._line_color, 
                                                self._given_color,
                                                sentiment_star_data
                                                )

    def show_record_sentiment_prob(self, content: dict[str, list[str]], classify_tool: object, comments_senti_data: list[float, float, float]) -> None:
        """
        The method is used to display all the records that are in the filtered dataset
        that are displayed in a scroll area that, once clikec you are able to see the 
        sentimental analysis of each record when you clik on the a record siplayed in 
        the dashboard (this returns none)
            Parameter:
                content (dict[str, list[str]]): each key contains a group in from the filtered dataset that refernces 
                                                the data associated with that group
                                                    example:
                                                        mapped_data['reviewText'] = [all data related to reviewText/commnets]
                                                        NOTE reviewText = the group in the filtered datset
                classify_tool (object): an object used to call the textblob object to use to calucate teh record sentimenatl analysis
                comments_senti_data (list[float, float, float]): listing of the sentimental analysis on comments for the record
                                                                    index 0: is the positive
                                                                    index 1: is the neutral
                                                                    index 2: is the negative 
        """
        with ui.card().classes('w-full h-[250px]').style('border: 2.5px solid #88607c; background-color: #170f18; border-radius: 20px;'): #NOTE background #291624
            with ui.column().classes('w-full'):
                with ui.row().classes('mt-[-10px]'):
                    result = [key for key in comments_senti_data.keys() if max(comments_senti_data.values()) <= comments_senti_data[key]]
                    if result == ["pos"]:
                        ui.label(f"In conclusion, if comments are {"".join(result)}itive then the 5-star reviews will mostly be {"".join(result)}itive and neutral but rarely negative.").style('color: #606688; font-size: 20px;').classes('mt-[10px]')
                    if result == ["neg"]:
                        ui.label(f"In conclusion, if comments are {"".join(result)}ative then the 5-star reviews will mostly be {"".join(result)}ative and neutral but rarely positive.").style('color: #606688; font-size: 20px;').classes('mt-[10px]')
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

    def build_app(self, content: dict[str,list[str]], classify_tool: object, sentiment_star_data: list[str], comments_senti_data: dict[str, int]) -> None:
        """
        The method is used to build the dashboard and build all the main comments to the dashboard
        (this returns none)
            Parameter:
                content (dict[str,list[str]]): the group is mapped to all the data that is associated with the group
                classify_tool (object): the object that is use to refence all the trained adn test
                                        data in order to do analysis on indicidual record
                sentiment_star_data (list[str]): the listing for the sentimental analyis overall on the 5-star review
                comments_senti_data (dict[str, int]): the sentimental analysis group refernce the number of times it
                                                        it shows in the dataset
                                                            example: 
                                                                comments_senti_data['pos'] = number of times is shown
                                                                comments_senti_data['neg'] = number of times is shown
                                                            NOTE: number of times is shown is an integer value
        """
        ui.query('body').style(f'background-color: {self._background_color};')

        with ui.row().classes('w-full justify-between items-center'):
            ui.label("Amozon Customer Sentimental Analysis on Reviews and Comments").style("font-weight: bold; font-size: 20px; color: #8a627e;")
            
        ui.separator().style("background-color: #8a627e;")
        with ui.column():
            with ui.row().classes('w-full'):
                self.show_comments(comments_senti_data)
                self.show_star_review(content, sentiment_star_data) 
        self.show_record_sentiment_prob(content, classify_tool, comments_senti_data)
        ui.run(port=os.getenv("FRONT_END_PORT"))
        