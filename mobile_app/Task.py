import uuid
import datetime

class Task:

    def __init__(self, project_id, deadline, creator, dur_estim, importance, effort, category,  description= {}):
        self.task_id = uuid.uuid4()
        self.progress = 0
        self.time_on_task = datetime.timedelta(0)
        self.dependent_on = [] # list of Task_id
        self.dependency_of = [] # list of Task_id

        self.date_completed = None

        self.project_id = project_id
        self.description = description # description string
        self.deadline = deadline  # datetime object
        self.created_by = creator # bot_id
        self.dur_estim = dur_estim #timedelta object
        self.importance = importance  # on a scale 1-3
        self.effort = effort  # on a scale 1-5
        self.category = category # user-defined category

    def prettify(self):
        args = [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))]

        print(self)
        for arg in args :
            print('  ' + arg + ' : ' , getattr(self, arg))

    def assign_to_project(self):
        #TODO
        pass

