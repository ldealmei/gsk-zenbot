# coding: utf-8

import datetime
import os
import time
from numpy.random import randint, randn, rayleigh
import numpy as np
from bokeh.plotting import figure
from bokeh.io import  show
from bokeh.palettes import Spectral3
from bokeh.models import ColumnDataSource

def plot_agenda(agenda, p, idx) :
    width = 3
    data = {'top' : [ev['end'].hour for ev in agenda],
            'bottom' : [ev['start'].hour for ev in agenda],
            'left' : [idx*width + 1 for ev in agenda],
            'right' : [idx*width + width + 1 for ev in agenda],
            'color' : [Spectral3[-(ev['priority'])] for ev in agenda]}

    source = ColumnDataSource(data = data)

    
    p.quad(top='top', bottom='bottom', left='left',
       right='right',
           color = 'color',
           source = source,
           line_color = 'white',
       legend = "Agenda nr " + str(idx))
# small_palettes['Pastel1']

def get_agenda() :
    agenda = []
    start = 8
    
    # Simulate agenda
    day_occupancy = int(1.5 * randn() + 8)
    number_of_events = max(int(1 * randn() + 4),3)
    
    # print("Day occupancy : " + str(day_occupancy) + " - Nr events : " + str(number_of_events))
    for i in range(number_of_events) :
    
        event_duration = int(max(1 * randn() + float(day_occupancy)/number_of_events,1))
        event_priority = randint(1,4)
        event_start = int(rayleigh(0.5)) + start
        event_end = event_start+event_duration
        
        event = {'start' : datetime.datetime(2018,1,4,event_start),
            'end' : datetime.datetime(2018,1,4,event_end),
            'priority' : event_priority}

        agenda.append(event)
        start = event_end

    return agenda

def get_meeting_slot(agendas, meeting_params) :
    
    # Compute all possible slots within the time frame
    slot_list = get_slot_list(meeting_params)

    # Score each of these for each agenda
    slot_list_scored = score_slots(agendas, slot_list)

    # Take lower and earlier slot
    scores = [slot['score'] for slot in slot_list_scored]
    idx = np.argmin(scores)
    #    slot = {'start' : slot_start,
#        'end' : slot_end}

    return slot_list_scored[idx]

def get_slot_list(meeting_params) :

    if meeting_params['time_frame']>= datetime.timedelta(weeks = 1) :
        joint_agenda = join_agendas(agendas)
        days_selected = select_best_days(joint_agenda)
    else :
        days_selected = [datetime.date.today() + datetime.timedelta(days = day) for day in range(meeting_params['time_frame'].days)]

    return slots_from_days(days_selected, meeting_params['duration'])

def score_slots(agendas, slot_list) :
    #TODO : Score each slot previously selected

    return [{'start' : slot['start'], 'end' : slot['end'], 'score' : score_slot(slot, agendas)} for slot in slot_list]

def score_slot(slot, agendas) :
    events = [event for agenda in agendas for event in agenda]

    penalties = [1.0/event['priority'] for event in events if  slot_overlap(slot, event) ]

    return sum(penalties)

def slot_overlap(slot1, slot2) :
    overlap = False

    set1 = set(range(slot1['start'].hour,slot1['end'].hour))
    set2 = set(range(slot2['start'].hour,slot2['end'].hour))

    for s in set1 :
        if s in set2:
            overlap = True
            break

    return overlap


def join_agendas(agendas) :
    return {'events' : [event for agenda in agendas for event in agenda ], 'participants' : len(agendas)}

def select_best_days(joint_agenda) :
    # Get list of days
    days = [event['start'].date() for event in joint_agenda['events']]
    days = list(set(days)) # Keep unique days only
    # score each day : compatibility between agendas and day occupancy
    days_scored = score_compatibility(days, joint_agenda)
    idx = np.argsort(days_scored)

    return days[idx[:3]]

def score_compatibility(days, joint_agenda) :

        return [score_day_compatibility([event for event in joint_agenda['events'] if joint_agenda['events'].date() == date])
                  for date in days]

def score_day_compatibility(events) :
        # count total occupied time
        return sum([time.mktime(event['end'].timetuple()) - time.mktime(event['start'].timetuple()) for event in events ])

def slots_from_days(days_selected, meeting_duration) :
    #TODO : Return possible slots within the selected days

    # Assumptions :
    # granularity = 'hour'
    # day_length = 10h
    # day_start = 8
    # day_end  = 18

    return [{'start' : datetime.datetime.combine(date,datetime.time(hour = start_hour)),
              'end' : datetime.datetime.combine(date,datetime.time(hour = start_hour + meeting_duration.seconds/3600))}
            for date in days_selected for start_hour in [8 + i for i in range(10-meeting_duration.seconds/3600+1)] ]


if __name__ == "__main__" :
    
    # Create bots agenda
    agendas = []
    p = figure(plot_width=1200, plot_height=400)

    for i in range(5) :
        agenda = get_agenda()
        # print agenda
        plot_agenda(agenda, p,i)
        # print
        agendas.append(agenda)

    show(p)

    # Get request parameters from chatbot

    meeting_params = {'time_frame' : datetime.timedelta(days = 1),
    'duration' : datetime.timedelta(hours = 2)}

    # Send request and compute answer
    print get_meeting_slot(agendas, meeting_params)


