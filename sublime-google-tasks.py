import sublime, sublime_plugin
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

gservice=None
gtasklists=None
gtasklist=None
gtasks=None
gtask=None

settings = sublime.load_settings("sublime-google-tasks.sublime-settings")

class GoogleViewTasksCommand(sublime_plugin.WindowCommand):

	
	
	quick_panel_tasklists_selected_index=None

	def get_auth(self):

		global gservice
		client_id = settings.get("client_id")
		client_secret = settings.get("client_secret")
		user_agent = settings.get("user_agent")

		FLOW = OAuth2WebServerFlow(
			client_id=client_id,
			client_secret=client_secret,
			scope='https://www.googleapis.com/auth/tasks',
			user_agent=user_agent)
		storage = Storage('google-tasks.dat')
		credentials = storage.get()
		if credentials is None or credentials.invalid == True:
			credentials = run(FLOW, storage)

		http = httplib2.Http()
		http = credentials.authorize(http)
		gservice = build(serviceName='tasks', version='v1', http=http)
		return	


	def run(self, resetTaskLists=False, resetTasks=False):

		global gtasklists

		#auth once
		if gservice==None:
			self.get_auth()

		if gtasklists is None or resetTaskLists==True:
			gtasklists = gservice.tasklists().list(fields='items(id,title)').execute()

		self.tli = []
		self.tli.append([u'\u271A'+' Add a New TaskList'])

		try:
			for tasklist in gtasklists['items']:
				self.tli.append(['  '+tasklist['title']])
		except:
			pass

		if resetTasks==True:
			self.get_tasks(self.quick_panel_tasklists_selected_index)
			return

		self.window.show_quick_panel(self.tli, self.get_tasks, sublime.MONOSPACE_FONT)

		
	def get_tasks(self, idx):

		global gtasklist
		global gtasks

		if idx==-1:
			return

		if idx==0:
			self.window.run_command('google_add_tasklist_from_input')
			return

		self.quick_panel_tasklists_selected_index = idx

		gtasklist = gtasklists['items'][idx-1]

		self.ti=[]
		self.ti.append('  '+gtasklist['title'])
		self.ti.append([u'\u21b5'+' Back to TaskLists'])
		self.ti.append([u'\u270E'+' Edit TaskList'])
		self.ti.append([u'\u2715'+' Delete TaskList'])
		self.ti.append([u'\u25FB'+' Clear TaskList'])
		self.ti.append([u'\u271A'+' Add a Task'])
		
		gtasks = gservice.tasks().list(tasklist=gtasklist['id'], fields='items(completed,id,status,title)').execute()

		# show check symbol for completed tasks
		try:
		 	for task in gtasks['items']:
		 		if task['status']=='completed':
		 			self.ti.append(['  '+u'\u2714'+' '+task['title']])
		 		else:	
		 			self.ti.append(['    '+task['title']])
		except:
			pass

		self.window.show_quick_panel(self.ti, self.get_mod_task_options, sublime.MONOSPACE_FONT)


	def get_mod_task_options(self, idx):

		global gtask

		if (idx==-1 or idx==0):
			return
		#go back	
		if idx==1:
			self.window.show_quick_panel(self.tli, self.get_tasks, sublime.MONOSPACE_FONT)
			return
		#edit tasklist title	
		if idx==2:
			self.window.run_command('google_edit_tasklist_from_input')
			return

		#confirm deletion of tasklist	
		if idx==3:
			confirmlist = [['Yes','Yes - Delete TaskList'],['No','No - Oops, don\'t Delete TaskList']]
			self.window.show_quick_panel(confirmlist, self.del_tasklist_confirm, sublime.MONOSPACE_FONT)
			return

		#clear completed tasks - which basically just hides them for list
		if idx==4:
			gservice.tasks().clear(tasklist=gtasklist['id']).execute()
			self.window.run_command('google_view_tasks', {'resetTasks':True})
			return

		if idx==5:
			# self.window.run_command('google_add_task_from_input', {"tasklistitem": gtasklist['id']})
			self.window.run_command('google_add_task_from_input')
			return

		
		gtask = gtasks['items'][idx-6]
		self.tasktitle = gtask['title']

		if gtask['status']=='completed':
			self.mod_options = [self.tasktitle,u'\u21b5'+' Back to Tasks', u'\u25FB'+' Remove Check', u'\u270E'+' Edit', u'\u2715'+' Delete']
		else:
			self.mod_options = [self.tasktitle,u'\u21b5'+' Back to Tasks', u'\u2714'+' Completed', u'\u270E'+' Edit', u'\u2715'+' Delete']

		self.window.show_quick_panel(self.mod_options, self.mod_task, sublime.MONOSPACE_FONT)


	def del_tasklist_confirm(self,idx):

		global gtasklist

		if idx==-1:
			return
		if idx==0:
			gservice.tasklists().delete(tasklist=gtasklist['id']).execute()
			self.selectedtasklistidx=None
			gtasklist=None
			self.window.run_command('google_view_tasks', {'resetTaskLists':True})
			return
		if idx==1:
			self.window.show_quick_panel(self.tli, self.get_tasks, sublime.MONOSPACE_FONT)			
			return


	def mod_task(self, idx):
		
		global gtasklist
		global gtask

		if idx==-1:
			return

		# Go Back		
		if idx==1:
			self.window.show_quick_panel(self.ti, self.get_mod_task_options, sublime.MONOSPACE_FONT)

		# Complete or Clear Task	
		if idx==2:
			if gtask['status'] == 'completed':
				gtask['status'] = 'needsAction'
				gtask['completed'] = None
			else:
				gtask['status'] = 'completed'

			gservice.tasks().patch(tasklist=gtasklist['id'], task=gtask['id'], body=gtask).execute()
			self.get_tasks(self.quick_panel_tasklists_selected_index)

		# Edit Task
		if idx==3:
			self.window.run_command('google_edit_task_from_input')
		
		# Delete Task
		if idx==4:
			gservice.tasks().delete(tasklist=gtasklist['id'], task=gtask['id']).execute()
			self.get_tasks(self.quick_panel_tasklists_selected_index)


class GoogleAddTasklistFromInputCommand(sublime_plugin.WindowCommand):
	
	# global gservice
	global gtasklist
	
	def run(self):
		self.tasklist = {'title': ''}
		self.window.show_input_panel('Add a New TaskList Title:', '', self.on_done, None, None)
		pass

	def on_done(self, input):
		if input!='':
			self.tasklist['title'] = input
			gtasklist = gservice.tasklists().insert(body=self.tasklist).execute()
			self.window.run_command('google_view_tasks', {'resetTaskLists':True})
		pass

class GoogleEditTasklistFromInputCommand(sublime_plugin.WindowCommand):

	# global gservice
	global gtasklist
	
	def run(self):
		self.window.show_input_panel('Edit TaskList Title:', gtasklist['title'], self.on_done, None, None)

	def on_done(self, input):
		if input!='':
			gtasklist['title'] = input
			gservice.tasklists().patch(tasklist=gtasklist['id'], body=gtasklist).execute()
			self.window.run_command('google_view_tasks', {'resetTaskLists':True, 'resetTasks':True})
		pass

		
class GoogleAddTaskFromInputCommand(sublime_plugin.WindowCommand):

	# global gservice
	global gtasklist
	
	# def run(self, tasklistitem=None):
	def run(self):
		self.task = {'title' : ''}
		self.window.show_input_panel('Add a Task:', '', self.on_done, None, None)
		pass

	def on_done(self, input):
		print gtasklist
		if input!='':
			self.task['title'] = input
			gservice.tasks().insert(tasklist=gtasklist['id'], body=self.task).execute()
			self.window.run_command('google_view_tasks', {'resetTasks':True})
		pass

class GoogleEditTaskFromInputCommand(sublime_plugin.WindowCommand):
	
	# global gservice
	global gtask

	def run(self):
		self.window.show_input_panel('Edit Task:', gtask['title'], self.on_done, None, None)
		pass

	def on_done(self, input):
		if input!='':
			gtask['title'] = input
			gservice.tasks().patch(tasklist=gtasklist['id'], task=gtask['id'], body=gtask).execute()
			self.window.run_command('google_view_tasks', {'resetTasks':True})
		pass
