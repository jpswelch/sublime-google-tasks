import sublime, sublime_plugin
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

gservice=None

class GoogleViewTasksCommand(sublime_plugin.WindowCommand):

	tasklists=None
	tasks=None
	selectedtasklistidx=None

	def get_auth(self):

		global gservice
		print 'GTasks: authenticating'
		# FLAGS = gflags.FLAGS
		FLOW = OAuth2WebServerFlow(
			client_id='630916051171.apps.googleusercontent.com',
			client_secret='Os8EcU7k7DZlFFHfXCxXIKaJ',
			scope='https://www.googleapis.com/auth/tasks',
			user_agent='Sublime Google Tasks/0.0.1')
		
		# FLAGS.auth_local_webserver = False

		storage = Storage('gtasks.dat')
		credentials = storage.get()
		if credentials is None or credentials.invalid == True:
			credentials = run(FLOW, storage)

		http = httplib2.Http()
		http = credentials.authorize(http)
		gservice = build(serviceName='tasks', version='v1', http=http)		
		return	


	def run(self):

		global gservice

		#auth once
		if gservice==None:
			self.get_auth()

		#show latest tasklist 	
		if self.selectedtasklistidx:		
			self.get_tasks(self.selectedtasklistidx)
			return

		self.tasklists = gservice.tasklists().list(fields='items(id,title)').execute()

		self.tli = []
		self.tli.append(['Add a New Task List'])

		try:
			for tasklist in self.tasklists['items']:
				self.tli.append(['  '+tasklist['title']])
		except:
			pass

		self.window.show_quick_panel(self.tli, self.get_tasks, sublime.MONOSPACE_FONT)

		
	def get_tasks(self, idx):

		global gservice

		if idx==-1:
			return

		if idx==0:
			window = sublime.active_window()
			window.run_command('google_add_task_list_from_input')
			return

		self.selectedtasklistidx = idx	

		self.tasklistitemindex = idx	
		self.tasklistitem = self.tasklists['items'][idx-1]['id']

		self.ti=[]
		self.ti.append(self.tli[idx][0])
		self.ti.append([u'\u21b5'+' View Task List'])
		self.ti.append([u'\u2715'+' Delete Task List'])
		self.ti.append([u'\u25FB'+' Clear Task List'])
		self.ti.append([u'\u271A'+' Add a Task'])
		
		self.tasks = gservice.tasks().list(tasklist=self.tasklistitem, fields='items(completed,id,status,title)').execute()
		try:
		 	for task in self.tasks['items']:
		 		if task['status']=='completed':
		 			self.ti.append(['  '+u'\u2714'+' '+task['title']])
		 		else:	
		 			self.ti.append(['    '+task['title']])
		except:
			pass

		self.window.show_quick_panel(self.ti, self.get_mod_task_options, sublime.MONOSPACE_FONT)


	def get_mod_task_options(self, idx):

		if (idx==-1 or idx==0):
			return

		if idx==1:
			self.window.show_quick_panel(self.tli, self.get_tasks)
			return

		if idx==2:
			confirmlist = []
			confirmlist.append(['Yes','Yes - Delete TaskList'])
			confirmlist.append(['No','No - Oops, don\'t Delete TaskList'])
			self.window.show_quick_panel(confirmlist, self.del_tasklist_confirm)
			return

		if idx==3:
			gservice.tasks().clear(tasklist=self.tasklistitem).execute()
			self.window.show_quick_panel(self.tli, self.get_tasks)
			return

		if idx==4:
			window = sublime.active_window()
			window.run_command('google_add_task_from_input', {"tasklistitem": self.tasklistitem})
			return	

		self.taskitem = self.tasks['items'][idx-5]['id']
		self.task = gservice.tasks().get(tasklist=self.tasklistitem, task=self.taskitem).execute()
		self.tasktitle = self.task['title']

		if self.task['status']=='completed':
			self.mod_options = [self.tasktitle,u'\u21b5'+' Back to Tasks', u'\u25FB'+' Clear', u'\u270E'+' Edit', u'\u2715'+' Delete']
		else:
			self.mod_options = [self.tasktitle,u'\u21b5'+' Back to Tasks', u'\u2714'+' Completed', u'\u270E'+' Edit', u'\u2715'+' Delete']

		self.window.show_quick_panel(self.mod_options, self.mod_task, sublime.MONOSPACE_FONT)


	def del_tasklist_confirm(self,idx):
		if idx==-1:
			return
		if idx==0:
			gservice.tasklists().delete(tasklist=self.tasklistitem).execute()
			self.selectedtasklistidx=None
			window = sublime.active_window()
			window.run_command('google_view_tasks')
			return
		if idx==1:
			self.window.show_quick_panel(self.tli, self.get_tasks, sublime.MONOSPACE_FONT)			
			return


	def mod_task(self, idx):
		if idx==-1:
			return

		# Go Back		
		if idx==1:
			self.window.show_quick_panel(self.ti, self.get_mod_task_options, sublime.MONOSPACE_FONT)

		# Complete/Clear Task	
		if idx==2:
			if self.task['status'] == 'completed':
				self.task['status'] = 'needsAction'
				self.task['completed'] = None
			else:
				self.task['status'] = 'completed'

			gservice.tasks().update(tasklist=self.tasklistitem, task=self.task['id'], body=self.task).execute()
			self.get_tasks(self.tasklistitemindex)

		# Edit Task
		if idx==3:
			window = sublime.active_window()
			window.run_command('google_edit_task_from_input', {"tasklistitem": self.tasklistitem, "task": self.task})
		
		# Delete Task
		if idx==4:
			gservice.tasks().delete(tasklist=self.tasklistitem, task=self.taskitem).execute()
			self.get_tasks(self.tasklistitemindex)



class GoogleAddTaskListFromInputCommand(sublime_plugin.WindowCommand):
	
	global gservice

	def run(self):
		self.tasklist = {'title': ''}
		self.window.show_input_panel('Add a New Task List Title:', self.tasklist['title'], self.on_done, self.on_change, self.on_cancel)

	def on_done(self, input):
		if input!='':
			self.tasklist['title'] = input
			result = gservice.tasklists().insert(body=self.tasklist).execute()
		window = sublime.active_window()
		window.run_command('google_view_tasks')
	

	def on_change(self, input):
		pass

	def on_cancel(self):
		pass	

		
class GoogleEditTaskFromInputCommand(sublime_plugin.WindowCommand):
	
	global gservice

	def run(self, tasklistitem=None, task=None):
		self.task = task
		self.tasklistitem = tasklistitem
		self.window.show_input_panel('Edit Task:', self.task['title'], self.on_done, self.on_change, self.on_cancel)

	def on_done(self, input):
		if input!='':
			self.task['title'] = input
			gservice.tasks().update(tasklist=self.tasklistitem, task=self.task['id'], body=self.task).execute()
			window = sublime.active_window()
			window.run_command('google_view_tasks')

	def on_change(self, input):
		pass

	def on_cancel(self):
		pass	


class GoogleAddTaskFromInputCommand(sublime_plugin.WindowCommand):

	global gservice
	
	def run(self, tasklistitem=None):
		self.task = {'title' : ''}
		self.tasklistitem = tasklistitem
		self.window.show_input_panel('Add a Task:', '', self.on_done, self.on_change, self.on_cancel)

	def on_done(self, input):
		if input!='':
			self.task['title'] = input
			gservice.tasks().insert(tasklist=self.tasklistitem, body=self.task).execute()
			window = sublime.active_window()
			window.run_command('google_view_tasks')

	def on_change(self, input):
		pass

	def on_cancel(self):
		pass	


# class GoogleEditTaskListFromInputCommand(sublime_plugin.WindowCommand):
	
	# global gservice

	# def run(self):
	# 	self.tasklist = {'title': ''}
	# 	self.window.show_input_panel('Edit Task List Title:', self.tasklist['title'], self.on_done, self.on_change, self.on_cancel)

	# def on_done(self, input):
	# 	if input!='':
	# 		self.tasklist['title'] = input
	# 		result = service.tasklists().update(tasklist=self.tasklist['id'], body=tasklist).execute()
	# 	window = sublime.active_window()
	# 	window.run_command('google_view_tasks')
	

	# def on_change(self, input):
	# 	pass

	# def on_cancel(self):
	# 	pass	
