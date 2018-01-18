import datetime
from numpy.random import randint

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
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


data = {
        'trainings_done' : [training_generator('back') for i in range(5)],
        'trainings_todo' : [training_generator('forth') for i in range(5)],
        }

p_training_kpi = figure(plot_height = 250, plot_width = 250)

p_training_kpi.annular_wedge(x=0, y=0,
                inner_radius=0.1, outer_radius=0.25,
                start_angle=0, end_angle=-0.5,
                color="green", alpha=0.6)

dashboardize(p_training_kpi)


table_source = ColumnDataSource(data)

p_indicators = figure(plot_height = 250, plot_width = 250)
p_indicators.hbar(y=1, height=0.5, left=0,
       right=0.95)
p_indicators.hbar(y=2, height=0.5, left=0,
       right=0.2)
p_indicators.hbar(y=3, height=0.5, left=0,
       right=0.2)
p_indicators.hbar(y=4, height=0.5, left=0,
       right=0.1)

dashboardize(p_indicators)
hover = HoverTool(tooltips = [('Value %','$x')])
p_indicators.add_tools(hover)

show(gridplot([p_training_kpi,None],[p_indicators, None],merge_tools=False))
