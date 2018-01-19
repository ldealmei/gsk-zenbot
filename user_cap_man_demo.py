import datetime
from numpy.random import randint, shuffle
# import numpy as np
import uuid

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, BoxAnnotation
from bokeh.layouts import row

from Task import Task

def task_generator(time_dir):

    project_id = uuid.uuid4()
    if time_dir =='forth' :
        deadline  = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days = randint(1,21)), datetime.time(0))
    elif time_dir =='back' :
        deadline  = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days = randint(1,21)), datetime.time(0))

    creator = ''
    dur_estim = datetime.timedelta(hours=randint(1,4))
    importance = randint(1,4)
    effort = randint(1,6)

    available_categories = ["Congés", "Design", "Documentation", "Formations suivies", "Gestion des accès", "Other", "Project preliminary", "TC3/TC5", "Technical Implementation", "Training recieved", "Validation Execution", "WB", "WB (Gestion + Meetings)"]
    category = available_categories[randint(0,len(available_categories))]

    return Task(project_id, deadline, creator, dur_estim, importance, effort, category,  description= {})


def dashboardize(p) :
    p.xgrid.grid_line_color = None
    p.toolbar_location = None
    p.outline_line_color = None

def get_day_workload(day_events) : # workload based on events and trainings

    return sum([ev.end.hour -ev.start.hour for ev in day_events])

def get_workload_timeline(events) :
    timeline = []

    events_day = [ev.start.date() for ev in events].sort()
    for day in events_day :
        events_of_the_day = [ev for ev in events if ev.start.date() == day]
        timeline.append(get_day_workload(events_of_the_day))

    return timeline

# ----------------- GET DATA FROM REPORTS -----------------
# get tasks df
# get events
events = get_report_events()

overall_timeline = get_workload_timeline(events)

timeline = []

data = {'timeline': timeline, 'forecast' : forecast,
        'x_past' : [datetime.datetime(year = 2018,month = 1,day =i) for i in range(1,len(timeline)+1) ],
        'x_futur': [datetime.datetime.today() + datetime.timedelta(days=i) for i in range(1, len(timeline) + 1)]}

source = ColumnDataSource(data)

p_timeline = figure(plot_height = 300, plot_width = 300, y_range = [0, 1.5], title = 'Workload Timeline', x_axis_type = 'datetime')
p_timeline.line(x='x_past', y='timeline', source = source)
p_timeline.circle(x='x_past', y='timeline', source = source)

hover_timeline = HoverTool(tooltips = [('Workload','@timeline')], mode = 'vline')
p_timeline.add_tools(hover_timeline)

overload_box = BoxAnnotation(bottom = 1,top=1.3, fill_alpha=0.1, fill_color='red')
p_timeline.add_layout(overload_box)

dashboardize(p_timeline)

p_forecast = figure(plot_height = 300, plot_width = 300, y_range = [0, 1.5], title = 'Workload Forecast', x_axis_type = 'datetime')
p_forecast.line(x='x_futur', y='forecast', source = source)
p_forecast.circle(x='x_futur', y='forecast', source = source)

hover_forecast = HoverTool(tooltips = [('Workload','@forecast')], mode = 'vline')
p_forecast.add_tools(hover_forecast)

dashboardize(p_forecast)
overload_box = BoxAnnotation(bottom = 1,top=1.3, fill_alpha=0.1, fill_color='red')
p_forecast.add_layout(overload_box)

show(row(p_timeline, p_forecast))
