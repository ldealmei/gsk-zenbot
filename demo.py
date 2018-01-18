from Zenbot import Zenbot
from Task import Task
from Event import Meeting, Training
import uuid
from numpy.random import randint, choice
import numpy as np

import datetime

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Text, HoverTool

def get_random_cert() :
    cert = ''

    with open('training_courses.txt') as f :
        courses = f.readlines()
        while len(cert)<5 :  # sure its not an empty line
            cert = courses[randint(0,len(courses))]

    return cert

def task_generator():
    project_id = uuid.uuid4()
    deadline  = datetime.date.today() + datetime.timedelta(days = randint(1,21))
    creator = ''
    dur_estim = datetime.timedelta(hours=randint(1,4))
    importance = randint(1,4)
    effort = randint(1,6)

    available_categories = ["Congés", "Design", "Documentation", "Formations suivies", "Gestion des accès", "Other", "Project preliminary", "TC3/TC5", "Technical Implementation", "Training recieved", "Validation Execution", "WB", "WB (Gestion + Meetings)"]
    category = available_categories[randint(0,len(available_categories))]

    return Task(project_id, deadline, creator, dur_estim, importance, effort, category,  description= {})


def event_generator():
    event_type = choice(['training', 'meeting'],1, p =[0.3, 0.7])

    if event_type == 'training' :
        start = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days = randint(0,21)),datetime.time(hour=8))
        duration = datetime.timedelta(hours=3)
        end= start + duration
        loc = {}
        certification = get_random_cert()

        return Training(start, end, loc, certification )

    elif event_type == 'meeting' :
        start = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days = randint(0,21)),datetime.time(hour=randint(8,14)))
        duration = datetime.timedelta(hours=randint(1,3))
        end = start + duration

        loc = {}
        project_id = uuid.uuid4()
        participants = []

        return Meeting(start, end, loc, project_id, participants, tasks= [])

def day_shift(event_date) :

    return event_date - datetime.date.today()

def plot_events(events) :

    width = 1
    data = {'top' : [ev.end.hour for ev in events],
            'bottom' : [ev.start.hour for ev in events],
            'left' : [ day_shift(ev.start.date()).days for ev in events],
            'right' : [ day_shift(ev.start.date()).days + width  for ev in events],
            'color' : [ 'blue' if isinstance(ev,Meeting) else 'red' for ev in events],
            'name' : [str(ev.project_id) if isinstance(ev,Meeting)  else ev.certification for ev in events]}

    source = ColumnDataSource(data)
    p = figure(plot_width = 1000, plot_height = 600, x_range = [0,7], tools = ['xwheel_pan'])

    p.quad(top='top', bottom='bottom', left='left',
       right='right',
           color = 'color',
           source = source,
           line_color = 'white')

    # p.add_glyph(source, Text(x = 'bottom', y='left', text_color = 'black'))
    p.toolbar.logo = None

    hover = HoverTool(tooltips = [('Name','@name')])

    p.add_tools(hover)

    show(p)

def event_overlap(ev1,ev2) :
    overlap = False

    set1 = set(range(ev1.start.hour, ev1.end.hour))
    set2 = set(range(ev2.start.hour, ev2.end.hour))

    for s in set1:
        if s in set2:
            overlap = True
            break
    print(overlap)
    return overlap

def resolve_conflicts(events) :
        drop_events = []
        for ev in events :
            for ev_comp in events :
                if ev.start.date() == ev_comp.start.date() :
                    if ev != ev_comp :
                        if event_overlap(ev,ev_comp):
                            drop_events.append(ev_comp)

        return [ev for ev in events if ev not in drop_events]


params={'id':'',
        'events' : resolve_conflicts([event_generator() for i in np.arange(50)]),
        'tasks' : [task_generator() for i in np.arange(100)]}

# print(params['tasks'])
print(len(params['events']))
plot_events(params['events'])

test_bot = Zenbot(params)
print(test_bot.make_today_schedule())