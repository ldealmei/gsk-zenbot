import uuid
import pandas as pd
from Zenbot_demo import Zenbot
Zenbot_master = Zenbot(owner = {'name':000000}, events =[], tasks = [])


class Team(object):
	def __init__ (self, creator_id, zenbot_ids, description = ''):
		self.team_id = str(uuid.uuid4())
		self.creator = creator_id
		self.zenbot_ids = zenbot_ids
		self.description = description
		self.accessdict= {'level1':['Z3N', creator_id], 'level2':[], 'level3':[]}


	def report_tasks(self, caller_zenbotid, zenbotids_tocall = []):
		report = dict()
		if len(zenbotids_tocall) == 0:
			zenbotids_tocall= self.zenbot_ids
		if caller_zenbotid in self.accessdict['level1'] or caller_zenbotid in self.accessdict['level2']:
			for zenbotid in zenbotids_tocall:
				zenbot = Zenbot.zenbot_dict[zenbotid]
				report[zenbotid] = zenbot.report_tasks(caller_zenbotid)
		else:
			report = None

		return (report)

	#returns a dataframe of the tasks in the team
	def report_tasks_aggregate(self, caller_zenbotid, zenbotids_tocall = []):
		task_report = pd.DataFrame()
		if len(zenbotids_tocall) == 0:
			zenbotids_tocall= self.zenbot_ids

		if caller_zenbotid in self.accessdict['level1'] or caller_zenbotid in self.accessdict['level2'] or (caller_zenbotid in self.accessdict['level3'] and len(zenbotids_tocall) > 1):
			report = self.report_tasks(caller_zenbotid)

			#TODO change this
			n = 0
			for zenbotid in zenbotids_tocall:
				if n == 0:
					task_report = report[zenbotid]
					n += 1
				else:
					task_report = task_report.append(report[zenbotid])

			task_report.append(list(report.values()))
			#task_report.columns = ['title', 'project_id', 'category', 'progress', 'deadline', 'date_completed', 'dur_estim', 'time_on_task', 'effort', 'dependency_of', 'description', 'completed', 'overdue', 'at_risk']
			task_report = task_report.sort_values(by = 'deadline').reset_index(drop = True)
		else:
			task_report = None

		return (task_report)

	# returns a dict keys:zenbotids values:dicts keys:certifications, requiredcertifications values:dicts key:certification_name value:date_acquired/required
	def report_certificates(self, caller_zenbotid, zenbotids_tocall = []):
		certs = dict()
		if len(zenbotids_tocall) == 0:
			zenbotids_tocall= self.zenbot_ids
		if caller_zenbotid in self.accessdict['level1'] or caller_zenbotid in self.accessdict['level2'] or (caller_zenbotid in self.accessdict['level3'] and len(zenbotids_tocall) > 1):
			for zenbotid in zenbotids_tocall:
				zenbot = Zenbot.zenbot_dict[zenbotid]
				certs[zenbotid] = {'certifications': zenbot.report_certifications(caller_zenbotid), 'requiredcertifications': zenbot.report_requiredcertifications(caller_zenbotid)}

		return(certs)


	# returns a dict keys:zenbotids values:lists of events
	def report_events(self, caller_zenbotid, zenbotids_tocall = []):
		events = dict()
		if len(zenbotids_tocall) == 0:
			zenbotids_tocall= self.zenbot_ids
		if caller_zenbotid in self.accessdict['level1'] or caller_zenbotid in self.accessdict['level2'] or (caller_zenbotid in self.accessdict['level3'] and len(zenbotids_tocall) > 1):
			for zenbotid in zenbotids_tocall:
				zenbot = Zenbot.zenbot_dict[zenbotid]
				events[zenbotid] = zenbot.report_events(caller_zenbotid)

		return events

		return(certs)

	# returns a dict keys:zenbotids values:lists of trainings
	def report_trainings(self, caller_zenbotid, zenbotids_tocall = []):
		trainings = dict()
		if len(zenbotids_tocall) == 0:
			zenbotids_tocall= self.zenbot_ids
		if caller_zenbotid in self.accessdict['level1'] or caller_zenbotid in self.accessdict['level2'] or (caller_zenbotid in self.accessdict['level3'] and len(zenbotids_tocall) > 1):
			for zenbotid in zenbotids_tocall:
				zenbot = Zenbot.zenbot_dict[zenbotid]
				trainings[zenbotid] = zenbot.report_trainings()

		return (trainings)

	def report_by_individual(self, caller_zenbotid, zenbotids_tocall = []):
		report = dict()
		if len(zenbotids_tocall) == 0:
			zenbotids_tocall= self.zenbot_ids
		for zenbotid in zenbotids_tocall:
			zenbot = Zenbot.zenbot_dict[zenbotid]
			report[zenbotid] = zenbot.report_info(caller_zenbotid)

		return(report)