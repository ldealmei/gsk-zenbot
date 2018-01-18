import uuid
import datetime

class Task:

    def __init__(self, project_id, deadline, creator, dur_estim, priority, effort, description= {}):
        self.task_id = uuid.uuid4()
        self.progress = 0.0
        self.time_on_task = datetime.timedelta(0)
        self.actors = [] #list of bot_ids
        self.dependent_on = [] # list of Task objects
        self.date_completed = None

        self.project_id = project_id
        self.description = description # description string
        self.deadline = deadline  # datetime object
        self.created_by = creator # bot_id
        self.dur_estim = dur_estim #timedelta object
        self.priority = priority
        self.effort = effort

    def assign_to_project(self):
        #TODO
        pass

