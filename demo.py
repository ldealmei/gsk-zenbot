import Zenbot
import Task
from Event import Meeting, Training
import uuid
from numpy.random import randint, choice
import numpy as np

import datetime

from bokeh.io import show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

def get_random_cert() :
    cert = ''

    with open('training_courses.txt') as f :
        courses = f.readlines()
        while len(cert)<5 :  # sure its not an empty line
            cert = courses[randint(0,len(courses))]

    return cert

def task_generator():
    project_id = uuid.uuid4()
    deadline  = datetime.date.today() + datetime.timedelta(days = randint(1,100))
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
        start = datetime.date.today() + datetime.timedelta(days = randint(0,100)) + datetime.time(hour=8)
        duration = datetime.timedelta(hours=3)
        end= start + duration
        loc = {}
        certification = get_random_cert()

        return Training(start, end, loc, certification )

    elif event_type == 'meeting' :
        start = datetime.date.today() + datetime.timedelta(days = randint(0,100)) + datetime.time(hour=randint(8,14))
        duration = datetime.timedelta(hours=randint(1,3))
        end = start + duration

        loc = {}
        project_id = ''
        participants = []

        return Meeting(start, end, loc, project_id, participants, tasks= [])

def day_shift(date) :

    return date - datetime.date.today()

def plot_events(events) :

    width = 1
    data = {'top' : [ev.end.hour for ev in events],
            'bottom' : [ev.start.hour for ev in events],
            'left' : [ day_shift(ev.start.date).days for ev in events],
            'right' : [ day_shift(ev.start.date).days + width  for ev in events],
            'color' : [ 'blue' if type(ev) == type(Meeting) else 'red' for ev in events]}

    p = figure(plot_width = 1000, plot_height = 600)

    p.toolbar.logo = None


params={'id':'',
        'events' : [event_generator() for i in np.arange(20)],
        'tasks' : [task_generator() for i in np.arange(50)]}

bot1 = Zenbot(params)