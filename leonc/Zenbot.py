import uuid
import datetime

class Zenbot(object):
	def __init__ (self, personalid):
		self.personalid = personalid
		self.zenbotid = uuid.uuid4()
		self.accessdict = {'level1': zenbotid}
		self.certifications = {}
		self.requiredcertifications = {}
		self.events = []
		self.tasks = []
		self.schedule = None

	def add_task(self, params):
		newtask = Task(params)
		self.tasks.append(newtask)
		self.schedule()

	def schedule(self):
		t = datetime.datetime.today()
		lastmomenttoday = datetime.datetime(t.year, t.month, t.day+1, 0, 0, 0)
		eventstoday = [event for event in self.events if event.start < lastmomenttoday and event.start > t]
		taskstoday = prioritisetasks()
		self.schedule = Schedule(eventstoday, taskstoday)

	def new_trainings(self):
		for cert in self.requiredcertifications:
			if cert in self.certifications:			#this only adds the training once the certification has expired
				if self.certifications[cert] > self.requiredcertifications[cert]:
					pass
				else:
					training = Training(cert)
			else:
				training = Training(cert)

		if training:
			self.events.append(training)


	def report_current(self):
		taskstats = []
		for task in self.tasks:
			taskstats.append([task.task_id, task.projec_id, task.deadline, task.progress, task.dur_estim, task.time_spent])

														#project deadline has passed and progess less than complete
		overdue_tasks = [task for task in self.tasks if task.deadline < datetime.datetime.today() and task.progress < 1]
														#the difference between the deadline and now is smaller than a third of the estimated remaining time
		at_risk_tasks = [task for task in self.tasks if (task.deadline - datetime.datetime.today() <  3*task.progress*task.dur_estim)]

		achieved_tasks = [task for task in self.tasks if task.deadline + datetime.timedelta(days = 5) > datetime.datetime.today() and task.progress == 1]

		return([overdue_tasks, at_risk_tasks, achieved_tasks])





	def report_last_month(self):






	def prioritise_tasks(self):
		


	def arrange_meetings(self, datetime, listofattendees, importance = 5, urgency = 5, projectid):


	def remove_old(self, tasks = True, events = True):


	def get_feedback(self):
		for task in self.schedule.tasks:
			get_feedback_on_task(task)
		for event in self.schedule.events:
			get_feedback_on_event(event)


	def get_feedback_on_event(self, Event):
		Event.attended = bool(input('Did you attend this event, {}? Please enter 1 if yes and 0 otherwise'.format(Event.description['title'])))

	def get_feedback_on_task(self, Task):
		Task.progress = float(input('Please enter your progress on the task {0} as a number between 0 and 100.').format(Task.description['title'])/100
		Hours = float(input('Please enter the time you spent on this task today in hours, e.g. 6.5 h for 6 hours, 30 minutes.'))
		Task.time_spent += datetime.timedelta(hours = Hours)












