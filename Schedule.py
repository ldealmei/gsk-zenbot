import datetime

class Schedule :
    """
    Schedule class
    """

    def __init__(self, events =[], tasks=[]):
        self.date = datetime.datetime.today()
        self.events = events
        self.tasks = tasks
