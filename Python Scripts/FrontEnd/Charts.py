from nicegui import ui

"""
This class is used to make charts
"""
class Charts:
    __slots__ = ('positive_color', 'neutral_color', 'negative_color')

    def __init__(self, positive_color: str, neutral_color: str, negative_color: str):
        """
        Constructor for the class 'Charts'

        Parameters:
            positive_color (str): the hexacode that will represent the positive reviews in the dashboard 
            neutral_color (str): the hexacode that will represent the neutral reviews in the dashboard
            negative_color (str): the hexacode that will represent the negative reviews in the dashboard
        """
        self._positive_color = positive_color
        self._neutral_color = neutral_color
        self._negative_color = negative_color

    def make_highlight_charts_1(self, background: str, line_color: str, given_color: str, all_senti_reviews: list[str]) -> None:
        """
        This method creates a highchart that displays an 
        interactive chart for the five-star reviews
        (this returns nothing)

        Parameters:
            background (str): the hexacodethat will represent the color of the background
            line_color (str): the hexacode will represent the color for the line colors for the grid lines and description text
            given_color (str): the hexacode that will be used for the axis
            all_senti_reivews (list[str]): a list that will have the sentimental positive, neutral, and negative of the
                                            5-star reviews
                                                index 0: is the positive
                                                index 1: is the neutral
                                                index 2: is the negative 
        """
        ui.highchart({
            'title': False,
            'colors': [self._positive_color, self._neutral_color, self._negative_color],
            'chart': {'type': 'bar', 'backgroundColor': background, 'color': given_color},
            'xAxis': {'categories': ['Reviews','B','C'], 
                        'axisLabel': {'color': given_color},
                        'color': given_color,
                        'lineColor': line_color,
                        'labels':{'itemStyle': {'color': line_color}, 'style': {'color': line_color}},
                    },
            'yAxis': {'title': {'text': 'Values', 'style': {'color': given_color}}, 'labels':{'style':{'color': given_color}}, 'lineColor': given_color},
            'legend': { 'fill': given_color, 'labels': { 'style': { 'fill': given_color }}},
            'series': [
                {'name': 'Positive', 'data': [float(all_senti_reviews[0].rstrip(","))]}, # index 0
                {'name': 'Neutral', 'data': [float(all_senti_reviews[1].rstrip(","))]}, # index 1
                {'name': 'Negative', 'data': [float(all_senti_reviews[2].rstrip(","))]} # index 2
            ],
            'plotOptions':
            {
                'bar':
                {
                    'borderColor': line_color,
                    'borderWidth': 2,
                }
            }
        }).classes(f'w-full h-90 [&_g.highcharts-legend-item_text]:!fill-[{line_color}] mt-[10px] [&_path.highcharts-grid-line]:!stroke-[{line_color}]')
    
    def make_highlight_charts(self, background: str, line_color: str, given_color: str, senti_comments: list[float]) -> None:
        """
        This method creates a highchart that displays an 
        interactive chart for the sentiment analysi on the
        review comments
        (this returns nothing)

        Parameters:
            background (str): the hexacodethat will represent the color of the background
            line_color (str): the hexacode will represent the color for the line colors for the grid lines and description text
            given_color (str): the hexacode that will be used for the axis
            senti_comments (list[float]): a list that will have the sentimental positive, neutral, and negative of the
                                            review comments
                                                index 0: is the positive
                                                index 1: is the neutral
                                                index 2: is the negative 
        """
        ui.highchart({
            'title': False,
            'colors': [self._positive_color, self._neutral_color, self._negative_color],
            'chart': {'type': 'bar', 'backgroundColor': background, 'color': given_color},
            'xAxis': {'categories': ['Reviews','B','C'], 
                        'axisLabel': {'color': given_color},
                        'color': given_color,
                        'lineColor': line_color,
                        'labels':{'itemStyle': {'color': line_color}, 'style': {'color': line_color}},
                    },
            'yAxis': {'title': {'text': 'Values', 'style': {'color': given_color}}, 'labels':{'style':{'color': given_color}}, 'lineColor': given_color},
            'legend': { 'fill': given_color, 'labels': { 'style': { 'fill': given_color }}},
            'series': [
                {'name': 'Positive', 'data': [senti_comments['pos']]}, # index 0
                {'name': 'Neutral', 'data': [0.0]}, # index 1
                {'name': 'Negative', 'data': [senti_comments['neg']]} # index 2
            ],
            'plotOptions':
            {
                'bar':
                {
                    'borderColor': line_color,
                    'borderWidth': 2,
                }
            }
        }).classes(f'w-full h-90 [&_g.highcharts-legend-item_text]:!fill-[{line_color}] mt-[10px] [&_path.highcharts-grid-line]:!stroke-[{line_color}]')
        