from Schedule import Schedule
from Event import Training, Meeting
import datetime
import uuid
import random

def get_random_cert() :
    cert = ''

    with open('training_courses.txt') as f :
        courses = f.readlines()
        while len(cert)<5 :  # sure its not an empty line
            cert = courses[random.randint(0,len(courses))]

    return cert


events = [Training(datetime.datetime(year = 2018, month=1, day= 18, hour = 8),
                   datetime.datetime(year = 2018, month=1, day= 18, hour = 12), {}, get_random_cert()),
          Meeting(datetime.datetime(year = 2018, month=1, day= 18, hour = 13),
                  datetime.datetime(year = 2018, month=1, day= 18, hour = 14), {}, uuid.uuid4(), [], tasks=[]),
          Meeting(datetime.datetime(year=2018, month=1, day=18, hour=15),
                  datetime.datetime(year=2018, month=1, day=18, hour=17), {}, uuid.uuid4(), [], tasks=[])]
tasks = []

test_schedule = Schedule(events =events, tasks=tasks)

