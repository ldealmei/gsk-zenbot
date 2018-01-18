import uuid

class Project():
    """
    Project Class
    """
    def __init__(self, people_dict, deadline, tasks = [], description = ''):
        self.project_id=uuid.uuid4()
        self.people_dict = people_dict
        self.tasks = tasks # List of Tasks
        self.deadline = deadline #datetime object
        self.description = description

    def report(self):
        #TODO
        pass