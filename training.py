from Event import Meeting, Training
import pandas as pd
from Zenbot import Zenbot

def get_trainings():
	return pd.read_excel('GSK DATA/Personal Assistant/Training Matrix_test.xlsx')

def show_all_courses():
	df = get_trainings()
	return df['Item Title'].unique()

def show_all_past_trainings():
	df = get_trainings()
	return df.loc[df['Completion Status'].str.endswith('_C', na=False)]

def show_past_trainings_user(user):
	df = get_trainings()
	return df.loc[show_all_past_trainings()['Name'].str.contains(user)]

def show_upcoming_trainings():
	pass

def show_deadline():
	pass

def show_state_trainings():
	pass


if __name__ == '__main___':
	x = show_past_trainings_user()
