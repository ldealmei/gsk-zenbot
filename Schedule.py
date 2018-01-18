import datetime

class Schedule :
    """
    Schedule class
    """

    def __init__(self, events =[], tasks=[]):
        self.date = datetime.datetime.today()
        self.events = events
        self.tasks = tasks

        self.workload = self.get_workload(self.events, self.tasks)

    def get_workload(self):
        #TODO : Compute workload based on the schedule
        return 
