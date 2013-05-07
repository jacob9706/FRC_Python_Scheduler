"""
Author: Jacob Ebey
Version: Pre-Alpha 0.1
"""

class Scheduler(object):
	# Modes for autonomous tasks
	PARALLEL_TASK = "PARALLEL_TASK"
	SEQUENTIAL_TASK = "SEQUENTIAL_TASK"

	def __init__(self, robot_name):
		"""
		Initialize a Scheduler for maneging robot tasks.

		Keyword arguments:
		@robot_name -- The name of the robot.
		"""
		self.robot_name = robot_name

		self.teleop_tasks = []
		self.auto_tasks = []


	def register_teleop_task(self, task_name, task):
		"""
		Register a callable task to be called in the
		teleop_loop function. task must return True or
		False. Once the function returns True the function
		will be removed from the dictionary of tasks to
		be called in the teleop_loop.

		Keyword arguments:
		@task_name -- The name of the task.
		@task -- A callable function that must return True or False.
		"""
		# If it's not callable throw a Runtime Error
		if not hasattr(task, '__call__'):
			raise RuntimeError(str(task_name) + " is not callable.")

		# Store the task as a list with it's name.
		self.teleop_tasks.append([task_name, task])


	def register_teleop_task_if_not_already(self, task_name, task):
		"""
		Register a callable task to be called in the
		teleop_loop function. task must return True or
		False. Once the function returns True the function
		will be removed from the dictionary of tasks to
		be called in the teleop_loop.

		Unlike register_teleop_task this method will check to see in a
		task of the name of the callable task is already registered. Not
		the task_name you give it but task.__name__. This means that if
		you register a Claw.teleop for one and try to register a Arm.teleop
		with this method the Arm.teleop will not be registered.

		Keyword arguments:
		@task_name -- The name of the task.
		@task -- A callable function that must return True or False.
		"""
		# If it's not callable throw a Runtime Error
		if not hasattr(task, '__call__'):
			raise RuntimeError(str(task_name) + " is not callable.")

		for i, info in enumerate(self.teleop_tasks):
			if info[1].__name__ == task.__name__:
				if debug:
					print(task.__name__, "is already registered.")
				return

		# Store the task as a list with it's name.
		self.teleop_tasks.append([task_name, task])


	def remove_teleop_task(self, task_name, debug=False):
		"""
		Remove a task based on a name. If the task is found and
		removed it will return True, else it will return False.

		Keyword arguments:
		@task_name -- The name of the task to remove.
		"""
		for i, info in enumerate(self.teleop_tasks):
			if info[0] == task_name:
				del self.teleop_tasks[i]
				if debug:
					print(task_name, "has been removed.")
				return True
		return False


	def teleop(self, debug=False):
		"""
		Call all the registered teleop tasks once.
		This is meant to be called inside of a loop.
		Will return True when all tasks have resolved otherwise False.
		"""

		# If we have no more tasks return True
		if len(self.teleop_tasks) == 0:
			return True

		to_delete = []

		# Loop through all the tasks
		for i, info in enumerate(self.teleop_tasks):
			name, task = info

			if debug:
				print(name, "is running.")

			# If the task has resolved
			if task():
				# Add it to the delete list
				to_delete.append(i)
				if debug:
					print(name, "has resolved.")

		# Remove the resolved tasks
		for i in sorted(to_delete, reverse=True):
			del self.teleop_tasks[i]

		return False


	def register_auto_task(self, task_name, task, ttype=SEQUENTIAL_TASK):
		"""
		Register an autonomous task to be executed in order they were added.
		Autonomous tasks can be either a SEQUENTIAL_TASK or a PARALLEL_TASK.

		A SEQUENTIAL_TASK will not be executed until all other sequential tasks
		added before have resolved (returned True). This allows for tasks to be
		schedualed in a "step by step" manner.

		A PARALLEL_TASK will run when it is reached and continue to run until it
		is resolved.

		Example:
		S = SEQUENTIAL_TASK
		P = PARALLEL_TASK

		S s1
		P p1
		S s2

		In this example s1 will be the only thing running until it has resolved. After
		it has resolved p1 and s2 will be run. if s2 resolves p1 will continue to run 
		until it has been resolved.

		Keyword arguments:
		@task_name -- The name of the task.
		@task -- A callable function that must return True or False.
		@ttype -- The type of task (default SEQUENTIAL_TASK)
		"""
		# If it's not callable throw a Runtime Error
		if not hasattr(task, '__call__'):
			raise RuntimeError(str(task_name) + " is not callable.")
		if ttype not in [self.SEQUENTIAL_TASK, self.PARALLEL_TASK]:
			raise RuntimeError("ttype \"" + str(ttype) + "\" is not allowed.")

		# Store the task as a list with it's name and ttype.
		self.auto_tasks.append([task_name, ttype, task])


	def register_auto_task_if_not_already(self, task_name, task):
		"""
		Register an autonomous task to be executed in order they were added.
		Autonomous tasks can be either a SEQUENTIAL_TASK or a PARALLEL_TASK.

		Unlike register_auto_task this method will check to see in a
		task of the name of the callable task is already registered. Not
		the task_name you give it but task.__name__. This means that if
		you register a Claw.teleop for one and try to register a Arm.teleop
		with this method the Arm.teleop will not be registered.

		A SEQUENTIAL_TASK will not be executed until all other sequential tasks
		added before have resolved (returned True). This allows for tasks to be
		schedualed in a "step by step" manner.

		A PARALLEL_TASK will run when it is reached and continue to run until it
		is resolved.

		Example:
		S = SEQUENTIAL_TASK
		P = PARALLEL_TASK

		S s1
		P p1
		S s2

		In this example s1 will be the only thing running until it has resolved. After
		it has resolved p1 and s2 will be run. if s2 resolves p1 will continue to run 
		until it has been resolved.

		Keyword arguments:
		@task_name -- The name of the task.
		@task -- A callable function that must return True or False.
		@ttype -- The type of task (default SEQUENTIAL_TASK)
		"""
		# If it's not callable throw a Runtime Error
		if not hasattr(task, '__call__'):
			raise RuntimeError(str(task_name) + " is not callable.")
		if ttype not in [self.SEQUENTIAL_TASK, self.PARALLEL_TASK]:
			raise RuntimeError("ttype \"" + str(ttype) + "\" is not allowed.")

		for i, info in enumerate(self.auto_tasks):
			if info[1].__name__ == task.__name__:
				if debug:
					print(task.__name__, "is already registered.")
				return

		# Store the task as a list with it's name and ttype.
		self.auto_tasks.append([task_name, ttype, task])


	def remove_auto_task(self, task_name, debug=False):
		"""
		Remove a task based on a name. If the task is found and
		removed it will return True, else it will return False.

		Keyword arguments:
		@task_name -- The name of the task to remove.
		"""
		for i, info in enumerate(self.auto_tasks):
			if info[0] == task_name:
				del self.auto_tasks[i]
				if debug:
					print(task_name, "has been removed.")
				return True
		return False


	def auto(self, debug=False):
		"""
		Call the registered autonomous tasks when their time has come.
		Will return True when all tasks have resolved otherwise False.

		See register_auto_task for an explanation of the diffrent kind of tasks.
		"""
		# If we have no more tasks return True
		if len(self.auto_tasks) == 0:
			return True

		# A list of tasks to remove when done
		to_delete = []

		# Loop through the registered tasks
		for i, info in enumerate(self.auto_tasks):
			name, ttype, task = info

			if debug:
				print(name, "is running.")

			# If the task has resolved
			if task():
				# Add it to the delete list
				to_delete.append(i)
				if debug:
					print(name, "has resolved.")
				# If it is a sequential task we can not move on so break	
				if ttype == self.SEQUENTIAL_TASK:
					break
		# Remove the resolved tasks
		for i in sorted(to_delete, reverse=True):
			del self.auto_tasks[i]

		return False


if __name__ == '__main__':
	def test():
		"""
		Function for testing teleop callbacks.
		"""
		print "Hello"
		return False

	def test2():
		"""
		Function for testing teleop callbacks.
		"""
		print "Hello2"

		return True

	# Create a robot core
	rc = Scheduler("3574 Robot")

	# Register tasks
	rc.register_teleop_task("test", test)
	rc.register_teleop_task("test2", test2)

	# "Teleop loop"
	for i in range(100):
		rc.teleop(debug=True)
		rc.remove_teleop_task("test", debug=True)

	print("========================== Autonomous ==========================")

	class Auto(object):
		def __init__(self):
			self.task = 0

		def sequential1(self):
			if self.task < 5:
				return False
			return True

		def parallel1(self):
			self.task += 1
			if self.task > 5:
				return True
			return False

	auto = Auto()
	rc.register_auto_task("sequential1", auto.sequential1, ttype=Scheduler.SEQUENTIAL_TASK)
	rc.register_auto_task("parallel1", auto.parallel1, ttype=Scheduler.PARALLEL_TASK)

	# rc.register_auto_task("task1", test2, ttype=Scheduler.SEQUENTIAL_TASK)
	# rc.register_auto_task("task2", test, ttype=Scheduler.PARALLEL_TASK)
	# rc.register_auto_task("task3", test2, ttype=Scheduler.SEQUENTIAL_TASK)

	for i in range(10):
		rc.auto(debug=True)