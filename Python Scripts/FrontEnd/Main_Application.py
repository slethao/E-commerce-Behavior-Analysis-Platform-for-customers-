from nicegui import ui

class Main_Application:
    def __init__(self, label):
        self._label = label

    def build_app(self):
        ui.query('body').style('background-color: #170f18;')
        with ui.row().classes('w-full justify-between items-center'):
            ui.label("Amozon Customer Sentimental Analysis on Reviews and Comments").style("font-weight: bold; font-size: 20px; color: #8a627e;")
            with ui.button(color='#6e2c5d'):
                with ui.row():
                    ui.icon('done').classes('bg-[#b5539c] p-1 rounded-full').style('color: #6e2c5d')
                    ui.label('transfer status').classes('mt-[5px]').style('color: #b5539c')
        ui.separator().style("background-color: #8a627e;")
        with ui.column():
            with ui.row().classes('w-full'):
                # with ui.card().classes('w-[700px] h-[450px] bg-blue-500 text-white border-solid border-gray-400'):
                with ui.card().classes('w-[700px] h-[475px] text-white').style('border: 2.5px solid #7b5e7b; background-color: #170f18; border-radius: 20px;'): #NOTE background-color: #271727
                    ui.label("Sentimental Comments From 2013 and 2014").style("font-size: 25px; color: #c495ad; font-weight: bold;").classes('font-bold italic justify-center')
                    ui.separator().style("background-color: #7b5e7b;")
                    ui.highchart({
                            'colors': ['#b39db7', '#9083a3', '#7e5479'], #NOTE play round with this
                            'title': False,
                            'chart': {'type': 'bar', 'backgroundColor': '#170f18', 'color': '#7b5e7b'},
                            'xAxis': {'categories': ['A', 'B', 'C'], 
                                        'axisLabel': {'color': '#7b5e7b'},
                                        'color': '#7b5e7b',
                                        'lineColor': '#c495ad',
                                        'labels':{'itemStyle': {'color': '#c495ad'}, 'style': {'color': '#c495ad'}},
                                        },
                            'yAxis': {'title': {'text': 'Values', 'style': {'color': '#7b5e7b'}}, 'labels':{'style':{'color': '#7b5e7b'}}, 'lineColor': '#7b5e7b'},
                            'legend': { 'fill': '#7b5e7b', 'labels': { 'style': { 'fill': '#7b5e7b' }}},
                            'series': [
                                {'name': 'Alpha', 'data': [0.1, 0.2]},
                                {'name': 'Beta', 'data': [0.3, 0.4]},
                                {'name': 'Gama', 'data': [0.7, 0.5]}
                            ],
                            'plotOptions':
                            {
                                'bar':
                                {
                                    'borderColor': '#c495ad',
                                    'borderWidth': 2,
                                }
                            }
                        }).classes('w-full h-90 [&_g.highcharts-legend-item_text]:!fill-[#c495ad] [&_path.highcharts-grid-line]:!stroke-[#c495ad]')
                    # ui.label("This is a graph")
                with ui.card().classes('w-[700px] h-[475px] no-border no-shadow').style('background-color: #170f18; border-radius: 20px;'): #NOTE #261b2a # border border: 2.5px solid #57435e;
                    with ui.column().classes('w-full justify-center'):
                        with ui.row().classes('items-center justify-between'): # .classes('justify-center')
                            ui.label("Overall Star Rating: 3.5").style('font-weight: bold; color: #c3b6fd; font-size: 25px;').classes('italic mt-[-10px]')
                            ui.rating(value=3.5, max=5,icon_selected='star',color="violet-300", size="40px").classes('mt-[-15px]') # .classes('w-full justify-center') # size='48px'
                        ui.highchart({
                            'title': False,
                            'colors': ['#9086ba', '#868bba', '#86a0ba'],
                            'chart': {'type': 'bar', 'backgroundColor': '#170f18', 'color': '#7b6582'},
                            'xAxis': {'categories': ['A', 'B', 'C'], 
                                        'axisLabel': {'color': '#7b6582'},
                                        'color': '#7b6582',
                                        'lineColor': '#c3b6fd',
                                        'labels':{'itemStyle': {'color': '##c3b6fd'}, 'style': {'color': '#c3b6fd'}},
                                    },
                            'yAxis': {'title': {'text': 'Values', 'style': {'color': '#7b6582'}}, 'labels':{'style':{'color': '#7b6582'}}, 'lineColor': '#7b6582'},
                            'legend': { 'fill': '#7b6582', 'labels': { 'style': { 'fill': '#7b6582' }}},
                            'series': [
                                {'name': 'Alpha', 'data': [0.1]},
                                {'name': 'Beta', 'data': [0.3]},
                                {'name': 'Gama', 'data': [0.7]}
                            ],
                            'plotOptions':
                            {
                                'bar':
                                {
                                    'borderColor': '#c3b6fd',
                                    'borderWidth': 2,
                                }
                            }
                        }).classes('w-full h-90 [&_g.highcharts-legend-item_text]:!fill-[#c3b6fd] mt-[10px] [&_path.highcharts-grid-line]:!stroke-[#c3b6fd]')
            with ui.card().classes('w-full h-[250px]').style('border: 2.5px solid #88607c; background-color: #170f18; border-radius: 20px;'): #NOTE background #291624
                with ui.column().classes('w-full'):
                    with ui.row().classes('mt-[-10px]'):
                        ui.label("This is the veidct box").style('color: #606688; font-size: 20px;').classes('mt-[10px]')
                        with ui.row():
                                ui.icon('sentiment_satisfied_alt', size='xl', color='#886087')
                                ui.label("20%").style('color: #886087; font-size: 20px;').classes('mt-[10px]')
                        with ui.row():
                            ui.icon('sentiment_neutral', size='xl', color='#776088')
                            ui.label('50%').style('color: #776088; font-size: 20px;').classes('mt-[10px]')
                        with ui.row():
                            ui.icon('sentiment_dissatisfied', size='xl', color='#686088')
                            ui.label("30%").style('color: #686088; font-size: 20px;').classes('mt-[10px]')
                        ui.label("(based on commentator)").classes('italic mt-[10px]').style('color: #606688; font-size: 15px;')
                    with ui.row().classes('w-full'):
                        with ui.scroll_area().classes('h-40 border').style('background-color: #291624; border-radius: 20px; border: 2px solid #47243e; font-size: 20px;'): # #291624 #47243e #6e4162
                            ui.label('I scroll. I scroll. I scroll. I scroll. I scroll. I scroll. I scroll. I scroll. I scroll.' * 20).style("color: #8680ad;")
        ui.run(port=5434)
        