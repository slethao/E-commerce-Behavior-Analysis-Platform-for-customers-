from nicegui import ui

class Charts:
    def __init__(self, positive_color, neutral_color, negative_color):
        self._positive_color = positive_color
        self._neutral_color = neutral_color
        self._negative_color = negative_color

    def make_highlight_charts_1(self, background, line_color, given_color, all_senti_reviews):
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
    
    def make_highlight_charts(self, background, line_color, given_color, senti_comments):
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
        