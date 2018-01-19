import datetime
from numpy.random import randint, shuffle
from math import pi

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Text, Label, TableColumn, DataTable, BoxAnnotation
from bokeh.layouts import gridplot, row

from Event import Training

def get_random_cert() :
    cert = ''

    with open('training_courses.txt') as f :
        courses = f.readlines()
        while len(cert)<5 :  # sure its not an empty line
            cert = courses[randint(0,len(courses))]

    return cert

def training_generator(dir):

    if dir == 'forth' :
        start = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days = randint(0,21)),datetime.time(hour=8))
    elif dir == 'back' :
        start = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days = randint(0,100)),datetime.time(hour=8))

    duration = datetime.timedelta(hours=3)
    end= start + duration
    loc = {}
    certification = get_random_cert()

    return Training(start, end, loc, certification )

def dashboardize(p) :
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.yaxis.visible = False
    p.toolbar_location = None
    p.outline_line_color = None


kpis = [0.95, 0.92, 0.87, 0.99]

kpi_data = {'kpi' : kpis, 'team' : ["Pascal","Jena","Chris","Salvino"],
            'kpi_disp' : [-2*pi*kpi for kpi in kpis],
            'kpi_text' : [str(int(100*kpi)) + '%' for kpi in kpis]}

kpi_source = ColumnDataSource(kpi_data)

p_training_kpi = figure(plot_height = 250, plot_width = 250, title = "Max T%", x_range =kpi_data['team'], y_range = [-1,1])
p_training_kpi.title.align = 'center'

p_training_kpi.annular_wedge(x='team', y=0,
                inner_radius=0.3, outer_radius=0.4,
                start_angle='kpi_disp', end_angle=0,
                color="green", alpha=0.6, source= kpi_source)

citation = Text(x='team', y=-0.07,
                 text='kpi_text', text_font_size = '10pt', text_align = 'center')

p_training_kpi.add_glyph(kpi_source,citation)

dashboardize(p_training_kpi)

# Capacity
timeline = [0.99375,1.06875,1.0625,1.10625,1.11875,1.25625,1.06875,1.14375,1.1375,1.0875,1.2875,1,1.18125,1.16875,1.08125,1.11875]

forecast = timeline.copy()
shuffle(forecast)


data = {'timeline': timeline, 'forecast' : forecast,
        'x_past' : [datetime.datetime(year = 2018,month = 1,day =i) for i in range(1,len(timeline)+1) ],
        'x_futur': [datetime.datetime.today() + datetime.timedelta(days=i) for i in range(1, len(timeline) + 1)]}
source = ColumnDataSource(data)

p_timeline = figure(plot_height = 250, plot_width = 250, y_range = [0, 1.5], title = 'Workload Timeline - Pascal', x_axis_type = 'datetime')
p_timeline.line(x='x_past', y='timeline', source = source)
p_timeline.circle(x='x_past', y='timeline', source = source)

hover_timeline = HoverTool(tooltips = [('Workload','@timeline')], mode = 'vline')
p_timeline.add_tools(hover_timeline)

overload_box = BoxAnnotation(bottom = 1,top=1.3, fill_alpha=0.1, fill_color='red')
p_timeline.add_layout(overload_box)

dashboardize(p_timeline)

p_forecast = figure(plot_height = 250, plot_width = 250, y_range = [0, 1.5], title = 'Workload Forecast - Pascal', x_axis_type = 'datetime')
p_forecast.line(x='x_futur', y='forecast', source = source)
p_forecast.circle(x='x_futur', y='forecast', source = source)

hover_forecast = HoverTool(tooltips = [('Workload','@forecast')], mode = 'vline')
p_forecast.add_tools(hover_forecast)

dashboardize(p_forecast)
overload_box = BoxAnnotation(bottom = 1,top=1.3, fill_alpha=0.1, fill_color='red')
p_forecast.add_layout(overload_box)





show(gridplot([p_training_kpi,p_timeline],
              [None, p_forecast], merge_tools = False))
