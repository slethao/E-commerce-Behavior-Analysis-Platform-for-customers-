from nicegui import ui

class Charts:
    def __init__(self, positive_color, neutral_color, negative_color):
        self._positive_color = positive_color
        self._neutral_color = neutral_color
        self._negative_color = negative_color

    def make_highlight_charts(self, background, line_color, given_color):
        ui.highchart({
            'title': False,
            'colors': [self._positive_color, self._neutral_color, self._negative_color],
            'chart': {'type': 'bar', 'backgroundColor': background, 'color': given_color},
            'xAxis': {'categories': ['A', 'B', 'C'], 
                        'axisLabel': {'color': given_color},
                        'color': given_color,
                        'lineColor': line_color,
                        'labels':{'itemStyle': {'color': line_color}, 'style': {'color': line_color}},
                    },
            'yAxis': {'title': {'text': 'Values', 'style': {'color': given_color}}, 'labels':{'style':{'color': given_color}}, 'lineColor': given_color},
            'legend': { 'fill': given_color, 'labels': { 'style': { 'fill': given_color }}},
            'series': [
                {'name': 'Alpha', 'data': [0.1]},
                {'name': 'Beta', 'data': [0.3]},
                {'name': 'Gama', 'data': [0.7]}
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
        