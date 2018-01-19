import pandas as pd
import uuid
import datetime
from Task import Task
from Schedule import Schedule
from Event import Training, Meeting
import numpy as np


# zenbot avatar
class Zenbot(object):
    zenbot_dict = dict()
    people_dict = dict()

    def __init__(self, owner, events, tasks):
        # dictionary of personal id
        self.owner = owner
        self.zenbotid = str(uuid.uuid4())
        Zenbot.zenbot_dict[self.zenbotid] = 'None'
        Zenbot.people_dict[owner['name']] = self.zenbotid
        # level1: just zenbot itself and administrator. level 2: direct supervisors, set tasks and see everything,
        # level 3: see user level aggregates only, no access req: see events (still not displayed to humans)
        # possible level 4: see team/project aggregates only
        self.accessdict = {'level1': [self.zenbotid, 'Z3N'], 'level2': [], 'level3': []}
        # the following four must come from apis or something
        self.certifications = {}
        self.requiredcertifications = {}
        self.events = events
        self.tasks = tasks
        self.schedule = None

    def report_info(self, asker_zenbotid):
        if asker_zenbotid in self.accessdict['level1'] or asker_zenbotid in self.accessdict[
            'level2'] or asker_zenbotid in self.accessdict['level3']:
            return ({'tasks': self.report_tasks(asker_zenbotid), 'events': self.report_events(asker_zenbotid),
                     'trainings': self.report_trainings(asker_zenbotid),
                     'certifications': self.report_certifications(asker_zenbotid),
                     'requiredcertifications': self.report_requiredcertifications(asker_zenbotid)})

    # creates a task and adds it to its list of tasks if appropriate
    def add_task(self, zenbotid,  adder_id, project_id=123456, deadline=datetime.datetime(2020, 2, 1, 0, 0, 0),
                 dur_estim=datetime.timedelta(days=1), importance=1, effort=2, category='type1',
                 description={'title': 'task1', 'description': 'do this'}):
        print(adder_id)
        newtask = Task(project_id=project_id, deadline=deadline, creator=adder_id, dur_estim=dur_estim,
                       importance=importance, effort=effort, category=category, description=description)
        asker_zenbotid = adder_id
        if zenbotid in self.accessdict['level1'] or asker_zenbotid in self.accessdict['level2']:
            self.tasks.append(newtask)
        else:
            pass

    def generate_timesheet(self):
        pass

    def report_trainings(self, asker_zenbotid):
        training_list = []
        if asker_zenbotid in self.accessdict['level1'] or asker_zenbotid in self.accessdict[
            'level2'] or asker_zenbotid in self.accessdict['level3']:
            for event in self.events:
                if type(event) == Training:
                    training_list.append(event)
        return (training_list)

    def report_events(self, asker_zenbotid):
        if asker_zenbotid in self.accessdict['level1'] or asker_zenbotid in self.accessdict[
            'level2'] or asker_zenbotid in self.accessdict['level3']:
            return (self.events)
        else:
            return None

    def report_certifications(self, asker_zenbotid):
        if asker_zenbotid in self.accessdict['level1'] or asker_zenbotid in self.accessdict[
            'level2'] or asker_zenbotid in self.accessdict['level3']:
            return (self.certifications)
        else:
            return None

    def report_requiredcertifications(self, asker_zenbotid):
        if asker_zenbotid in self.accessdict['level1'] or asker_zenbotid in self.accessdict[
            'level2'] or asker_zenbotid in self.accessdict['level3']:
            return (self.requiredcertifications)
        else:
            return None

    def report_tasks(self, asker_zenbotid):
        df = self.generate_df()

        if asker_zenbotid in self.accessdict['level1'] or asker_zenbotid in self.accessdict[
            'level2'] or asker_zenbotid in self.accessdict['level3']:
            return (df)
        else:
            return None

    # lets a person A grant person B access to person C, but not to the same level as themselves
    def grant_access(self, access_for_zenbotid, access_to_zenbotid, level='level3'):
        print(access_to_zenbotid in Zenbot.zenbot_dict)
        zenbot = Zenbot.zenbot_dict.get(access_to_zenbotid)
        print(zenbot)
        if self.zenbotid in zenbot.accessdict['level1']:
            if level != 'level1':
                zenbot.accessdict[level].append(access_for_zenbotid)
        elif self.zenbotid in zenbot.accessdict['level2']:
            if level not in ['level1', 'level2']:
                zenbot.accessdict[level].append(access_for_zenbotid)
        else:
            print('You are not permitted to grant access to {}.'.format(access_to_zenbotid))

    def check(self, asker_zenbotid):
        if asker_zenbotid in self.accessdict['level1']:
            return (vars(self.zenbot))

    def make_today_schedule(self):

        events = [event for event in self.events if datetime.datetime.today.date() == event.start.date()]

        time_available = datetime.timedelta(hours=8) - sum([ev.end - ev.start for ev in events], datetime.timedelta(0))

        tasks_scored = [{'task': task, 'score': self._ranking_function(task)} for task in self.tasks]

        return Schedule(events, self._select_tasks(tasks_scored, time_available))

    def _select_tasks(self, tasks, time_available):
        # TODO: ASSUMPTION : Tasks are small (a task cannot be more than 2-3 hour long)

        selection = []

        ranks = np.argsort([t['score'] for t in tasks])

        for r in ranks:
            task = tasks[r]
            if time_available - (task['task'].dur_estim) > datetime.timedelta(0):
                selection.append(task['task'])
                time_available = time_available - (task['task'].dur_estim)

        return selection

    def _get_threshold(self, Task):
        # TODO: Make sense of this - super arbitrary

        # simple linear relation to effort and importance
        return Task.effort * Task.importance  # expressed in days

    def _get_urgency(self, Task):
        # on a scale 1-10

        time_left = datetime.datetime.today() - Task.deadline
        time_needed = (1 - Task.progress) * Task.dur_estim

        if (time_left.days - time_needed.days) < self._get_threshold(Task):
            return 10 - (10.0 / (self._get_threshold(Task) + 1) * (time_left.days - time_needed.days) + 1)
        else:
            return 0

    def _ranking_function(self, Task):
        # Ideally this function would be a machine learning algorithm that evolves based on the results

        # proxy value to urgency
        urgency = self._get_urgency(Task)

        # value due to the number of tasks it blocks (and their importance)
        if len(Task.dependency_of) > 5:
            pivotal_points = 5
        else:
            pivotal_points = len(Task.dependency_of)

        return urgency + pivotal_points

    # for every key in self.required_certifications, check if it is in self.certifications & up to date. If not either of these, create a training object
    def new_trainings(self):
        co = False
        for cert in self.requiredcertifications:
            if cert in self.certifications:  # this only adds the has expired
                if self.certifications[cert] > self.requiredcertifications[cert]:
                    print(self.certifications[cert])
                    pass
                else:
                    print(cert)
                    co = True
                    training_task = Task(project_id=111111,
                                         deadline=datetime.datetime.today() + datetime.timedelta(days=7),
                                         creator=self.zenbotid, dur_estim=datetime.timedelta(seconds=600), importance=2,
                                         effort=0, category='training', description={'title': cert, 'description': str(
                            self.requiredcertifications[cert])})
            else:
                print(cert)
                co = True
                training_task = Task(project_id=111111, deadline=datetime.datetime.today() + datetime.timedelta(days=7),
                                     creator=self.zenbotid, dur_estim=datetime.timedelta(seconds=600), importance=2,
                                     effort=0, category='training',
                                     description={'title': cert, 'description': str(self.requiredcertifications[cert])})

            if co:
                # print('Added task for ' + cert)
                self.tasks.append(training_task)

    # analyse zenbots stats that are relevant for current actions & evaluation
    def generate_df(self):

        self.remove_old()

        tasklist = [[task.description['title'], task.project_id, task.category, task.progress, task.deadline,
                     task.date_completed, task.dur_estim, task.time_on_task, task.effort,
                     ' | '.join(task.dependency_of), task.description['description']] for task in self.tasks]
        if len(tasklist):
            task_df = pd.DataFrame(tasklist)
            task_df.columns = ['title', 'project_id', 'category', 'progress', 'deadline', 'date_completed', 'dur_estim',
                               'time_on_task', 'effort', 'dependency_of', 'description']

            now = datetime.datetime.today()
            overdue = [x - now for x in task_df['deadline']]
            at_risk = [x - now for x in task_df['deadline']]

            task_df['remaining_time'] = task_df['progress'] * task_df['dur_estim']

            task_df['completed'] = 1 if task_df['progress'].tolist() == 1 else 0
            task_df['overdue'] = task_df['deadline'].apply(
                lambda x: 1 if x - now < datetime.timedelta(seconds=0) else 0)
            task_df['at_risk'] = task_df['deadline'].apply(lambda x: 1 if x - now < datetime.timedelta(days=5) else 0)
            task_df = task_df.sort_values(by='deadline').reset_index(drop=True)
        else:
            task_df = None

        return (task_df)

    def arrange_meetings(self, datetime, listofattendees, project_id, importance=5, urgency=5):
        pass

    # removes either tasks or events or both from object that are older than days
    def remove_old(self, Days=30, tasks=True, events=True):
        if len(self.tasks):
            self.tasks = [task for task in self.tasks if
                          task.date_completed is None or task.date_completed + datetime.timedelta(
                              days=30) > datetime.datetime.today()]
        if len(self.events):
            self.events = [event for event in self.events if
                           event.end is not None or event.end + datetime.timedelta(days=30) > datetime.datetime.today()]


