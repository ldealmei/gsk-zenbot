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

def get_kpis(cert_report_dict):
    nbr_done = len(cert_report_dict['certifications'].keys())
    nbr_todo = len(cert_report_dict['requiredcertifications'].keys())

    main_kpi = float(nbr_done) / nbr_todo
    return [main_kpi, 1 - main_kpi]

# ---------------- GET DATA ----------------
cert_report_dict = None
kpis= get_kpis(cert_report_dict)
kpi_names = ['%T', '%(U-Y-X)']
print(kpis)

kpi_data = {'kpi' :  kpis, 'y' : [1,2],
            'txt_kpi' : [k+0.03 for k in kpis], 'txt_y' : kpi_names, 'txt_format' : [str(k*100) + ' %' for k in kpis]}
kpi_source = ColumnDataSource(kpi_data)


# ---------------- MAIN KPI VIEW ----------------
p_training_kpi = figure(plot_height = 250, plot_width = 250, title = "Max T%")
p_training_kpi.title.align = 'center'

p_training_kpi.annular_wedge(x=0, y=0,
                inner_radius=0.5, outer_radius=0.6,
                start_angle=-2*pi*kpis[0], end_angle=0,
                color="green", alpha=0.6)

citation = Label(x=0, y=-0.1,
                 text=str(kpis[0]*100) + ' %', render_mode='css', text_font_size = '20pt', text_align = 'center')

p_training_kpi.add_layout(citation)

dashboardize(p_training_kpi)

# ---------------- INDIVIDUAL KPI VIEW ----------------
p_indicators = figure(plot_height = 250, plot_width = 250, x_range = [0, 1.3], y_range = kpi_names)
p_indicators.hbar(y='y', height=0.5, left=0, right='kpi', fill_alpha = 0.6, source = kpi_source)
p_indicators.circle(x = 'kpi',y = 'y', name = 'tip', alpha = 0, hover_alpha = 1, source = kpi_source)
text_glyph = Text(x='txt_kpi', y="txt_y", text='txt_format')
p_indicators.add_glyph(kpi_source, text_glyph)

hover = HoverTool(tooltips = [('Value %','@kpi')],mode = 'hline', names =['tip'])
p_indicators.add_tools(hover)

dashboardize(p_indicators)
p_indicators.yaxis.visible = True

# ---------------- TRAINING TO DO VIEW ----------------

temp = [(k,v) for k,v in cert_report_dict['requiredcertifications'].keys()]

data_forth = {'title': [], 'date' : []}
data_forth['title'] = [v[0] for v in temp]
data_forth['date'] = [v[1] for v in temp]

temp = [(k,v) for k,v in cert_report_dict['certifications'].keys()]

data_back = {'title': [], 'date' : []}
data_back['title'] = [v[0] for v in temp]
data_back['date'] = [v[1] for v in temp]


table_forth_source = ColumnDataSource(data_forth)
table_back_source = ColumnDataSource(data_back)

columns = [
        TableColumn(field="title", title="Certification"),
        TableColumn(field="date", title="Date",  formatter=DateFormatter()),
        ]

forth_table = DataTable(source=table_forth_source, columns=columns, width=400, height=280)
back_table = DataTable(source=table_back_source, columns=columns, width=400, height=280)

show(gridplot([p_training_kpi,forth_table],[p_indicators, back_table],merge_tools=False))
