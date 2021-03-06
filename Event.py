class Event() :
    """
    Event class
    """
    def __init__(self, start, end, loc):

        self.start = start #datetime object
        self.end = end # datetime object
        self.loc = loc # object type to define - json

    def prettify(self):
        args = [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))]

        print(self)
        for arg in args :
            print('  ' + arg + ' : ' , getattr(self, arg))

class Meeting(Event):
    """
    Meeting class
    """

    def __init__(self, start, end, loc, project_id, participants, tasks= []):
        Event.__init__(self,start, end, loc)
        self.project_id = project_id
        self.required_tasks = tasks
        self.participants = participants #list of bot_ids

        self.attendees = [] #list of bot_ids

        # self.importance = importance
        # self.urgency = urgency

class Training(Event) :
    def __init__(self, start, end, loc, certification):
        Event.__init__(self,start, end, loc)
        self.certification = certification
        # self.last_certified = last_certified #datetime object
        # self.validity = validity # datetime object

        self.attended = False
