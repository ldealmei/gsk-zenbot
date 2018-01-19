import kivy
kivy.require('1.9.0')


from kivy.app import App
from kivy.uix.gridlayout import GridLayout
#from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.listview import ListView
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from functools import partial
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore

import datetime
import csv, json
import os, time
import webbrowser
from demo import test_schedule 
from Event import Training, Meeting

class Menu(Screen): #
### keep register for another thing
    def registered(self):
        content= Button(text='Scores Saved', text_size=(None, None))
        popup = Popup(title="What's on today", content=content,  auto_dismiss=False, size_hint=(0.40,0.40))
        content.bind(on_press=popup.dismiss)
        popup.open()
    
    def my_dashboard(self):
        webbrowser.open('file:///Users/ldealmei/Desktop/GSK%20Hack%20Days/user_training_view.html')

    def my_team(self):
	webbrowser.open('file:///Users/ldealmei/Desktop/GSK%20Hack%20Days/team_overview.html')

    def my_capman(self):
        webbrowser.open('file:///Users/ldealmei/Desktop/GSK%20Hack%20Days/user_cap_man.html')

# Help from: http://stackoverflow.com/questions/23789358/keyerror-stopping-app-in-kivy

    def exit(self):
        App.get_running_app().stop()

class Planner(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.box.add_widget(Label(text="My Agenda Today:", color=(0,0,0,1), font_name="Roboto-BoldItalic.ttf" ))
        self.box1.add_widget(Label(text=datetime.datetime.now().strftime("%d/%m/%Y"), color=(0,0,0,1)))
 
        my_day_event = test_schedule.events        
        my_day_task = test_schedule.tasks
        container = GridLayout(cols=2)
        container2 = GridLayout(cols=1)
        self.box3.add_widget(Label(text='My Events',  color=(0,0,0,1),font_name="Roboto-BoldItalic.ttf" , underline=True))
        for row in range(len(my_day_event)):
            container.add_widget(Label(text=str(my_day_event[row].start.hour)+':00', color=(0,0,0,1)))
            if isinstance(my_day_event[row], Training):
                text=my_day_event[row].certification
            elif isinstance(my_day_event[row], Meeting):
                text=str(my_day_event[row].project_id)
            container.add_widget(Label(text=text, color=(0,0,0,1)))
        self.box2.add_widget(container)
        self.box4.add_widget(Label(text='My Tasks', color=(0,0,0,1),font_name="Roboto-BoldItalic.ttf"))
        for row in range(len(my_day_task)):
            container2.add_widget(Label(text=my_day_task[row].category, color=(0,0,0,1)))
        
        self.box5.add_widget(container2)



#    def calendar():
#        return

class MyTeam(Screen):
    def myteam(self):
        return

class CapMan(Screen):
    def capman(self):
        return

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Menu(name='menu'))
        sm.add_widget(Planner(name='planner'))
        #sm.add_widget(CapMan(name='capman'))
        #sm.add_widget(MyTeam(name='myteam'))
        #sm.add_widget(Leaderboard(name='leaderboard'))
        return sm #Menu()



MyApp().run()
