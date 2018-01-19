import datetime
from numpy.random import randint
from math import pi

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Text, Label, TableColumn, DataTable, DateFormatter
from bokeh.layouts import gridplot

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
    p.axis.visible = False
    p.toolbar_location = None
    p.outline_line_color = None


kpis = [0.95, 0.02, 0.01, 0.02]

kpi_data = {'kpi' : [0.95, 0.02, 0.01, 0.02], 'y' : [1,2,3,4],
            'txt_kpi' : [k+0.03 for k in kpis], 'txt_y' : [i - 0.15 for i in [1,2,3,4]], 'txt_format' : [str(k*100) + ' %' for k in kpis]}
kpi_source = ColumnDataSource(kpi_data)


p_training_kpi = figure(plot_height = 250, plot_width = 250, title = "Max T%")
p_training_kpi.title.align = 'center'

p_training_kpi.annular_wedge(x=0, y=0,
                inner_radius=0.5, outer_radius=0.6,
                start_angle=-2*pi*max(kpi_data['kpi']), end_angle=0,
                color="green", alpha=0.6)

citation = Label(x=0, y=-0.1,
                 text=str(max(kpi_data['kpi'])*100) + ' %', render_mode='css', text_font_size = '20pt', text_align = 'center')

p_training_kpi.add_layout(citation)

dashboardize(p_training_kpi)

p_indicators = figure(plot_height = 250, plot_width = 250, x_range = [0, 1.3])
p_indicators.hbar(y='y', height=0.5, left=0, right='kpi', fill_alpha = 0.6, source = kpi_source)
p_indicators.circle(x = 'kpi',y = 'y', name = 'tip', alpha = 0, hover_alpha = 1, source = kpi_source)
text_glyph = Text(x='txt_kpi', y="txt_y", text='txt_format')
p_indicators.add_glyph(kpi_source, text_glyph)

hover = HoverTool(tooltips = [('Value %','@kpi')],mode = 'hline', names =['tip'])
p_indicators.add_tools(hover)

dashboardize(p_indicators)


trainings_todo = [training_generator('forth') for i in range(5)]
data_forth = {'title': [],
        'start' : [],
        'end' : []}
for train in trainings_todo :
    data_forth['title'].append(train.certification)
    data_forth['start'].append(train.start)
    data_forth['end'].append(train.end)

trainings_done = [training_generator('back') for i in range(5)]
data_back = {'title': [],
        'start' : [],
        'end' : []}
for train in trainings_done :
    data_back['title'].append(train.certification)
    data_back['start'].append(train.start)
    data_back['end'].append(train.end)

table_forth_source = ColumnDataSource(data_forth)
table_back_source = ColumnDataSource(data_back)

columns = [
        TableColumn(field="title", title="Certification"),
        TableColumn(field="start", title="Date",  formatter=DateFormatter()),
        ]

forth_table = DataTable(source=table_forth_source, columns=columns, width=400, height=280)
back_table = DataTable(source=table_back_source, columns=columns, width=400, height=280)

show(gridplot([p_training_kpi,forth_table],[p_indicators, back_table],merge_tools=False))
