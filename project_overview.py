import datetime
from numpy.random import randint, shuffle
# import numpy as np
import uuid

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, BoxAnnotation, CDSView, BooleanFilter
from bokeh.layouts import row

from Task import Task

def dashboardize(p) :
    p.ygrid.grid_line_color = None
    p.xgrid.grid_line_color = None
    p.toolbar_location = None
    p.outline_line_color = None

statuses =[True, True, False, False, False]

data = {'status' : statuses,
        'phase' : ["Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5"]}
source = ColumnDataSource(data)

view_done = CDSView(source=source, filters=[BooleanFilter(statuses)])
view_todo = CDSView(source=source, filters=[BooleanFilter([not s for s in statuses])])


p = figure(plot_height = 300, plot_width = 800, title = 'Project Timeline', x_range = data['phase'])
p.title.align = 'center'

p.line(x = 'phase', y = 0, line_dash ='solid', line_width = 5, source= source, view = view_done)
p.line(x = 'phase', y = 0, line_dash ='dashed', line_width = 5, source= source, view = view_todo)

# TODO : Remove cheat Hack
view_hack = CDSView(source=source, filters=[BooleanFilter([False,True,True, False, False])])
p.line(x = 'phase', y = 0, line_dash ='solid', line_width = 5, source= source, view = view_hack)

p.circle(x='phase',y=0, size =20,  source= source, view = view_done)
p.circle(x='phase',y=0,fill_color ='white', size =20, source= source, view = view_todo)
dashboardize(p)

hover = HoverTool(tooltips = [('Resources', 'Jane, Bob'),
                              ('Deadline', '2018-01-23'),
                              ('...','...')],
                  mode = 'vline')
p.add_tools(hover)

p.xaxis.major_label_text_font_size = '20pt'
p.xaxis.major_label_text_font_style = 'bold'

show(p)
