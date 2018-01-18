import pandas as pd
import uuid
import datetime
import Task
import Schedule
import Project
from Event import Training, Meeting

#zenbot avatar
class Zenbot(object):
	def __init__ (self, params):
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
	def add_task(self, zenbotid, params):
		newtask = Task(params)
		if zenbotid == self.zenbotid:
			self.tasks.append(newtask)
			self.schedule()
		else:
			pass

	#collects events of the day, most important tasks, and creates a schedule from them
	# def schedule(self):
	# 	t = datetime.datetime.today()
	# 	lastmomenttoday = datetime.datetime(t.year, t.month, t.day+1, 0, 0, 0)
	# 	eventstoday = [event for event in self.events if event.start < lastmomenttoday and event.start > t]
	# 	taskstoday = prioritisetasks()
	# 	self.schedule = Schedule(eventstoday, taskstoday)

	#for every key in self.required_certifications, check if it is in self.certifications & up to date. If not either of these, create a training object
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

	#analyse zenbots stats that are relevant for current actions & evaluation
	def current_analysis(self):
		ach = self.achieved_analysis()
		at = self.at_risk_analysis()
		ov = self.overdue_analysis()
		return([ach, at, ov])


	#three functions that return particular statistics: achieved_analysis for tasks achieved that have a deadline in the last 7 days or in the future
	def achieved_analysis(self):
		# achieved_tasks = [[task.description['title'], task.deadline, task.completed, task.estim_dur, task.time_spent, task.effort, task['description']] for task in self.tasks if task.deadline > task.date_completed and task.deadline + datetime.timedelta(days = 7) > datetime.datetime.today())]
		# achieved_df = pd.DataFrame(achieved_tasks)
		# achieved_df.columns = ['title','deadline', 'time completed' ,'estim_dur', 'time_spent', 'effort', 'description']
		# achieved_df['time difference (hours)'] = achieved_df['time_spent']/achieved_df['time_spent'] - achieved_df['estim_dur']
		# achieved_df['time difference (percent)'] = achieved_df['time_spent']/achieved_df['estim_dur'] * 100

		# return(achieved_df)
		return

	#identifies tasks that are at risk of not being completed on time
	def at_risk_analysis(self):
		# at_risk_tasks = [[task.description['title'], task.deadline, task.progress, ', '.join(task.dependency_of), task.estim_dur, task.time_spent, task.['description'] ] for task in self.tasks if (task.deadline - datetime.datetime.today() <  3*task.progress*task.dur_estim)]
		# at_risk_df = pd.DataFrame(at_risk_tasks)
		# at_risk_df.columns = ['title', 'deadline', 'progress', 'dependency_of', 'estim_dur', 'time_spent', 'description']
		# at_risk_df['time difference (hours)'] = at_risk_df['time_spent']/at_risk_df['time_spent'] - at_risk_df['estim_dur']
		# at_risk_df['time difference (percent)'] = at_risk_df['time_spent']/at_risk_df['estim_dur'] * 100
		# at_risk_df['remaining time'] = (1 - at_risk_df['progress']) * at_risk_df['estim_dur']
		# at_risk_df['remaining time recalibrated'] = (1 - at_risk_df['progress']) * at_risk_df['time_spent']
		# return(at_risk_df)
		return

	# identifies tasks that are already overdue
	def overdue_analysis(self):
		# overdue_tasks = [[task.description['title'], task.deadline, task.progress, ', '.join(task.dependency_of), task.estim_dur, task.time_spent, task.['description'] ] for task in self.tasks if task.deadline < datetime.datetime.today() and task.progress < 1]
		# overdue_df = pd.DataFrame(overdue_tasks)
		# overdue_df.columns = ['title', 'deadline', 'progress', 'dependency_of', 'estim_dur', 'time_spent', 'description']
		# overdue_df['time difference (hours)'] = overdue_df['time_spent']/overdue_df['time_spent'] - overdue['estim_dur']
		# overdue_df['time difference (percent)'] = overdue_df['time_spent']/overdue_df['estim_dur'] * 100
		# overdue_df['remaining time'] = (1 - overdue_df['progress']) * overdue_df['estim_dur']
		# overdue_df['remaining time recalibrated'] = (1 - overdue_df['progress']) * overdue_df['time_spent']

		# return(overdue_df)
		return

	#removes tasks and events older than 30 days and then creates data for events and tasks with deadlines before now.
	def report_past(self):
		# remove_old(days = 30, tasks = True, events = True)
        #
		# past_tasks = [[task.description['title'], task.deadline, task.completed, task.estim_dur, task.time_spent, task.effort, task['description'] for task in self.tasks if task.deadline < datetime.datetime.today()]
		#
		# past_df = pd.DataFrame(past_tasks)
		# past_df.columns = ['title','deadline', 'time completed' ,'estim_dur', 'time_spent', 'effort', 'description']
		# past_df['time difference (hours)'] = past_df['time_spent']/past_df['time_spent'] - past_df['estim_dur']
		# past_df['time difference (percent)'] = past_df['time_spent']/past_df['estim_dur'] * 100

		# return [past_df]
		return

	def make_today_schedule(self):

		events = [event for event in self.events if datetime.datetime.today.date() == event.start.date()]

		time_available = datetime.timedelta(hours=8) - sum([ev.end - ev.start for ev in events], datetime.timedelta(0))

		tasks = [self._ranking_function(task) for task in self.tasks]

		return Schedule(events, self._select_tasks(tasks, time_available))

	def _select_tasks(self, tasks, time_available):
		# TODO: ASSUMPTION : Tasks are small (a task cannot be more than 2-3 hour long)

		selection = []

		for task in tasks:
			if time_available - (task.dur_estim) > datetime.timedelta(0):
				selection.append(task)
				time_available = time_available - (task.dur_estim)

		return selection

	def _get_threshold(self, Task):
		# TODO: Make sense of this - super arbitrary

		# simple linear relation to effort and importance
		return Task.effort * Task.importance  # expressed in days

	def _get_urgency(self, Task):
		# on a scale 1-10

		time_left = datetime.datetime.today() - Task.deadline
		time_needed = (1 - Task.progress) * Task.dur_estim

		if (time_left.days - time_needed.days) < self._get_threshold(self, Task):
			return 10 - (10.0 / self._get_threshold(self, Task)) * (time_left.days - time_needed.days)
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


	def arrange_meetings(self, datetime, listofattendees, projectid, importance = 5, urgency = 5):
		pass


	#removes either tasks or events or both from object that are older than days
	def remove_old(self, days = 30, tasks = True, events = True):
		if tasks:
			self.tasks = [task for task in self.task if task.completed + datetime.timedelta(days = days) > datetime.datetime.today()]
		if events:
			self.events = [event for event in self.events if event.ed + datetime.timedelta(days = days) > datetime.datetime.today()]


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
		# Task.progress = float(input('Please enter your progress on the task {0} as a number between 0 and 100.').format(Task.description['title'])/100
		# Hours = float(input('Please enter the time you spent on this task today in hours, e.g. 6.5 h for 6 hours, 30 minutes.'))
		# Task.time_spent += datetime.timedelta(hours = Hours)
        #
		# Task.effort.append(float(input('Please enter as how effortful you experienced working on this task, as a number between 0 and 5.').format(Task.description['title'])/5)

		pass











