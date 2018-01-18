import pandas as pd
import uuid
import datetime
from Task import Task
from Schedule import Schedule
import Project
from Event import Training, Meeting

#zenbot avatar
class Zenbot(object):
	def __init__ (self,params):
		# dictionary of personal id
		self.personal_id = params['id']
		self.zenbotid = uuid.uuid4()
		#unclear how access is granted to new bots
		self.accessdict = {'level1': self.zenbotid}
		# the following four must come from apis or something
		self.certifications = {}
		self.requiredcertifications = {}
		self.events = params['events']
		self.tasks = params['tasks']
		self.schedule = None


	#creates a task and adds it to its list of tasks if appropriate
	def add_task(self, zenbotid):
		newtask = Task(project_id =123456, deadline = datetime.datetime(2020,2,1,0,0,0), creator = self.zenbotid, dur_estim = datetime.timedelta(days = 1), importance = 1, effort = 2, category = 'type1', description = {'title': 'task1', 'description':'body'})
		if zenbotid == self.zenbotid:
			self.tasks.append(newtask)
		else:
			pass

	#DEPRECATED collects events of the day, most important tasks, and creates a schedule from them


	#for every key in self.required_certifications, check if it is in self.certifications & up to date. If not either of these, create a training object
	def new_trainings(self):
		co = False
		for cert in self.requiredcertifications:
			if cert in self.certifications:			#this only adds the has expired
				if self.certifications[cert] > self.requiredcertifications[cert]:
					print(self.certifications[cert])
					pass
				else:
					print(cert)
					co = True
					training_task = Task(project_id = 111111, deadline = datetime.datetime.today() + datetime.timedelta(days = 7), creator = self.zenbotid, dur_estim = datetime.timedelta(seconds = 600), importance = 2, effort = 0, category = 'training',  description= {'title': cert , 'description': str(self.requiredcertifications[cert])})
			else:
				print(cert)
				co = True
				training_task = Task(project_id = 111111, deadline = datetime.datetime.today() + datetime.timedelta(days = 7), creator = self.zenbotid, dur_estim = datetime.timedelta(seconds = 600), importance = 2, effort = 0, category = 'training',  description= {'title': cert , 'description': str(self.requiredcertifications[cert])})
			
			if co:
				#print('Added task for ' + cert)
				self.tasks.append(training_task)


	#analyse zenbots stats that are relevant for current actions & evaluation
	def generate_df(self):

		self.remove_old()

		tasklist = [[task.description['title'], task.project_id, task.category, task.progress, task.deadline, task.date_completed, task.dur_estim, task.time_on_task, task.effort, ' | '.join(task.dependency_of), task.description['description']] for task in self.tasks]
		task_df = pd.DataFrame(tasklist)
		print(tasklist)
		task_df.columns = ['title', 'project_id', 'category', 'progress', 'deadline', 'date_completed', 'dur_estim', 'time_on_task', 'effort', 'dependency_of', 'description']

		now = datetime.datetime.today()
		overdue = [x - now for x in task_df['deadline']]
		at_risk = [x - now for x in task_df['deadline']]

		task_df['remaining_time'] = task_df['progress'] * task_df['dur_estim']

		task_df['completed'] = 1 if task_df['progress'].tolist() == 1 else 0
		task_df['overdue'] = task_df['deadline'].apply(lambda x: 1 if x - now < datetime.timedelta(seconds = 0) else 0)
		task_df['at_risk'] = task_df['deadline'].apply(lambda x: 1 if x - now < datetime.timedelta(days = 5) else 0)

		return(task_df)





	def arrange_meetings(self, datetime, listofattendees, project_id, importance = 5, urgency = 5):
		pass


	#removes either tasks or events or both from object that are older than days
	def remove_old(self, Days = 30, tasks = True, events = True):
		print(len(self.tasks))
		if len(self.tasks):
			self.tasks = [task for task in self.tasks if task.date_completed is None or task.date_completed + datetime.timedelta(days = 30) > datetime.datetime.today()]
		if len(self.events):
			self.events = [event for event in self.events if event.end is not None or event.end + datetime.timedelta(days = 30) > datetime.datetime.today()]


	#get feedback from user and feed data into task and event objects
	def get_feedback(self):
		for task in self.schedule.tasks:
			self.get_feedback_on_task(task)
		for event in self.schedule.events:
			self.get_feedback_on_event(event)

	#get boolean on attendance
	def get_feedback_on_event(self, Event):
		Event.attended = bool(input('Did you attend this event, {}? Please enter 1 if yes and 0 otherwise'.format(Event.description['title'])))

	#get feedback on progress on task, the time spent on it, how much effort it took to work on it today (this can be averaged later)
	def get_feedback_on_task(self, Task):
		#Task.progress = float(input('Please enter your progress on the task {0} as a number between 0 and 100.').format(Task.description['title'])/100
		#Hours = float(input('Please enter the time you spent on this task today in hours, e.g. 6.5 h for 6 hours, 30 minutes.'))
		#Task.time_spent += datetime.timedelta(hours = Hours)
		#
		#Task.effort.append(float(input('Please enter as how effortful you experienced working on this task, as a number between 0 and 5.').format(Task.description['title'])/5)

		pass


