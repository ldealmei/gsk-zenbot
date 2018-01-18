
	#three functions that return particular statistics: achieved_analysis for tasks achieved that have a deadline in the last 7 days or in the future
	def achieved_analysis(self):
		achieved_tasks = [[task.description['title'], task.category, task.deadline, task.completed, task.estim_dur, task.time_spent, task.effort, task['description']] for task in self.tasks if task.deadline > task.date_completed and task.deadline + datetime.timedelta(days = 7) > datetime.datetime.today()]
		achieved_df = pd.DataFrame(achieved_tasks)
		achieved_df.columns = ['title','task category', 'deadline', 'time completed' ,'estim_dur', 'time_spent', 'effort', 'description']
		achieved_df['time difference (hours)'] = achieved_df['time_spent']/achieved_df['time_spent'] - achieved_df['estim_dur']
		achieved_df['time difference (percent)'] = achieved_df['time_spent']/achieved_df['estim_dur'] * 100

		return(achieved_df)
		
	#identifies tasks that are at risk of not being completed on time
	def at_risk_analysis(self):
		at_risk_tasks = [[task.description['title'], task.deadline, task.progress, ', '.join(task.dependency_of), task.estim_dur, task.time_spent, task['description'] ] for task in self.tasks if (task.deadline - datetime.datetime.today() <  3*task.progress*task.dur_estim)]
		at_risk_df = pd.DataFrame(at_risk_tasks)
		at_risk_df.columns = ['title', 'deadline', 'progress', 'dependency_of', 'estim_dur', 'time_spent', 'description']
		at_risk_df['time difference (hours)'] = at_risk_df['time_spent']/at_risk_df['time_spent'] - at_risk_df['estim_dur']
		at_risk_df['time difference (percent)'] = at_risk_df['time_spent']/at_risk_df['estim_dur'] * 100
		at_risk_df['remaining time'] = (1 - at_risk_df['progress']) * at_risk_df['estim_dur']
		at_risk_df['remaining time recalibrated'] = (1 - at_risk_df['progress']) * at_risk_df['time_spent']
		return(at_risk_df)
		

	def make_schedule(self):
		t = datetime.datetime.today()
		lastmomenttoday = datetime.datetime(t.year, t.month, t.day+1, 0, 0, 0)
		eventstoday = [event for event in self.events if event.start < lastmomenttoday and event.start > t]
		time_available = datetime.timedelta(hours=8) - sum([ev.end - ev.start for ev in eventstoday], datetime.timedelta(0))

		Tasks = [self._ranking_function(task) for task in self.tasks]
		taskstoday = _select_tasks(Tasks, time_available)
		self.schedule = Schedule(eventstoday, taskstoday)

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
		pass

	#removes tasks and events older than 30 days and then creates data for events and tasks with deadlines before now.
	def report_past(self):
		# remove_old(days = 30, tasks = True, events = True)
		#
		# past_tasks = [[task.description['title'], task.category, task.deadline, task.completed, task.estim_dur, task.time_spent, task.effort, task['description'] for task in self.tasks if task.deadline < datetime.datetime.today()]
		#
		# past_df = pd.DataFrame(past_tasks)
		# past_df.columns = ['title','deadline', task.category, 'time completed' ,'estim_dur', 'time_spent', 'effort', 'description']
		# past_df['time difference (hours)'] = past_df['time_spent']/past_df['time_spent'] - past_df['estim_dur']
		# past_df['time difference (percent)'] = past_df['time_spent']/past_df['estim_dur'] * 100

		# return [past_df]
		pass