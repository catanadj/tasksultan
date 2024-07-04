from taskw import TaskWarrior
import json
import datetime
import inquirer
from colorama import init, Fore, Back, Style
from datetime import datetime, timedelta,timezone
from collections import defaultdict
from collections import Counter
from termcolor import colored
from itertools import zip_longest
import textwrap
from dateutil.parser import parse
import pytz
import questionary
from questionary import Style
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from dateutil.tz import tzlocal
import subprocess
import argparse
import os
import calendar
from datetime import date
import texttable as tt
import pandas as pd
from fuzzywuzzy import process



def main():
	# Map each command to its corresponding function
	command_to_function = {
		's': search_task,
		'c': clear_data,
		'b': basic_summary,
		'd': detailed_summary,
		'a' : all_summary,
		'i': display_inbox_tasks,
		'tl': display_due_tasks,
		'ht': handle_task,
		'tc': task_control_center,
		'td': print_tasks_for_selected_day,
		'sp': call_and_process_task_projects,
		'o' : display_overdue_tasks,
		'rr': recurrent_report,
		'z': eisenhower,
	}
	
	parser = argparse.ArgumentParser(description='Process some commands.')
	parser.add_argument('command', metavar='CMD', type=str, nargs='?', default='',
						help='A command to run')

	args = parser.parse_args()

	if args.command:
		# Call the corresponding function if a command argument is provided
		command_to_function[args.command]()
	else:
		# Continue to the interactive prompt if no command argument is provided
		import os
		script_directory = os.path.dirname(os.path.abspath(__file__))
		file_path = os.path.join(script_directory, "sultandb.json")
		interactive_prompt(file_path)



try:
	

	def print_calendar_with_marked_day(year, month, day):
			cal = calendar.TextCalendar(firstweekday=calendar.MONDAY)
			today = date.today()  # Today's date
	
			month_name = calendar.month_name[month]
			year_text = str(year)
			
			
			print(f"{delimiter}\033[1;31m{month_name} {year_text}\033[0m{delimiter}")
	
			line = ""
			for week in cal.monthdayscalendar(year, month):
				for weekday in week:
					current_day = date(year, month, weekday) if weekday != 0 else None
	
					if weekday == day:
						line += f"{Back.GREEN}{Fore.BLACK}{weekday:02d}{Fore.RESET}{Back.RESET} "
					elif weekday == 0:
						line += "   "
					else:
						if current_day < today:  # Dates before today
							line += f"{Fore.BLACK}{Back.YELLOW}{weekday:02d}{Fore.RESET}{Back.RESET} "
						elif current_day > today:  # Dates after today
							line += f"{Fore.CYAN}{weekday:02d}{Fore.RESET} "
						else:  # Today
							line += f"{weekday:02d} "
			print(line)
	


			
			
			
			
	def display_overdue_tasks():
		warrior = TaskWarrior()
		tasks = warrior.load_tasks()
		print(colored("Overdue Tasks", 'yellow', attrs=['bold']))
		include_recurrent = questionary.confirm(
			"Include recurrent tasks in the search?", default=False).ask()
		if include_recurrent:
			tasks = tasks['pending']
		else:
			tasks = [task for task in tasks['pending'] if 'recur' not in task]

		# Determine local timezone
		local_tz = datetime.now().astimezone().tzinfo

		# Filter tasks for overdue tasks only
		overdue_tasks = []
		now = datetime.now(local_tz)
		for task in tasks:
			due_date_str = task.get('due')
			if due_date_str:
				due_date = datetime.strptime(
					due_date_str, "%Y%m%dT%H%M%SZ").replace(tzinfo=pytz.UTC)
				due_date = due_date.astimezone(local_tz)  # Convert to local time
				if due_date < now:
					time_remaining = now - due_date
					task['time_remaining'] = str(time_remaining.days) + " days"  # Calculate time remaining in days
					overdue_tasks.append(task)

		# Sort overdue tasks by due date (oldest to newest)
		overdue_tasks.sort(key=lambda task: task['due'])

		# Display overdue tasks
		if overdue_tasks:
			for task in overdue_tasks:
				task_id = colored(f"{task['id']}", 'yellow')
				description = colored(task['description'], 'cyan')
				tag = colored(','.join(task.get('tags', [])), 'red', attrs=['bold'])  # Join tags with comma
				project = colored(task.get('project', ''), 'blue', attrs=['bold'])
				time_remaining = colored(task.get('time_remaining', ''), 'green', attrs=['bold'])  # Display time remaining

				print(f"{task_id} {description} {tag} {project} -{time_remaining}")

				if 'annotations' in task:  # Ensure annotations are in the task
					for annotation in task['annotations']:
						entry_date = datetime.strptime(annotation['entry'], '%Y%m%dT%H%M%SZ').date()
						print(f"\t{Fore.CYAN}{entry_date}{Fore.YELLOW}: {annotation['description']}")
			print('=' * 60)
		else:
			print("No overdue tasks found.")




	def print_tasks_for_selected_day():
		# Initialize colorama
		init(autoreset=True)

		def get_deleted_tasks_due_today(date):
			# Run the 'task export' command and get the output
			result = subprocess.run(['task', 'export'], stdout=subprocess.PIPE)

			# Load the output into Python as JSON
			all_tasks = json.loads(result.stdout)

			# Prepare a list to store tasks
			deleted_tasks_due_today = []

			# Iterate over all tasks
			for task in all_tasks:
				# Check if task status is 'deleted' and if it's due date is today
				if task['status'] == 'deleted' and 'due' in task and datetime.strptime(task['due'], '%Y%m%dT%H%M%SZ').date() == date:
					deleted_tasks_due_today.append(task)

			# Return the list of tasks
			return deleted_tasks_due_today

		def parse_date(date_str):
			utc_time = datetime.strptime(date_str, '%Y%m%dT%H%M%SZ')
			return utc_time.replace(tzinfo=timezone.utc).astimezone(tz=None)

		user_choice = input("Do you want to display tasks for yesterday (y), today (t), or tomorrow (tm)? (y/t/tm): ").strip().lower()
		if user_choice not in ("yesterday", "yd","y", "today", "td","t", "tomorrow", "tm"):
			print("Default choice, today tasks displayed.")
			user_choice = "today"

		if user_choice in ("today", "td","t"):
			date = datetime.now().date()
			print(f"Selected tasks for {date}")
		elif user_choice in ("tomorrow", "tm"):
			date = datetime.now().date() + timedelta(days=1)
			print(f"Selected tasks for {date}")
		elif user_choice in ("yesterday", "yd","y"):
			date = datetime.now().date() - timedelta(days=1)
			print(f"Selected tasks for {date}")
		else:
			date = datetime.now().date()
			print(f"Selected tasks for {date}")
		
		w = TaskWarrior()
		pending_tasks = w.load_tasks()['pending']
		completed_tasks = w.load_tasks()['completed']
		deleted_tasks = get_deleted_tasks_due_today(date)

		due_tasks = sorted(
			(task for task in pending_tasks if task.get('due') and parse_date(task['due']).date() == date),
			key=lambda task: parse_date(task['due'])
		)

		completed_tasks = sorted(
			(task for task in completed_tasks if task.get('end') and parse_date(task['end']).date() == date),
			key=lambda task: parse_date(task['end'])
		)

		tasks_dict = {}
		for task_list in [due_tasks, completed_tasks, deleted_tasks]:
			for task in task_list:
				local_time = parse_date(task['due']) if task.get('due') else parse_date(task['end'])
				hour = local_time.hour
				minute = local_time.minute
				time_key = (hour, minute)
				task_status = task.get('status')
				task_id_or_deleted = '[DELETED]' if task in deleted_tasks else task.get('id')
				task_info = (
					task['description'], task.get('duration', 0), task_id_or_deleted, task.get('project'), task.get('tags'),
					task_status, task.get('annotations')
				)
				if time_key not in tasks_dict:
					tasks_dict[time_key] = [task_info]
				else:
					tasks_dict[time_key].append(task_info)

		current_time = datetime.now(timezone.utc).astimezone()

		for hour in range(24):
			hour_printed = False
			for minute in range(60):
				time_key = (hour, minute)
				if time_key in tasks_dict:
					if minute == 0 or not hour_printed:
						print(f"{Fore.YELLOW}{hour:02d}:00")
						hour_printed = True

					for task, duration, task_id, project, tags, status, annotations in tasks_dict[time_key]:
						project_color = Fore.GREEN if project and project.startswith('AoR.') else Fore.BLUE
						task_id_or_completed = f'{Fore.GREEN}[COMPLETED]{Fore.RESET}' if status == 'completed' else f"{Fore.RED} {task_id}"
						task_details = f"{Fore.YELLOW}{hour:02d}:{minute:02d} {task_id_or_completed}, {Fore.RESET}{task} [{duration} mins], {project_color}Pro:{project}, {Fore.RED}{tags}"
						print(task_details)
						if annotations:
							# print(f"{Fore.MAGENTA}Annotations:")
							for annotation in annotations:
								entry_date = parse_date(annotation['entry']).date()
								print(f"\t{Fore.CYAN}{entry_date}{Fore.YELLOW}: {annotation['description']}")

				if user_choice in ("today", "td") and hour == current_time.hour and minute == current_time.minute:
					print(f"{Fore.CYAN}{current_time.strftime('%H:%M')}{'=' * 25} {Fore.WHITE}Present Moment {Fore.RESET}{Fore.CYAN}{'=' * 25}{Fore.RESET}")

			if not hour_printed:
				print(f"{Fore.BLUE}{hour:02d}:00")

		if user_choice in ("today", "td") and current_time.hour == 23 and current_time.minute == 59:
			print(f"{'=' * 25} {Fore.WHITE}Present Moment {Fore.RESET}{'=' * 25}")

		if len(due_tasks) == 0:
			print(f"\n\t{Fore.BLACK}{Back.LIGHTCYAN_EX}  No pending tasks!{Fore.RESET}{Back.RESET}")
		else:
			print(f"\n\t\033[1m{len(due_tasks)} pending tasks out of {len(due_tasks)+len(completed_tasks)} total. {len(completed_tasks)} completed and {len(deleted_tasks)} deleted!")


		print_calendar_with_marked_day(date.year, date.month, date.day)
		while True:  
			
			action = questionary.select("What do you want to do next?", choices=["Refresh","Exit"]).ask()
			
			# CTRL+C actionx
			action = "Exit" if action is None else action

			if action == "Refresh":
				print_tasks_for_selected_day()  # Refresh and show data again
			elif action == "Exit":
				print("Exit")
				break




	def search_task():
		warrior = TaskWarrior()
		tasks = warrior.load_tasks()

		include_completed = questionary.confirm("Include completed tasks in the search?",default=False).ask()
		if include_completed:
			tasks = tasks['pending'] + tasks['completed']
		else:
			tasks = tasks['pending']

		task_descriptions = [task.get('description') for task in tasks]
		completer = FuzzyWordCompleter(task_descriptions)

		task_description = prompt("Enter a task description: ", completer=completer)

		selected_task = next((task for task in tasks if task.get('description') == task_description), None)

		if selected_task:
			print(f"{Fore.BLUE}ID:{Fore.RESET} {Fore.RED}{selected_task.get('id')}{Fore.RESET}")
			print(f"{Fore.BLUE}Description:{Fore.RESET} {Fore.YELLOW}{selected_task.get('description')}{Fore.RESET}")
			print(f"{Fore.BLUE}Project:{Fore.RESET} {Fore.YELLOW}{selected_task.get('project')}{Fore.RESET}")
			print(f"{Fore.BLUE}Tags:{Fore.RESET} {Fore.YELLOW}{', '.join(selected_task.get('tags', []))}{Fore.RESET}")
			due_date_str = selected_task.get('due')
			due_date = parse(due_date_str).replace(tzinfo=timezone.utc) if due_date_str else None
			if due_date:
				now = datetime.now(timezone.utc)
				time_remaining = due_date - now
				print(f"{Fore.BLUE}Due:{Fore.RESET} {Fore.YELLOW}{due_date}{Fore.RESET}\n{Fore.BLUE}Time Remaining:{Fore.RESET} {Fore.YELLOW}{time_remaining.days} days, {time_remaining.seconds // 3600}:{time_remaining.seconds % 3600 // 60}{Fore.RESET}")
		else:
			print("No task found with that description.")  



	def display_inbox_tasks():
		warrior = TaskWarrior()
		tasks = warrior.load_tasks()['pending']
		delimiter = ('-' * 40)
		# Filter tasks with the tag "in"
		inbox_tasks = [task for task in tasks if 'in' in task.get('tags', [])]

		# Parse entry dates and calculate time deltas
		for task in inbox_tasks:
			entry_date = datetime.strptime(task['entry'], '%Y%m%dT%H%M%SZ').replace(tzinfo=timezone.utc).astimezone(tz=None)
			task['time_delta'] = datetime.now(timezone.utc).astimezone(tz=None) - entry_date

		# Sort tasks by their time deltas
		inbox_tasks.sort(key=lambda task: task['time_delta'])

		# Print tasks
		print(f"{Fore.RED}{delimiter}{Fore.RESET}")
		for task in inbox_tasks:
			# Format time delta as days
			days = task['time_delta'].days
			formatted_days = f"-{days:02d}d"  # Adds leading zero if days < 10
			print(f"{Fore.CYAN}{task['id']}{Fore.RESET}, {Fore.GREEN}{formatted_days}{Fore.RESET}, {Fore.YELLOW}{task['description']}{Fore.RESET}")
		print(f"{Fore.BLUE}{delimiter}{Fore.RESET}")


	def handle_task():
		print("Please enter the task command:")
		print("Examples:")
		print("'223,114,187 done' - Marks tasks 223, 114, and 187 as done.")
		print("!!!! The operation will be done without asking for confirmation!.")
		print("To return to the main menu, press 'Enter'.\n")
		print("----------------------------------------------\n")

		while True:
			task_command = input()
			if task_command.lower() == '':
				return
			else:
				subprocess.run(f"yes | task {task_command}",shell=True)


	def display_due_tasks():
		warrior = TaskWarrior()
		tasks = warrior.load_tasks()

		include_recurrent = questionary.confirm(
			"Include recurrent tasks in the search?", default=False).ask()
		if include_recurrent:
			tasks = tasks['pending']
		else:
			tasks = [task for task in tasks['pending'] if 'recur' not in task]

		# Determine local timezone
		local_tz = datetime.now().astimezone().tzinfo

		# Define time frames
		now = datetime.now(local_tz)
		start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
		start_of_overdue = start_of_day - timedelta(days=365)
		end_of_today = start_of_day + timedelta(days=1)
		end_of_tomorrow = end_of_today + timedelta(days=1)
		# This should point to next Monday
		start_of_next_week = start_of_day + \
			timedelta(days=(7 - start_of_day.weekday()) % 7)
		end_of_next_week = start_of_next_week + \
			timedelta(days=6)  # This should point to next Sunday
		# This should point to day after tomorrow
		start_of_rest_of_the_week = end_of_tomorrow
		# This should point to the end of this week (Sunday)
		end_of_rest_of_the_week = start_of_next_week - timedelta(seconds=1)
		start_of_next_2_weeks = start_of_next_week
		end_of_next_2_weeks = start_of_next_2_weeks + \
			timedelta(days=15)  # Updated to include 2 weeks + 1 day
		start_of_next_3_weeks = start_of_next_week
		end_of_next_3_weeks = start_of_next_3_weeks + timedelta(days=21)
		end_of_next_3_months = start_of_day + timedelta(days=90)
		end_of_next_6_months = start_of_day + timedelta(days=180)
		end_of_next_year = start_of_day + timedelta(days=365)
		end_of_next_3_years = start_of_day + timedelta(days=365*3)
		end_of_next_5_years = start_of_day + timedelta(days=365*5)
		end_of_next_10_years = start_of_day + timedelta(days=365*10)
		end_of_next_20_years = start_of_day + timedelta(days=365*20)

		time_frames = [
			("Next 20 Years", end_of_next_10_years, end_of_next_20_years),
			("Next 10 Years", end_of_next_5_years, end_of_next_10_years),
			("Next 5 Years", end_of_next_3_years, end_of_next_5_years),
			("Next 3 Years", end_of_next_year, end_of_next_3_years),
			("Next Year", end_of_next_6_months, end_of_next_year),
			("Next 6 Months", end_of_next_3_months, end_of_next_6_months),
			("Next 3 Months", end_of_next_3_weeks, end_of_next_3_months),
			# Change the start time to end_of_next_week
			("Next 3 Weeks", end_of_next_week, end_of_next_3_weeks),
			# Change the start time to end_of_next_week
			("Next 2 Weeks", end_of_next_week, end_of_next_2_weeks),
			("Next Week", start_of_next_week, end_of_next_week),
			("Rest of the Week", start_of_rest_of_the_week,
			 end_of_rest_of_the_week),
			("Tomorrow", end_of_today, end_of_tomorrow),
			("Today", start_of_day, end_of_today),
			("Overdue", start_of_overdue, start_of_day),
		]

		# Categorize tasks
		categorized_tasks = {name: [] for name, _, _ in time_frames}
		for task in tasks:
			due_date_str = task.get('due')
			if due_date_str:
				due_date = datetime.strptime(
					due_date_str, "%Y%m%dT%H%M%SZ").replace(tzinfo=pytz.UTC)
				due_date = due_date.astimezone(local_tz)  # Convert to local time
				for name, start, end in time_frames:
					if start is None or (start <= due_date < end):
						if name== "Today":
							delta = ""
						else:
							delta = due_date - now
							days, seconds = delta.days, delta.seconds
							hours = seconds // 3600
							minutes = (seconds % 3600) // 60
							task['time_remaining'] = f"{days} days, {hours}:{minutes:02d}"  # Calculate time remaining
							categorized_tasks[name].append(task)
						break

		# Display tasks
		for name, tasks in list(categorized_tasks.items()):
			if tasks:
				print(colored(name, 'yellow', attrs=['bold']))
				for task in tasks:
					task_id = colored(f"[{task['id']}]", 'yellow')
					description = colored(task['description'], 'cyan')
					tag = colored(','.join(task.get('tags', [])), 'red', attrs=['bold'])  # Join tags with comma
					project = colored(task.get('project', ''), 'blue', attrs=['bold'])
					time_remaining = colored(task.get('time_remaining', ''), 'green', attrs=['bold'])  # Display time remaining
					
					print(f"{task_id} {description} {tag} {project} {time_remaining}")
					
					if 'annotations' in task:  # Ensure annotations are in the task
						for annotation in task['annotations']:
							entry_date = datetime.strptime(annotation['entry'], '%Y%m%dT%H%M%SZ').date()
							print(f"\t{Fore.CYAN}{entry_date}{Fore.YELLOW}: {annotation['description']}")
				print('=' * 60)

	def get_item_info(user_input):
		print(user_input + "this needs work")


	def mark_item_inactive(item_name, aors, projects):
		for item in aors:
			if item['name'] == item_name:
				item['status'] = 'Completed'

		for item in projects:
			if item['name'] == item_name:
				item['status'] = 'Completed'

	def get_creation_date(item_name):
		warrior = TaskWarrior()
		tasks = warrior.load_tasks()
		for task in tasks['pending']:
			project = task.get('project')
			if project and (project == item_name or project.startswith("AoR." + item_name)):
				created = task.get('entry')
				if created:
					print(datetime.strptime(created, "%Y%m%dT%H%M%SZ"))
					return datetime.strptime(created, "%Y%m%dT%H%M%SZ")

		return None

	def get_last_modified_date(item_name):
		warrior = TaskWarrior()
		tasks = warrior.load_tasks()
		last_modified = None
		for task in tasks['pending']:
			project = task.get('project')
			if project and (project == item_name or project.startswith("AoR." + item_name)):
				modified = task.get('modified')
				if modified:
					modified_date = datetime.strptime(
						modified, "%Y%m%dT%H%M%SZ")
					if last_modified is None or modified_date > last_modified:
						last_modified = modified_date

		return last_modified

	def get_tags_for_item(item_name):
		warrior = TaskWarrior()
		tasks = warrior.load_tasks()
		tags = {}
		for task in tasks['pending']:
			project = task.get('project')
			if project and (project == item_name or project.startswith("AoR." + item_name)):
				for tag in task.get('tags', []):
					if not tag.startswith("project:") and tag != item_name:
						tags[tag] = tags.get(tag, 0) + 1
		return tags

	def view_data(item, tags):
		print(f"{Fore.BLUE}Name: {Fore.YELLOW}{item['name']}{Fore.RESET}")
		print(
			f"{Fore.BLUE}Description: {Fore.YELLOW}{item.get('description', '')}{Fore.RESET}")

		# Get the number of pending tasks
		pending_tasks = 0
		for tag, count in tags.items():
			if tag != 'Completed':
				pending_tasks += count

		# Get the number of completed tasks
		completed_tasks = tags.get('Completed', 0)

		print(f"{Fore.BLUE}Pending: {Fore.YELLOW}{pending_tasks}{Fore.RESET} | "
			  f"{Fore.BLUE}Completed: {Fore.YELLOW}{completed_tasks}{Fore.RESET}")

		if 'standard' in item:
			field_name = "Standard" if 'outcome' not in item else "Outcome"
			field_value = item.get(
				'standard') if 'outcome' not in item else item.get('outcome')
			print(f"{Fore.BLUE}{field_name}: {Fore.YELLOW}{field_value}{Fore.RESET}")

		creation_date = get_creation_date(item['name'])
		if creation_date:
			current_datetime = datetime.now()
			creation_time_difference = current_datetime - creation_date
			creation_days_remaining = creation_time_difference.days
			creation_time_remaining = creation_time_difference.seconds
			creation_time_prefix = "-" if creation_days_remaining > 0 else "+"
			creation_time_remaining_formatted = str(
				timedelta(seconds=abs(creation_time_remaining)))
			creation_time_difference_formatted = f"({creation_time_prefix}{abs(creation_days_remaining)} days, {creation_time_remaining_formatted})"
			print(
				f"{Fore.BLUE}Creation Date: {Fore.YELLOW}{creation_date} {creation_time_difference_formatted}{Fore.RESET}")

		last_modified_date = get_last_modified_date(item['name'])
		if last_modified_date:
			current_datetime = datetime.now()
			last_modified_time_difference = current_datetime - last_modified_date
			last_modified_days_remaining = last_modified_time_difference.days
			last_modified_time_remaining = last_modified_time_difference.seconds
			last_modified_time_prefix = "-" if last_modified_days_remaining > 0 else "+"
			last_modified_time_remaining_formatted = str(
				timedelta(seconds=abs(last_modified_time_remaining)))
			last_modified_time_difference_formatted = f"({last_modified_time_prefix}{abs(last_modified_days_remaining)} days, {last_modified_time_remaining_formatted})"
			print(f"{Fore.BLUE}Last Modified Date: {Fore.YELLOW}{last_modified_date} {last_modified_time_difference_formatted}{Fore.RESET}")

		if 'outcome' in item:
			print(
				f"{Fore.BLUE}Outcome: {Fore.YELLOW}{item['outcome']}{Fore.RESET}")

		print(f"{Fore.BLUE}Tags:{Fore.RESET}")
		no_tag_tasks = []  # List to store tasks without tags
		for tag, count in tags.items():
			if tag != 'Completed':
				print(f" - {Fore.BLACK}{Back.YELLOW}{tag}{Fore.RESET}{Back.RESET} ({count} task{'s' if count > 1 else ''})")
				# Load tasks
				warrior = TaskWarrior()
				tasks = warrior.load_tasks()['pending']
				# Print tasks with the current tag and same project/AoR
				for task in tasks:
					task_tags = task.get('tags', [])
					task_project = task.get('project', '')
					if tag in task_tags and (task_project == item['name'] or task_project.startswith("AoR." + item['name'])):
						task_id = task['id']
						task_description = task.get('description', '')
						time_remaining = ""
						if 'due' in task:
							due_date = datetime.strptime(task['due'], '%Y%m%dT%H%M%SZ')
							time_remaining = due_date - datetime.now()
							time_remaining = str(time_remaining).split('.')[0]
						print(f"\t{Fore.YELLOW}{task_id}{Fore.RESET}, {Fore.CYAN}{task_description}{Fore.RESET} {time_remaining}")
					elif not task_tags and (task_project == item['name'] or task_project.startswith("AoR." + item['name'])):
						if task not in no_tag_tasks:  # Add tasks without tags to the list only if not already included
							no_tag_tasks.append(task)

		if no_tag_tasks:
			print(f" - \033[1;31m No Tag Tasks:\033[0m ({len(no_tag_tasks)} task{'s' if len(no_tag_tasks) > 1 else ''})")
			for task in no_tag_tasks:
				task_id = task['id']
				task_description = task.get('description', '')
				time_remaining = ""
				if 'due' in task:
					due_date = datetime.strptime(task['due'], '%Y%m%dT%H%M%SZ')
					time_remaining = due_date - datetime.now()
					time_remaining = str(time_remaining).split('.')[0]
				print(f"\t{Fore.RED}{task_id}{Fore.RESET}, {Fore.CYAN}{task_description}{Fore.RESET} {time_remaining}")
		else:
			print("No tags found.")
		
		if 'annotations' in item:
			print(f"\n{Fore.BLUE}Annotations:{Fore.RESET}")
			for annotation in item['annotations']:
				timestamp = annotation.get('timestamp')
				content = annotation.get('content', '')
				print(
					f" - {Fore.YELLOW}{timestamp}{Fore.RESET}: {Fore.YELLOW}{content}{Fore.RESET}")

		if 'workLogs' in item:
			print(f"{Fore.BLUE}Work Logs:{Fore.RESET}")
			for work_log in item['workLogs']:
				timestamp = work_log.get('timestamp')
				content = work_log.get('content', '')
				print(
					f" - {Fore.YELLOW}{timestamp}{Fore.RESET}: {Fore.YELLOW}{content}{Fore.RESET}")


	def execute_taskwarrior_command(command):
		"""Execute a TaskWarrior command and return its output."""
		try:
			proc = subprocess.run(command, shell=True, text=True, capture_output=True)
			if proc.stdout:
				return proc.stdout.strip()  # Remove extra whitespace
			if proc.stderr:
				print(f"Error: {proc.stderr}")
		except Exception as e:
			print(f"An error occurred while executing the TaskWarrior command: {e}")
		return ""

	def get_task_count(item_name, status):
		"""Get the count of tasks by status for a specific project."""
		command = f"task count project:{item_name} status:{status}"
		return int(execute_taskwarrior_command(command))

	def view_data_with_tree(item, tags,item_name):
		print(f"{Fore.BLUE}Name: {Fore.YELLOW}{item['name']}{Fore.RESET}")
		print(
			f"{Fore.BLUE}Description: {Fore.YELLOW}{item.get('description', '')}{Fore.RESET}")

		pending_tasks = get_task_count(item_name, 'pending')
		completed_tasks = get_task_count(item_name, 'completed')
		deleted_tasks = get_task_count(item_name, 'deleted')

		print(f"{Fore.YELLOW}Pending: {Fore.YELLOW}{pending_tasks}{Fore.RESET} | {Fore.YELLOW}Completed: {Fore.GREEN}{completed_tasks}{Fore.RESET} | {Fore.YELLOW}Deleted: {Fore.BLUE}{deleted_tasks}{Fore.RESET}")
			  
		print(delimiter)
		if 'standard' in item:
			field_name = "Standard" if 'outcome' not in item else "Outcome"
			field_value = item.get(
				'standard') if 'outcome' not in item else item.get('outcome')
			print(f"{Fore.BLUE}{field_name}: {Fore.YELLOW}{field_value}{Fore.RESET}")

		creation_date = get_creation_date(item['name'])
		if creation_date:
			current_datetime = datetime.now()
			creation_time_difference = current_datetime - creation_date
			creation_days_remaining = creation_time_difference.days
			creation_time_remaining = creation_time_difference.seconds
			creation_time_prefix = "-" if creation_days_remaining > 0 else "+"
			creation_time_remaining_formatted = str(
				timedelta(seconds=abs(creation_time_remaining)))
			creation_time_difference_formatted = f"({creation_time_prefix}{abs(creation_days_remaining)} days, {creation_time_remaining_formatted})"
			print(
				f"{Fore.BLUE}Creation Date: {Fore.YELLOW}{creation_date} {creation_time_difference_formatted}{Fore.RESET}")

		last_modified_date = get_last_modified_date(item['name'])
		if last_modified_date:
			current_datetime = datetime.now()
			last_modified_time_difference = current_datetime - last_modified_date
			last_modified_days_remaining = last_modified_time_difference.days
			last_modified_time_remaining = last_modified_time_difference.seconds
			last_modified_time_prefix = "-" if last_modified_days_remaining > 0 else "+"
			last_modified_time_remaining_formatted = str(
				timedelta(seconds=abs(last_modified_time_remaining)))
			last_modified_time_difference_formatted = f"({last_modified_time_prefix}{abs(last_modified_days_remaining)} days, {last_modified_time_remaining_formatted})"
			print(f"{Fore.BLUE}Last Modified Date: {Fore.YELLOW}{last_modified_date} {last_modified_time_difference_formatted}{Fore.RESET}")
		print(delimiter)
		if 'outcome' in item:
			print(
				f"{Fore.BLUE}Outcome: {Fore.YELLOW}{item['outcome']}{Fore.RESET}")

		print(delimiter)
		if 'annotations' in item:
			print(f"\n{Fore.BLUE}Annotations:{Fore.RESET}")
			for annotation in item['annotations']:
				timestamp = annotation.get('timestamp')
				content = annotation.get('content', '')
				print(
					f" - {Fore.YELLOW}{timestamp}{Fore.RESET}: {Fore.YELLOW}{content}{Fore.RESET}")
		print(delimiter)
		if 'workLogs' in item:
			print(f"{Fore.BLUE}Work Logs:{Fore.RESET}")
			for work_log in item['workLogs']:
				timestamp = work_log.get('timestamp')
				content = work_log.get('content', '')
				print(
					f" - {Fore.YELLOW}{timestamp}{Fore.RESET}: {Fore.YELLOW}{content}{Fore.RESET}")
		print(delimiter)
		project_summary(item_name)
		print(delimiter)

	def get_multiline_input(prompt):
		print(prompt)
		lines = []
		while True:
			line = input()
			if line:
				lines.append(line)
			else:
				break
		return '\n'.join(lines)

	def update_item(items, item_index, file_path, specific_field, aors, projects):
		commands = ['Add description', 'Add annotation',
					'Add work log entry', f'Add {specific_field}', 'Go back']
		while True:
			questions = [
				inquirer.List('command',
							message="Please select a command",
							choices=commands,
							),
			]
			answers = inquirer.prompt(questions)

			if answers['command'] == 'Add description':
				text = get_multiline_input("Enter Description: ")
				items[item_index]['description'] = text
				print(f"Added Description: {text}")
				save_sultandb(file_path, aors, projects)

			elif answers['command'] == 'Add annotation':
				text = get_multiline_input("Enter Annotation: ")
				timestamp = datetime.now()
				entry = {"content": text, "timestamp": timestamp}
				if 'annotations' not in items[item_index]:
					items[item_index]['annotations'] = []
				items[item_index]['annotations'].append(entry)
				print(f"Added Annotation: {text} at {timestamp}")
				save_sultandb(file_path, aors, projects)

			elif answers['command'] == 'Add work log entry':
				text = get_multiline_input("Enter Work Log Entry: ")
				timestamp = datetime.now()
				entry = {"content": text, "timestamp": timestamp}
				if 'workLogs' not in items[item_index]:
					items[item_index]['workLogs'] = []
				items[item_index]['workLogs'].append(entry)
				print(f"Added Work Log Entry: {text} at {timestamp}")
				save_sultandb(file_path, aors, projects)

			elif answers['command'] == f'Add {specific_field}':
				text = get_multiline_input(f"Enter {specific_field.capitalize()}: ")
				items[item_index][specific_field] = text
				print(f"Added {specific_field.capitalize()}: {text}")
				save_sultandb(file_path, aors, projects)

			elif answers['command'] == 'Go back':
				break


				


	def call_and_process_task_projects():
		# Call 'task projects' and capture its output
		result = subprocess.run(['task', 'projects'], capture_output=True, text=True)
		lines = result.stdout.splitlines()

		# Process the output from 'task projects'
		project_list = process_input(lines)  # project_list is now a list of all processed projects

		# Use the processed output as input to search_project()
		search_project(project_list)

	
	def process_input(lines):
		level_text = {0: ''}
		last_level = -1
		spaces_per_level = 2  # adjust this if needed

		# Ignore the first 4 and last 3 lines
		lines = lines[4:-3]

		output_lines = []  # Initialize the list to store all processed projects

		for line in lines:
			stripped = line.lstrip()
			level = len(line) - len(stripped)

			# Split the line into text and number, and only keep the text
			text = stripped.split()[0]

			if level % spaces_per_level != 0:
				raise ValueError('Invalid indentation level in input')

			level //= spaces_per_level

			if level > last_level + 1:
				raise ValueError('Indentation level increased by more than 1')

			level_text[level] = text

			# Clear all deeper levels
			level_text = {k: v for k, v in level_text.items() if k <= level}

			output_line = '.'.join(level_text[l] for l in range(level + 1))

			output_lines.append(output_line)  # Add each processed project to the list

			last_level = level
		
		return output_lines  # Return the list of all processed projects



	def project_summary(selected_item):
		from rich import print
		from rich.tree import Tree
		from rich.text import Text
		from rich.console import Console
		from datetime import datetime
		import pytz
		from dateutil.parser import parse

		console = Console()
		warrior = TaskWarrior()
		tasks = warrior.load_tasks()
		selected_project = selected_item

		task_dict = {}
		now = datetime.utcnow().replace(tzinfo=pytz.UTC)
		all_tasks = {task['uuid']: task for task in tasks['pending']}
		uuid_to_real_id = {task['uuid']: task['id'] for task in tasks['pending']}

		def is_relevant(task):
			project = task.get('project')
			return project and (project == selected_project or project.startswith(selected_project + '.'))

		def collect_tasks(task_uuid, visited=set()):
			if task_uuid in visited or task_uuid not in all_tasks:
				return
			visited.add(task_uuid)
			task = all_tasks[task_uuid]
			dependencies = task.get('depends', [])

			task_dict[task_uuid] = {
				'project': task.get('project'),
				'description': task.get('description', ''),
				'due_date': task.get('due'),
				'time_remaining': calculate_time_remaining(task.get('due'), now),
				'annotations': task.get('annotations', []),
				'tags': task.get('tags', []),
				'dependencies': dependencies
			}

			for dep_uuid in dependencies:
				collect_tasks(dep_uuid, visited)

		for task_uuid, task in all_tasks.items():
			if is_relevant(task):
				collect_tasks(task_uuid)

		tree = Tree(f"Dependency Tree: {selected_project}", style="green")
		local_tz = datetime.now().astimezone().tzinfo

		def add_task_to_tree(task_uuid, parent_branch):
			if task_uuid not in task_dict:
				return
			task = task_dict[task_uuid]
			real_id = uuid_to_real_id[task_uuid]
			task_description = task['description']
			task_id_text = Text(f"[{real_id}] ", style="red")
			task_description_text = Text(task_description, style="white")
			task_id_text.append(task_description_text)

			due_date = task.get('due_date')
			if due_date:
				formatted_due_date = parse(due_date).strftime('%Y-%m-%d')
				time_remaining, time_style = calculate_time_remaining(due_date, now)
				due_text = Text(f" {formatted_due_date} ", style="blue")
				time_remaining_text = Text(time_remaining, style=time_style)
				due_text.append(time_remaining_text)
				task_id_text.append(due_text)

			# Display tags in red bold
			if task.get('tags'):
				tags_text = Text(f" +{', '.join(task['tags'])} ", style="bold red")
				task_id_text.append(tags_text)

			# Display project in blue bold if different from the selected or if no project is assigned
			if task.get('project') != selected_project:
				project_text = Text(f" {task.get('project', 'No Project')} ", style="magenta")
				task_id_text.append(project_text)

			task_branch = parent_branch.add(task_id_text)

			annotations = task.get('annotations', [])
			if annotations:
				annotation_branch = task_branch.add(Text("Annotations:", style="white"))
				for annotation in annotations:
					entry_datetime = parse(annotation['entry'])
					if entry_datetime.tzinfo is None or entry_datetime.tzinfo.utcoffset(entry_datetime) is None:
						entry_datetime = entry_datetime.replace(tzinfo=local_tz)
					else:
						entry_datetime = entry_datetime.astimezone(local_tz)
					annotation_text = Text(f"{entry_datetime.strftime('%Y-%m-%d %H:%M:%S')} - {annotation['description']}", style="dim white")
					annotation_branch.add(annotation_text)

			for dep_uuid in task['dependencies']:
				add_task_to_tree(dep_uuid, task_branch)

		for task_uuid in task_dict:
			if not any(task_uuid in task_dict[dep_uuid]['dependencies'] for dep_uuid in task_dict):
				add_task_to_tree(task_uuid, tree)

		console.print(tree)


	def calculate_time_remaining(due_date_str, now):
		if due_date_str:
			due_date = parse(due_date_str)
			time_remaining = due_date - now
			if time_remaining.total_seconds() >= 0:
				time_style = "green"
			else:
				time_style = "red"

			# Formatted string to include days, hours, and minutes
			days = time_remaining.days
			seconds = time_remaining.seconds
			hours, remainder = divmod(seconds, 3600)
			minutes = remainder // 60

			if days or hours or minutes:
				formatted_time = f"{days}d {hours}h {minutes}m" if days else f"{hours}h {minutes}m"
			else:
				formatted_time = "0m"  # Show 0 minutes if time remaining is very short

			return formatted_time, time_style
		return None  # Return None when no due date







	def search_project(project_list):
		# Load from SultanDB

		
		script_directory = os.path.dirname(os.path.abspath(__file__))
		file_path = os.path.join(script_directory, "sultandb.json")
		aors, projects = load_sultandb(file_path)

		# Sync with TaskWarrior to update projects and AoRs
		active_aors, _, active_projects, _ = sync_with_taskwarrior(aors, projects, file_path)

		# Combine active and inactive projects and AoRs
		all_items = active_projects + active_aors

		# Create a list of all project and AoR names
		item_names = [item['name'] for item in all_items]

		# Create a fuzzy completer with all project and AoR names
		#print ("Debug:" + project_list)
		completer = FuzzyWordCompleter(project_list)

		# Prompt the user for a project or AoR name
		item_name = prompt("Enter a project or AoR name: ", completer=completer)
		#print(item_name)
		closest_match = process.extractOne(item_name, [item['name'] for item in all_items])
		#print(closest_match)
		if closest_match:
			# If a match was found, retrieve the item from all_items
			selected_item = next((item for item in all_items if item['name'] == closest_match[0]), None)

			# Run the project_summary with the selected project
			if selected_item:
				print(f"Dependency list for: {item_name}")
				tags=get_tags_for_item(selected_item['name'])
				view_data_with_tree(selected_item, tags,item_name)

				while True:  # Run until a non-refresh option is selected
					# Ask the user if they want to update the project or refresh
					print("\n\n\n" + "-:" * 40)
					action = questionary.select(
												"What do you want to do next?",
												choices=[
													"Refresh",
													"Display tree",
													"Add new task",
													"Set dependencies",
													"Remove dependencies",
													"Search another project",
													"Handle tasks",
													"Update metadata",
													"Main menu",
													"Exit"
												]
											).ask()
					print("-:" * 40)
					# CTRL+C actionx
					action = "Exit" if action is None else action

					if action == "Update metadata":
						if item_name.startswith("AoR."):
							specific_field = "standard"
						else:
							specific_field = "outcome"

						update_item(all_items, all_items.index(selected_item), file_path, specific_field, aors, projects)
						view_data_with_tree(selected_item, tags,item_name) #refresh after updating the data
						#break  # Break the loop after updating
					elif action == "Add new task":
						add_task_to_project(item_name)
						view_data_with_tree(selected_item, tags,item_name)  # Refresh and show data again
					elif action == "Set dependencies":
						dependency_input = questionary.text("Enter the tasks and their dependencies in the format 'ID>ID>ID, ID>ID':\n").ask()
						set_task_dependencies(dependency_input)
						view_data_with_tree(selected_item, tags,item_name)  # Refresh and show data again
					elif action == "Remove dependencies":
						task_ids_input = questionary.text("Enter the IDs of the tasks to remove dependencies (comma-separated):\n").ask()
						remove_task_dependencies(task_ids_input)
						view_data_with_tree(selected_item, tags,item_name)  # Refresh and show data again
					elif action == "Search another project":
						call_and_process_task_projects()
					elif action == "Handle tasks":
						handle_task()
						view_data_with_tree(selected_item, tags,item_name)  # Refresh and show data again
					elif action == "Refresh":
						view_data_with_tree(selected_item, tags,item_name)  # Refresh and show data again
					elif action == "Exit":
						print("Exit")
						break
					elif action == "Display tree":
						display_tasks(f"task pro:{item_name} +PENDING export")
					elif action == "Main menu":
						main_menu()
			else:
				print("No project or AoR found with that name.")
# x_x

	def add_task_to_project(project_name):
		task_description = questionary.text("Enter the description for the new task:").ask()
		
		# Create the task ensuring the entire input is treated as a single argument
		# by wrapping it in single quotes to handle special characters like + for tags
		create_command = f"task add proj:{project_name} {task_description}"
		execute_task_command(create_command)
		
		# Retrieve the ID of the newly created task
		task_id = get_latest_task_id()

		# Ask about dependencies
		has_dependencies = questionary.confirm("Does this task have dependencies?").ask()

		if has_dependencies:
			dependency_type = questionary.select(
				"Is this a blocking task (secondary) or does it have dependent tasks (primary)?",
				choices=["Secondary task", "Primary task"]
			).ask()

			if dependency_type == "Secondary task":
				blocking_task_id = questionary.text("Enter the ID of the task this is a sub-task of:").ask()
				modify_command = f"task {blocking_task_id} modify depends:{task_id}"
				execute_task_command(modify_command)
				print(f"Task {task_id} is now a sub-task of {blocking_task_id}.")
			elif dependency_type == "Primary task":
				dependent_task_ids = questionary.text("Enter the IDs of the tasks that depend on this (comma-separated):").ask()
				modify_dependent_tasks(task_id,dependent_task_ids)

	def get_latest_task_id():
		export_command = "task +LATEST export"
		try:
			proc = subprocess.run(export_command, shell=True, text=True, capture_output=True)
			if proc.stdout:
				tasks = json.loads(proc.stdout)
				if tasks:
					return str(tasks[0]['id'])
			if proc.stderr:
				print(proc.stderr)
		except Exception as e:
			print(f"An error occurred while exporting the latest task: {e}")
		return None

	def execute_task_command(command):
		try:
			proc = subprocess.run(command, shell=True, text=True, capture_output=True)
			if proc.stdout:
				print(proc.stdout)
			if proc.stderr:
				print(proc.stderr)
		except Exception as e:
			print(f"An error occurred while executing the task command: {e}")

	def modify_dependent_tasks(dependent_ids, task_id):
		ids = dependent_ids.split(',')
		for id in ids:
			modify_command = f"task {id.strip()} modify depends:{task_id}"
			execute_task_command(modify_command)
			print(f"Task {task_id} now depends on task {id.strip()}.")

	def set_task_dependencies(dependency_input):
		chains = dependency_input.split(',')
		for chain in chains:
			tasks = chain.split('>')
			# Reverse to set up each as blocking the previous
			tasks.reverse()
			for i in range(len(tasks) - 1):
				dependent_id = tasks[i].strip()
				task_id = tasks[i + 1].strip()
				modify_command = f"task {task_id} modify depends:{dependent_id}"
				execute_task_command(modify_command)
				print(f"Task {dependent_id} now depends on task {task_id}.")

	def remove_task_dependencies(task_ids_input):
		ids = task_ids_input.split(',')
		for id in ids:
			modify_command = f"task {id.strip()} modify depends:"
			execute_task_command(modify_command)
			print(f"Dependencies removed from task {id.strip()}.")

	def interactive_prompt(file_path):
		# Load from SultanDB
		aors, projects = load_sultandb(file_path)

		# Sync with TaskWarrior to update projects and AoRs
		active_aors, inactive_aors, active_projects, inactive_projects = sync_with_taskwarrior(
			aors, projects,file_path)

		commands = {
			'ua': ('Update AoRs', '⟳'),
			'up': ('Update Projects', '🗓️'),
			'e': ('Exit', '⇒'),
			's': ('Search', '🔍'),
			'c': ('Clear Data', '✖'),
			'b': ('Basic summary', '☰'),
			'd': ('Detailed summary', '☷'),
			'tc': ('Task centre', '⌖'),
			'ht': ('Handle Task', '🔧'),
			'o' : ('Overdue tasks list','Δ'),
			'td': ('Daily tasks', '✓'),
			'rr': ('Recurrent tasks report', '↻'),
			'z': ('Process or Value assignment', '⚙')
		}

		custom_style = Style([
			('qmark', 'fg:#673ab7 bold'),
			('question', 'bold'),
			('answer', 'fg:#f44336 bold'),
			('pointer', 'fg:#673ab7 bold'),
			('highlighted', 'fg:#673ab7 bold'),
			('selected', 'fg:#cc5454'),
			('separator', 'fg:#cc5454'),
			('instruction', ''),
			('text', ''),
			('disabled', 'fg:#858585 italic')
		])

		while True:
			print("\nPlease select a command:")
			for short, (full, emoji) in commands.items():
				print(f"{short:<2}: {emoji} {full:<18}")
			print("type command or press Enter to select a command from list.")

			command = input()
			if command:
				command = commands.get(command)[0] if commands.get(command) else None
				if not command:
					print("Invalid command.")
					continue
			else:
				command = questionary.select(
				"Please select a command",
				choices=[full for full, emoji in commands.values()],
				style=custom_style
			).ask()

		


			if command == 'Update AoRs':
				all_aors = active_aors + inactive_aors
				# Sort AoRs alphabetically
				all_aors.sort(key=lambda aor: aor['name'])

				# Group AoRs by prefix
				aor_groups = {}
				for aor in all_aors:
					prefix = aor['name'].split(".")[0]
					if prefix not in aor_groups:
						aor_groups[prefix] = []
					aor_groups[prefix].append(aor)

				# Prompt to select an AoR group
				aor_group_choices = list(aor_groups.keys()) + ['Back']
				questions = [
					inquirer.List('aor_group',
								  message="Please select an Area of Responsibility Group",
								  choices=aor_group_choices,
								  ),
				]
				aor_group_answers = inquirer.prompt(questions)
				if aor_group_answers['aor_group'] == 'Back':
					continue

				selected_aor_group = aor_groups[aor_group_answers['aor_group']]

				# Now prompt to select a specific AoR
				aor_choices = [aor['name']
							   for aor in selected_aor_group] + ['Back']
				questions = [
					inquirer.List('aor',
								  message="Please select an Area of Responsibility",
								  choices=aor_choices,
								  ),
				]
				aor_answers = inquirer.prompt(questions)
				if aor_answers['aor'] == 'Back':
					continue

				selected_aor = next(
					(aor for aor in selected_aor_group if aor['name'] == aor_answers['aor']), None)

				if selected_aor:
					# Find the index of the selected AoR
					item_index = all_aors.index(selected_aor)

					# Get tags for the selected AoR
					aor_tags = get_tags_for_item(selected_aor['name'])

					# Prompt to view data or update
					options = ['Update', 'View Data']
					questions = [
						inquirer.List('action',
									  message="Please select an action",
									  choices=options,
									  ),
					]
					action_answers = inquirer.prompt(questions)

					if action_answers['action'] == 'Update':
						# Existing code to update the selected AoR
						update_item(all_aors, item_index, file_path,
									'standard', aors, projects)
					elif action_answers['action'] == 'View Data':
						view_data(selected_aor, aor_tags)

			elif command == 'Update Projects':
				all_projects = active_projects + inactive_projects
				# Sort projects alphabetically
				all_projects.sort(key=lambda project: project['name'])

				# Group projects by prefix
				project_groups = {}
				for project in all_projects:
					prefix = project['name'].split(".")[0]
					if prefix not in project_groups:
						project_groups[prefix] = []
					project_groups[prefix].append(project)

				# Prompt to select a project group
				project_group_choices = list(project_groups.keys()) + ['Back']
				questions = [
					inquirer.List('project_group',
								  message="Please select a Project Group",
								  choices=project_group_choices,
								  ),
				]
				project_group_answers = inquirer.prompt(questions)
				if project_group_answers['project_group'] == 'Back':
					continue

				selected_project_group = project_groups[project_group_answers['project_group']]

				# Now prompt to select a specific project
				project_choices = [project['name']
								   for project in selected_project_group] + ['Back']
				questions = [
					inquirer.List('project',
								  message="Please select a Project",
								  choices=project_choices,
								  ),
				]
				project_answers = inquirer.prompt(questions)
				if project_answers['project'] == 'Back':
					continue

				selected_project = next(
					(project for project in selected_project_group if project['name'] == project_answers['project']), None)

				if selected_project:
					# Find the index of the selected project
					item_index = all_projects.index(selected_project)

					# Get tags for the selected project
					project_tags = get_tags_for_item(selected_project['name'])

					# Prompt to view data or update
					options = ['Update', 'View Data']
					questions = [
						inquirer.List('action',
									  message="Please select an action",
									  choices=options,
									  ),
					]
					action_answers = inquirer.prompt(questions)

					if action_answers['action'] == 'Update':
						# Existing code to update the selected project
						update_item(all_projects, item_index,
									file_path, 'outcome', aors, projects)
					elif action_answers['action'] == 'View Data':
						view_data(selected_project, project_tags)
			elif command == 'Search':
				search_commands = ['Search Data',
								   'Search Project', 'Search Task', 'Back']
				search_command = questionary.select(
					"Please select a search command",
					choices=search_commands,
					style=custom_style
				).ask()
				if search_command == 'Search Data':
					search_data(aors, projects)
				elif command == 'Search Project':
					call_and_process_task_projects()
				elif search_command == 'Search Task':
					search_task()
			elif command == 'View Data':
				all_items = active_aors + active_projects
				all_items.sort(key=lambda x: x['name'])

				item_choices = [item['name'] for item in all_items] + ['Back']
				questions = [
					inquirer.List('item',
								  message="Please select an item to view data",
								  choices=item_choices,
								  ),
				]
				answers = inquirer.prompt(questions)
				if answers['item'] == 'Back':
					continue

				selected_item = next(
					(item for item in all_items if item['name'] == answers['item']), None)
				if selected_item:
					if selected_item in active_aors:
						item_tags = get_tags_for_item(selected_item['name'])
					elif selected_item in active_projects:
						item_tags = get_tags_for_item(selected_item['name'])
					view_data(selected_item, item_tags)
				else:
					print("Invalid item selection.")

			elif command == 'Exit':
				break

			elif command == 'Clear Data':
				clear_data(aors, projects, file_path)
			elif command == 'Basic summary':
				basic_summary()

			elif command == 'Detailed summary':
				detailed_summary()
			elif command == 'Inbox':
				display_inbox_tasks()
			elif command == 'Task list':
				display_due_tasks()
			elif command == 'Handle Task':
				handle_task()
			elif command == 'Daily tasks':
				print_tasks_for_selected_day()
			elif command == 'Overdue tasks list':
				display_overdue_tasks()
			elif command == 'Recurrent tasks report':
				recurrent_report()
			elif command == 'Process or Value assignment':
				eisenhower()
			elif command == 'Task centre':
				task_control_center()



	def search_data(aors, projects):
		search_term = input("Enter the search term: ")
		found_entries = []

		for aor in aors:
			entry = {
				"name": f"AoR: {aor['name']}",
				"matches": []
			}

			if search_term in aor['description']:
				entry['matches'].append(("Description", aor['description']))

			if search_term in aor['standard']:
				entry['matches'].append(("Standard", aor['standard']))

			for annotation in aor.get('annotations', []):
				if search_term in annotation['content']:
					entry['matches'].append(
						("Annotation", annotation['content']))

			for work_log in aor.get('workLogs', []):
				if search_term in work_log['content']:
					entry['matches'].append(
						("Work Log Entry", work_log['content']))

			if entry['matches']:
				found_entries.append(entry)

		for project in projects:
			entry = {
				"name": f"Project: {project['name']}",
				"matches": []
			}

			if search_term in project['description']:
				entry['matches'].append(
					("Description", project['description']))

			if search_term in project['outcome']:
				entry['matches'].append(("Outcome", project['outcome']))

			for annotation in project.get('annotations', []):
				if search_term in annotation['content']:
					entry['matches'].append(
						("Annotation", annotation['content']))

			for work_log in project.get('workLogs', []):
				if search_term in work_log['content']:
					entry['matches'].append(
						("Work Log Entry", work_log['content']))

			if entry['matches']:
				found_entries.append(entry)

		if found_entries:
			print(f"Search Results for '{search_term}':")
			for entry in found_entries:
				print(f"{Fore.BLUE}{entry['name']}{Fore.RESET}")
				for match in entry['matches']:
					field_name, field_value = match
					field_value = field_value.replace(
						search_term, f"{Fore.YELLOW}{search_term}{Fore.RESET}")
					print(f" - {field_name}: {field_value}")
		else:
			print(f"No results found for '{search_term}'.")

	def clear_data(aors, projects, file_path):
		while True:
			commands = ['All AoR data', 'All Projects data',
						'Everything', 'Individual AoR or Project', 'Go back']
			questions = [
				inquirer.List('command',
							  message="Please select a command",
							  choices=commands,
							  ),
			]
			answers = inquirer.prompt(questions)

			if answers['command'] == 'All AoR data':
				confirmation = confirm_action(
					"Are you sure you want to clear all AoR data?")
				if confirmation:
					for aor in aors:
						aor['description'] = ""
						aor['standard'] = ""
						aor['annotations'] = []
						aor['workLogs'] = []
					print("Cleared all AoR data.")
					save_sultandb(file_path, aors, projects)
				else:
					print("Action canceled.")

			elif answers['command'] == 'All Projects data':
				confirmation = confirm_action(
					"Are you sure you want to clear all Projects data?")
				if confirmation:
					for project in projects:
						project['description'] = ""
						project['outcome'] = ""
						project['annotations'] = []
						project['workLogs'] = []
					print("Cleared all Projects data.")
					save_sultandb(file_path, aors, projects)
				else:
					print("Action canceled.")

			elif answers['command'] == 'Everything':
				confirmation = confirm_action(
					"Are you sure you want to clear everything?")
				if confirmation:
					for aor in aors:
						aor['description'] = ""
						aor['standard'] = ""
						aor['annotations'] = []
						aor['workLogs'] = []
					for project in projects:
						project['description'] = ""
						project['outcome'] = ""
						project['annotations'] = []
						project['workLogs'] = []
					print("Cleared all AoR and Project data.")
					save_sultandb(file_path, aors, projects)
				else:
					print("Action canceled.")

			elif answers['command'] == 'Individual AoR or Project':
				# Existing code for clearing individual AoR or Project
				commands = ['AoR', 'Project', 'Go back']
				questions = [
					inquirer.List('command',
								  message="Would you like to clear an AoR or a Project?",
								  choices=commands,
								  ),
				]
				answers = inquirer.prompt(questions)

				if answers['command'] == 'AoR':
					if len(aors) == 0:
						print("No AoRs available.")
					else:
						while True:
							questions = [
								inquirer.List('aor',
											  message="Please select an AoR",
											  choices=[aor['name']
													   for aor in aors] + ['Go back'],
											  ),
							]
							answers = inquirer.prompt(questions)

							if answers['aor'] == 'Go back':
								break

							item_index = next(index for (index, d) in enumerate(
								aors) if d["name"] == answers['aor'])
							aor = aors[item_index]
							aor['description'] = ""
							aor['standard'] = ""
							aor['annotations'] = []
							aor['workLogs'] = []
							print("Cleared selected AoR data.")
							save_sultandb(file_path, aors, projects)

				elif answers['command'] == 'Project':
					if len(projects) == 0:
						print("No Projects available.")
					else:
						while True:
							questions = [
								inquirer.List('project',
											  message="Please select a Project",
											  choices=[project['name']
													   for project in projects] + ['Go back'],
											  ),
							]
							answers = inquirer.prompt(questions)

							if answers['project'] == 'Go back':
								break

							item_index = next(index for (index, d) in enumerate(
								projects) if d["name"] == answers['project'])
							project = projects[item_index]
							project['description'] = ""
							project['outcome'] = ""
							project['annotations'] = []
							project['workLogs'] = []
							print("Cleared selected Project data.")
							save_sultandb(file_path, aors, projects)

			elif answers['command'] == 'Go back':
				break

	def confirm_action(message):
		questions = [
			inquirer.Confirm('confirmation',
							 message=message,
							 ),
		]
		answers = inquirer.prompt(questions)
		return answers['confirmation']

	def get_tags_for_aor(aor_name):
		warrior = TaskWarrior()
		tasks = warrior.load_tasks()['pending']
		aor_tasks = [task for task in tasks if 'tags' in task and task.get(
			'project') == f"AoR.{aor_name}"]

		tag_counts = {}
		for task in aor_tasks:
			for tag in task['tags']:
				if tag.startswith("AoR.") or tag.startswith("project:"):
					continue
				if tag not in tag_counts:
					tag_counts[tag] = 0
				tag_counts[tag] += 1

		return tag_counts

	def load_sultandb(file_path):
		try:
			with open(file_path, 'r', encoding='utf-8') as file:
				sultandb = json.load(file)
		except FileNotFoundError:
			sultandb = {"aors": [], "projects": []}
		return sultandb['aors'], sultandb['projects']

	def save_sultandb(file_path, aors, projects):
		sultandb = {"aors": aors, "projects": projects}
		with open(file_path, 'w', encoding='utf-8') as file:
			json.dump(sultandb, file, default=str, indent=4)

	def sync_with_taskwarrior(aors, projects,file_path):
		warrior = TaskWarrior()
		tasks = warrior.load_tasks()

		task_projects = set()

		for task in tasks['pending']:
			project = task.get('project')
			if project:
				task_projects.add(project)

		active_aors = []
		inactive_aors = []
		completed_aors = []
		active_projects = []
		inactive_projects = []
		completed_projects = []

		for aor in aors:
			if f"AoR.{aor['name']}" in task_projects:
				active_aors.append(aor)
			else:
				if aor['status'] != 'Completed':
					aor['status'] = 'Completed'
				completed_aors.append(aor)

		for project in projects:
			if project['name'] in task_projects:
				active_projects.append(project)
			else:
				if project['status'] != 'Completed':
					project['status'] = 'Completed'
				completed_projects.append(project)

		for task_project in task_projects:
			if task_project.startswith("AoR."):
				aor_name = task_project[4:]
				if aor_name not in [aor['name'] for aor in aors]:
					new_aor = {'name': aor_name, 'description': '', 'standard': '', 'annotations': [
					], 'workLogs': [], 'status': 'Active'}
					active_aors.append(new_aor)

			elif task_project not in [project['name'] for project in projects]:
				new_project = {'name': task_project, 'description': '', 'outcome': '', 'annotations': [
				], 'workLogs': [], 'status': 'Active'}
				active_projects.append(new_project)

		# Save sultandb.json
		save_sultandb(file_path, active_aors + completed_aors,
					  active_projects + completed_projects)

		return active_aors, inactive_aors, active_projects, inactive_projects + completed_projects

	colors = ['red', 'green', 'yellow', 'magenta', 'cyan'] #colors for tree branch levels for the functions underneath

	def basic_summary():
		from rich import print
		from rich.tree import Tree
		from rich.text import Text
		from rich.console import Console


		console = Console()
		warrior = TaskWarrior()
		tasks = warrior.load_tasks()

		project_data = defaultdict(lambda: defaultdict(list))
		now = datetime.utcnow().replace(tzinfo=pytz.UTC)

		for task in tasks['pending']:
			project = task.get('project', None)
			tags = task.get('tags', [])
			description = task.get('description', '')
			task_id = task.get('id', '')
			due_date_str = task.get('due')
			due_date = parse(due_date_str) if due_date_str and due_date_str != '' else None

			if project:
				if tags:
					for tag in tags:
						time_remaining = due_date - now if due_date else None
						time_remaining_str = str(time_remaining)[:-7] if time_remaining else ''
						project_data[project][tag].append([f"{task_id} {description}", due_date_str, time_remaining_str])
				else:
					project_data[project]["No Tag"].append([f"{task_id} {description}", due_date_str, time_remaining_str])
			else:
				# For tasks without a project, we will put them under "No Project" key
				if tags:
					for tag in tags:
						project_data["No Project"][tag].append([f"{task_id} {description}", due_date_str, time_remaining_str])
				else:
					# For tasks without a project and without tags, we put them under "No Tag" key
					project_data["No Project"]["No Tag"].append([f"{task_id} {description}", due_date_str, time_remaining_str])

		tree = Tree("Tasks Summary")

		for project, tag_data in sorted(project_data.items()):
			if project != "No Project":
				project_levels = project.split(".")
				project_branch = tree
				for i, level in enumerate(project_levels):
					color = colors[i % len(colors)]
					level = Text(level, style=f'{color} bold')
					if level not in [child.label for child in project_branch.children]:
						project_branch = project_branch.add(level)
					else:
						project_branch = next(child for child in project_branch.children if child.label == level)

				for tag, tasks_data in sorted(tag_data.items()):
					tag_color = 'green' if not project.startswith("AoR.") else 'cyan'
					tag_branch = project_branch.add(Text(f"{tag} [{len(tasks_data)}]", style=f'{tag_color} bold'))

		# Handle "No Project" separately to make sure it comes at the end
		if "No Project" in project_data:
			project_branch = tree.add(Text("No Project", style='red bold'))
			for tag, tasks_data in sorted(project_data["No Project"].items()):
				tag_color = 'blue'
				tag_branch = project_branch.add(Text(f"{tag} [{len(tasks_data)} tasks]", style=f'{tag_color} bold'))

		console.print(tree)


	
	
	def detailed_summary():
		#the modules are imported here because of an unidentified cause: the ascii codes are getting printed in the other functions instead of coloring the output when these modules are imported in the main.
		from rich import print
		from rich.tree import Tree
		from rich.text import Text
		from rich.console import Console
		console = Console()
		warrior = TaskWarrior()
		tasks = warrior.load_tasks()

		project_data = defaultdict(lambda: defaultdict(list))
		now = datetime.utcnow().replace(tzinfo=pytz.UTC)

		for task in tasks['pending']:
			project = task.get('project', None)
			tags = task.get('tags', [])
			description = task.get('description', '')
			task_id = task.get('id', '')
			due_date_str = task.get('due')
			due_date = parse(due_date_str) if due_date_str and due_date_str != '' else None

			if project:
				if tags:
					for tag in tags:
						if not project_data[project][tag] or (due_date and (not project_data[project][tag][1] or due_date < parse(project_data[project][tag][1]))):
							time_remaining = due_date - now if due_date else None
							time_remaining_str = str(time_remaining)[:-7] if time_remaining else ''
							project_data[project][tag] = [f"{task_id} {description}", due_date_str, time_remaining_str]
				else:
					time_remaining = due_date - now if due_date else None
					time_remaining_str = str(time_remaining)[:-7] if time_remaining else ''
					project_data[project]["No Tag"] = [f"{task_id} {description}", due_date_str, time_remaining_str]

			else:
				# For tasks without a project, we will put them under "No Project" key
				if tags:
					for tag in tags:
						project_data["No Project"][tag].append(f"{task_id} {description}")
				else:
					# For tasks without a project and without tags, we put them under "No Tag" key
					project_data["No Project"]["No Tag"].append(f"{task_id} {description}")

		tree = Tree(Text("Saikou", style='green bold'))

		for project, tag_data in sorted(project_data.items()):
			if project != "No Project":
				project_levels = project.split(".")
				project_branch = tree

				for level_idx, level in enumerate(project_levels):
					if level not in [child.label.plain for child in project_branch.children]:
						project_branch = project_branch.add(Text(level, style=f'{colors[level_idx % len(colors)]} bold'))
					else:
						project_branch = next(child for child in project_branch.children if child.label.plain == level)

				for tag, data in sorted(tag_data.items()):
					tag_color = 'blue' if not project.startswith("AoR.") else 'yellow'
					tag_branch = project_branch.add(Text(tag, style=f'{tag_color} bold'))

					task_data = data[0]
					if task_data:
						task_id, description = (task_data.split(" ", 1) + [""])[:2]
						due_date = data[1] if len(data) > 1 else None
						try:
							due_date_formatted = datetime.strptime(due_date, "%Y%m%dT%H%M%SZ").strftime("%Y-%m-%d") if due_date else ""
						except ValueError:
							due_date_formatted = ""

						time_remaining = data[2] if len(data) > 2 else None

						tag_branch.add(f"[red bold]{task_id}[/red bold] [white bold]{description}[/white bold] [blue bold]{due_date_formatted}[/blue bold] [green bold]{time_remaining}[/green bold]")

		# Handle "No Project" separately to make sure it comes at the end
		if "No Project" in project_data:
			project_branch = tree.add(Text("No Project", style='red bold'))
			for tag, data in sorted(project_data["No Project"].items()):
				tag_color = 'blue'
				tag_branch = project_branch.add(Text(tag, style=f'{tag_color} bold'))

				task_data = data[0]
				if task_data:
					task_id, description = (task_data.split(" ", 1) + [""])[:2]
					due_date = data[1] if len(data) > 1 else None
					try:
						due_date_formatted = datetime.strptime(due_date, "%Y%m%dT%H%M%SZ").strftime("%Y-%m-%d") if due_date else ""
					except ValueError:
						due_date_formatted = ""

					time_remaining = data[2] if len(data) > 2 else None

					tag_branch.add(f"[red bold]{task_id}[/red bold] [white]{description}[/white] [blue bold]{due_date_formatted}[/blue bold] [green bold]{time_remaining}[/green bold]")

		console.print(tree)





	def all_summary():
		from rich import print
		from rich.tree import Tree
		from rich.text import Text
		from rich.console import Console
		console = Console()
		warrior = TaskWarrior()
		tasks = warrior.load_tasks()

		project_data = defaultdict(lambda: defaultdict(list))
		no_project_data = defaultdict(list)
		no_project_no_tag_data = []
		now = datetime.utcnow().replace(tzinfo=pytz.UTC)

		for task in tasks['pending']:
			project = task.get('project', None)
			tags = task.get('tags', [])
			description = task.get('description', '')
			task_id = task.get('id', '')
			due_date_str = task.get('due')
			due_date = parse(due_date_str) if due_date_str and due_date_str != '' else None
			time_remaining = due_date - now if due_date else None
			time_remaining_str = str(time_remaining)[:-7] if time_remaining else ''
			priority = task.get('priority', '')

			if project:
				if tags:
					for tag in tags:
						project_data[project][tag].append([f"{task_id} {description}", due_date_str, time_remaining_str,priority])
				else:
					project_data[project]["No Tag"].append([f"{task_id} {description}", due_date_str, time_remaining_str,priority])
			elif tags:
				for tag in tags:
					no_project_data[tag].append([f"{task_id} {description}", due_date_str, time_remaining_str,priority])
			else:
				no_project_no_tag_data.append([f"{task_id} {description}", due_date_str, time_remaining_str,priority])

		tree = Tree("Saikou", style="green bold")

		sorted_projects = sorted([project for project in project_data.keys() if project != "No Project"]) + ["No Project" if "No Project" in project_data else ""]

		for project in sorted_projects:
			tag_data = project_data[project]
			project_levels = project.split(".")
			project_branch = tree

			for level_idx, level in enumerate(project_levels):
				if level not in [child.label.plain for child in project_branch.children]:
					project_branch = project_branch.add(Text(level, style=f'{colors[level_idx % len(colors)]} bold'))
				else:
					project_branch = next(child for child in project_branch.children if child.label.plain == level)

			for tag, tasks_data in sorted(tag_data.items()):
				tag_color = 'blue' if not project.startswith("AoR.") else 'yellow'
				tag_branch = project_branch.add(Text(tag, style=f'{tag_color} bold'))

				for data in tasks_data:
					task_data = data[0]
					task_id, description = (task_data.split(" ", 1) + [""])[:2]
					due_date = data[1] if len(data) > 1 else None
					priority = data[3] if len(data) > 3 else 'No Priority'
					try:
						due_date_formatted = datetime.strptime(due_date, "%Y%m%dT%H%M%SZ").strftime("%Y-%m-%d") if due_date else ""
					except ValueError:
						due_date_formatted = ""

					time_remaining = data[2] if len(data) > 2 else None

					color_pri = ""
					if priority == "H" :
						color_pri = "red"
					else:
						color_pri = "white"

					tag_branch.add(f"[yellow bold]{priority}[/yellow bold] [red bold]{task_id}[/red bold] [{color_pri}]{description}[/{color_pri}] [blue bold]{due_date_formatted}[/blue bold] [green bold]{time_remaining}[/green bold]")

		# Handle "No Project" tasks
		no_project_branch = tree.add("No Project", style="red bold")

		for tag, tasks_data in no_project_data.items():
			tag_branch = no_project_branch.add(Text(f"{tag} [{len(tasks_data)} tasks]", style='blue bold'))

			for data in tasks_data:
				task_data = data[0]
				task_id, description = (task_data.split(" ", 1) + [""])[:2]
				due_date = data[1] if len(data) > 1 else None
				priority = data[3] if len(data) > 3 else 'No Priority'
				try:
					due_date_formatted = datetime.strptime(due_date, "%Y%m%dT%H%M%SZ").strftime("%Y-%m-%d") if due_date else ""
				except ValueError:
					due_date_formatted = ""

				time_remaining = data[2] if len(data) > 2 else None

				tag_branch.add(f"[yellow bold]{priority}[/yellow bold] [red bold]{task_id}[/red bold] [white]{description}[/white] [blue bold]{due_date_formatted}[/blue bold] [green bold]{time_remaining}[/green bold] ")

		# Handle "No Project, No Tag" tasks
		no_project_no_tag_branch = tree.add("No Project, No Tag", style="red bold")

		for data in no_project_no_tag_data:
			task_data = data[0]
			task_id, description = (task_data.split(" ", 1) + [""])[:2]
			due_date = data[1] if len(data) > 1 else None
			priority = data[3] if len(data) > 3 else 'No Priority'
			try:
				due_date_formatted = datetime.strptime(due_date, "%Y%m%dT%H%M%SZ").strftime("%Y-%m-%d") if due_date else ""
			except ValueError:
				due_date_formatted = ""

			time_remaining = data[2] if len(data) > 2 else None

			no_project_no_tag_branch.add(f"[yellow bold]{priority}[/yellow bold] [red bold]{task_id}[/red bold] [white]{description}[/white] [blue bold]{due_date_formatted}[/blue bold] [green bold]{time_remaining}[/green bold]")

		console.print(tree)

	def recurrent_report():
		from rich.table import Table
		from rich.console import Console
		from statistics import mean
		def parse_date(date_str):
			utc_time = datetime.strptime(date_str, '%Y%m%dT%H%M%SZ')
			return utc_time.replace(tzinfo=timezone.utc).astimezone(tz=None)

		def color_code_percentage(percentage):
			if percentage > 0.75:
				return '[green]', '[/green]'
			elif 0.5 <= percentage <= 0.75:
				return '[yellow]', '[/yellow]'
			elif 0.25 <= percentage < 0.5:
				return '[magenta]', '[/magenta]'
			else:
				return '[red]', '[/red]'

		def get_all_deleted_tasks():
			# Run the 'task export' command and get the output
			result = subprocess.run(['task', 'export'], stdout=subprocess.PIPE)

			# Load the output into Python as JSON
			all_tasks = json.loads(result.stdout)

			# Prepare a list to store tasks
			deleted_tasks = []

			# Iterate over all tasks
			for task in all_tasks:
				# Check if task status is 'deleted' 
				if task['status'] == 'deleted' and 'due' in task:
					task['due'] = datetime.strptime(task['due'], '%Y%m%dT%H%M%SZ').date()  # convert to datetime.date object
					deleted_tasks.append(task)

			# Return the list of tasks
			return deleted_tasks
		quote = "We are what we repeatedly do. Excellence, then, is not an act, but a habit."
		print(quote)
		warrior = TaskWarrior()
		all_tasks = warrior.load_tasks()

		completed_tasks = all_tasks['completed']
		pending_tasks = all_tasks['pending']

		tasks_today = [task for task in pending_tasks + completed_tasks if 'recur' in task and 'due' in task and parse_date(task['due']).date() == datetime.now().date()]

		deleted_tasks = get_all_deleted_tasks()

		weekly_report = {}
		task_counter = 1  # Start task_counter from 1
		task_map = {}
		completion_rates = []
		total_status_counter = Counter()
		for task in tasks_today:
			status_counter = Counter()
			task_description = task['description']
			task_id = task['id']

			weekly_report[task_counter] = {}

		
			for i in range(8):
				date = datetime.now().date() - timedelta(days=i)

				completed = any(task for task in completed_tasks if task.get('end') and parse_date(task['end']).date() == date and task['description'] == task_description)
				pending = any(task for task in pending_tasks if 'due' in task and parse_date(task['due']).date() == date and task['description'] == task_description)
				deleted = any(task for task in deleted_tasks if task['description'] == task_description and task['due'] == date)

				due = pending

				if completed:
					weekly_report[task_counter][date.strftime('%m-%d')] = '[green]C[/green]'
					status_counter['C'] += 1
				elif deleted:
					weekly_report[task_counter][date.strftime('%m-%d')] = '[red]D[/red]'
					status_counter['D'] += 1
				elif due:
					weekly_report[task_counter][date.strftime('%m-%d')] = '[red bold]P[/red bold]'
					status_counter['P'] += 1
				else:
					weekly_report[task_counter][date.strftime('%m-%d')] = '-'

			completion_percentage = status_counter['C'] / sum(status_counter.values())
			completion_rates.append(completion_percentage)
			color_open, color_close = color_code_percentage(completion_percentage)

			if completion_percentage >= 0.80:
				task_description = f"[white bold]{task_description}[/white bold]"
			task_map[task_counter] = f"{color_open}{completion_percentage:.0%}{color_close} {task_description} [{task_id:02}]"
			
			total_status_counter += status_counter

			task_counter += 1  # Increment task_counter

		total_tasks = sum(total_status_counter.values())		
		average_completion_percentage = mean(completion_rates)

		# Convert the weekly report to a pandas DataFrame
		report_df = pd.DataFrame(weekly_report)

		console = Console()
		table = Table(show_header=True, header_style="bold cyan")

		# Add columns
		table.add_column("Date")
		for col in range(1, len(report_df.columns) + 1):
			table.add_column(f"{col:02}")

		# Add rows
		for date, statuses in report_df.iterrows():
			table.add_row(date, *[str(status) for status in statuses])

		console.print(table)

		for task_number, task_description in task_map.items():
			console.print(f"Task {task_number:02}: {task_description}")
		# Print summary statistics
		console.print(f"\nTotal Tasks: {total_tasks}")
		console.print(f"Tasks Completed: {total_status_counter['C']}")
		console.print(f"Tasks Deleted: {total_status_counter['D']}")
		console.print(f"Tasks Pending: {total_status_counter['P']}")
		console.print(f"Average Completion Rate: {average_completion_percentage:.2%}")

# ==================


	def eisenhower():
		delimiter = '=' * 30
		try:
			filter_query = input(Fore.CYAN + "Enter your Taskwarrior filter:\n ")

			fork = input ("Do you want to asses priority (i) or process (o) the tasks?\n" + Fore.RED)

			if fork == "i":
				tasks = get_tasks(filter_query)

				for task in tasks:
					print(delimiter)
					display_task_details(task['uuid'])
					print(Fore.CYAN + f"\nProcessing task: {task['description']}")
					response = ask_questions()
					if response in ['skip', 'done', 'del']:
						if response == 'skip':
							print(Fore.BLUE + "Skipping task.")
						elif response == 'done':
							run_taskwarrior_command(f"task {task['uuid']} done")
							print(Fore.GREEN + "Marked task as done.")
						elif response == 'del':
							run_taskwarrior_command(f"task {task['uuid']} delete -y")
							print(Fore.GREEN + f"Deleted task {task['uuid']}")
						continue

					urgency, importance = response
					value = urgency * importance

					# Update task with the calculated value
					update_command = f"task {task['uuid']} modify value:{value}"
					run_taskwarrior_command(update_command)
					print(Fore.GREEN + f"Updated task with value: {value}")
			elif fork == "o":
				tasks = get_inbox_tasks(filter_query)
				for task in tasks:
					process_task(task)
		except KeyboardInterrupt:
			print(Fore.RED + "\nProcess interrupted. Exiting.")
			return


	def run_taskwarrior_command(command):
		try:
			result = subprocess.check_output(command, shell=True, text=True)
			return result
		except subprocess.CalledProcessError as e:
			print(f"An error occurred: {e}")
			return None

	def get_tasks(filter_query):
		command = f"task {filter_query} +PENDING -CHILD export"
		output = run_taskwarrior_command(command)
		if output:
			# Parse the JSON output into Python objects
			tasks = json.loads(output)
			return tasks
		else:
			return []

	def ask_question(question):
		while True:
			response = input(question + Fore.WHITE + " (0-5, 'skip', 'done', 'del'): \n:=> ").strip().lower()
			if response in ['skip', 'done', 'del']:
				return response
			try:
				response = int(response)
				if 0 <= response <= 5:
					return response
				else:
					print(Fore.RED + "Please enter a number between 0 and 5.")
			except ValueError:
				print("x_x")
				print(Fore.RED + "Invalid input. Please enter a number between 0 and 5, 'skip', 'done', or 'del'.")
				
				


	def ask_questions():
		print(Fore.RED + "\nAssessing Importance:")
		imp_questions = [
		Fore.BLUE + "Impact on Objectives: How will completing this task impact my short-term and long-term objectives or goals?\n0 - No impact.\n1 - Negligible/Uncertain\n2 - Small impact.\n3 - Medium impact.\n4 - High impact.\n5 - Critical\n",
    Fore.GREEN +  "Consequences of Neglect: What are the consequences if this task is not completed?\n0 - No consequences.\n1 - Minor inconvenience.\n2 - Moderate inconvenience.\n3 - Significant inconvenience.\n4 - Major issue.\n5 - Catastrophic consequences.\n",
    Fore.CYAN +  "Value Addition: How much value does completing this task add to my project or overall work?\n0 - No value.\n1 - Little value.\n2 - Some value.\n3 - Considerable value.\n4 - High value.\n5 - Exceptional value.\n",
    Fore.WHITE +  "Stakeholder Expectations: Are there any stakeholders (like a boss, client, or team) who consider this task critical?\n0 - No stakeholders.\n1 - Low importance to stakeholders.\n2 - Some importance to stakeholders.\n3 - Important to some stakeholders.\n4 - Important to many stakeholders.\n5 - Critical to key stakeholders.\n",
    Fore.YELLOW +  "Development Opportunities: Does this task offer any opportunities for personal or professional growth?\n0 - No growth opportunities.\n1 - Very little growth.\n2 - Some growth.\n3 - Moderate growth.\n4 - Significant growth.\n5 - Exceptional growth.\n",
    Fore.MAGENTA + "Regret Minimization: In 20 years, will I regret not doing this?\n0 - No regret.\n1 - Very little regret.\n2 - Some regret.\n3 - Moderate regret.\n4 - Significant regret.\n5 - Extreme regret.\n"
    ]

		importance_scores = []
		for q in imp_questions:
			score = ask_question(q)
			if score in ['skip', 'done', 'del']:
				return score
			importance_scores.append(score)

		print(Fore.RED + "\nAssessing Urgency:")
		urg_questions = [
		Fore.RED + "Deadlines: Is there a fixed deadline for this task, and how soon is it?\n0 - No deadline.\n1 - Far in the future.\n2 - Somewhat distant.\n3 - Approaching soon.\n4 - Imminent.\n5 - Immediate.\n",
    Fore.CYAN + "Dependency: Are other tasks or people dependent on the completion of this task?\n0 - No dependency.\n1 - Very low dependency.\n2 - Low dependency.\n3 - Moderate dependency.\n4 - High dependency.\n5 - Critical dependency.\n",
    Fore.BLUE + "Time Sensitivity: Will the task become more difficult or impossible if not done soon?\n0 - Not time-sensitive.\n1 - Very low sensitivity.\n2 - Low sensitivity.\n3 - Moderate sensitivity.\n4 - High sensitivity.\n5 - Extremely time-sensitive.\n",
    Fore.WHITE + "Risk of Delay: What are the risks or costs associated with delaying this task?\n0 - No risks.\n1 - Very low risk.\n2 - Low risk.\n3 - Moderate risk.\n4 - High risk.\n5 - Extreme risk.\n",
    Fore.YELLOW + "Immediate Benefit: Is there an immediate benefit or relief from completing this task quickly?\n0 - No immediate benefit.\n1 - Very little benefit.\n2 - Some benefit.\n3 - Considerable benefit.\n4 - High benefit.\n5 - Exceptional benefit.\n"
    ]

		urgency_scores = []
		for q in urg_questions:
			score = ask_question(q)
			if score in ['skip', 'done', 'del']:
				return score
			urgency_scores.append(score)

		total_importance = sum(importance_scores)
		total_urgency = sum(urgency_scores)

		return total_urgency, total_importance
		
	def display_task_details(task_uuid):
		command = f"task {task_uuid} export"
		output = run_taskwarrior_command(command)
		if output:
			task_details = json.loads(output)
			if task_details:
				task = task_details[0]  # Assuming the first item is the task we want
				for key, value in task.items():
					print(f"{key}: {value}")
			else:
				print(Fore.RED + "No task details found.")
		else:
			print(Fore.RED + "Failed to retrieve task details.")

	# =========================================================


	def run_taskwarrior_command(command):
		try:
			result = subprocess.check_output(command, shell=True, text=True)
			return result
		except subprocess.CalledProcessError as e:
			print(f"An error occurred: {e}")
			return None

	def get_inbox_tasks(filter):
		command = f"task {filter} +PENDING -CHILD export"
		output = run_taskwarrior_command(command)
		if output:
			tasks = json.loads(output)
			return tasks
		else:
			return []

	def process_input(lines):
		level_text = {0: ''}
		last_level = -1
		spaces_per_level = 2  # adjust this if needed

		# Ignore the first 4 and last 3 lines
		lines = lines[4:-3]

		output_lines = []  # Initialize the list to store all processed projects

		for line in lines:
			stripped = line.lstrip()
			level = len(line) - len(stripped)

			# Split the line into text and number, and only keep the text
			text = stripped.split()[0]

			if level % spaces_per_level != 0:
				raise ValueError('Invalid indentation level in input')

			level //= spaces_per_level

			if level > last_level + 1:
				raise ValueError('Indentation level increased by more than 1')

			level_text[level] = text

			# Clear all deeper levels
			level_text = {k: v for k, v in level_text.items() if k <= level}

			output_line = '.'.join(level_text[l] for l in range(level + 1))

			output_lines.append(output_line)  # Add each processed project to the list

			last_level = level
		
		return output_lines  # Return the list of all processed projects


	def call_and_process_task_projects2():
		result = subprocess.run(['task', 'projects'], capture_output=True, text=True)
		lines = result.stdout.splitlines()
		project_list = process_input(lines)
		return project_list

	def search_project2(project_list):
		completer = FuzzyWordCompleter(project_list)
		item_name = prompt("Enter a project name: ", completer=completer)
		closest_match, match_score = process.extractOne(item_name, project_list)

		# You can adjust the threshold based on how strict you want the matching to be
		MATCH_THRESHOLD = 80  # For example, 80 out of 100

		if match_score >= MATCH_THRESHOLD:
			return closest_match
		else:
			return item_name  # Use the new name entered by the user

	def display_task_details(task_uuid):
		command = f"task {task_uuid} export"
		output = run_taskwarrior_command(command)
		if output:
			task_details = json.loads(output)
			if task_details:
				task = task_details[0]  # Assuming the first item is the task we want
				for key, value in task.items():
					print(f"{key}: {value}")
			else:
				print(Fore.RED + "No task details found.")
		else:
			print(Fore.RED + "Failed to retrieve task details.")

	def add_new_task_to_project(project_name):
		while True:
			new_task_description = input("Enter the description for the new task (or press Enter to stop adding tasks): ")
			if new_task_description.lower() in ['exit','']:
				break

			if new_task_description:
				command = f"task add {new_task_description} project:{project_name} -in"
				run_taskwarrior_command(command)
				print(Fore.GREEN + "New task added to the project.")

	def process_task(task):
		print(Fore.YELLOW + f"\nProcessing task: {task['description']}")
		action = input("Choose action: modify (mod) /skip (s) /delete (del) /done (d)):\n ").strip().lower()

		if action == 'mod':
			print(Fore.YELLOW + "Task details:")
			display_task_details(task['uuid'])
			mod_confirm = input("Do you want to modify this task? (yes/no):\n ").strip().lower()
			if mod_confirm in ['yes','y']:
				modification = input("Enter modification (e.g., '+tag @context priority'):\n ")
				run_taskwarrior_command(f"task {task['uuid']} modify {modification} -in")

			pro_confirm = input("Do you want to assign this task to a project? (yes/no):\n ").strip().lower()
			if pro_confirm in ['yes','y']:
				project_list = call_and_process_task_projects2()
				selected_project = search_project2(project_list)
				run_taskwarrior_command(f"task {task['uuid']} modify project:{selected_project} -in")
				print(Fore.GREEN + f"Task categorized under project: {selected_project}\n")

				# Ask if user wants to add another task to the same project
				add_another = input("Do you want to add another task to this project? (yes/no): ").strip().lower()
				if add_another in ['yes', 'y']:
					add_new_task_to_project(selected_project)
		elif action == 'skip':
			print(Fore.BLUE + "Skipping task.")
		elif action == 'del':
			run_taskwarrior_command(f"task {task['uuid']} delete -y")
			print(Fore.RED + f"Deleted task {task['uuid']}")
		elif action == 'd':
			run_taskwarrior_command(f"task {task['uuid']} done")
			print(Fore.GREEN + f"Marked = {task['uuid']} = as done.")

			# =========================================================

	def parse_datetime(due_date_str):
		try:
			return datetime.strptime(due_date_str, "%Y%m%dT%H%M%SZ") if due_date_str else None
		except ValueError:
			return None

	def display_tasks(command):
		from rich.tree import Tree
		from rich.text import Text
		from rich.console import Console
		from collections import defaultdict
		import sys
		result = subprocess.run(command, shell=True, capture_output=True, text=True)
		console = Console()

		if result.stdout:
			tasks = json.loads(result.stdout)
			if not tasks:
				console.print("No tasks found.", style="bold red")
				return

			project_tag_map = defaultdict(lambda: defaultdict(list))

			for task in tasks:
				project = task.get('project', 'No Project')
				tags = task.get('tags', ['No Tag'])
				description = task['description']
				task_id = str(task['id'])
				due_date_str = task.get('due')
				due_date = parse_datetime(due_date_str)
				annotations = task.get('annotations', [])

				for tag in tags:
					project_tag_map[project][tag].append((task_id, description, due_date, annotations))

			tree = Tree("Task Overview", style="green")

			for project, tags in project_tag_map.items():
				if project == 'No Project' and not any(tags.values()):
					continue

				project_levels = project.split(".")
				current_branch = tree

				for level in project_levels:
					# Adding or finding the branch for each project level
					found_branch = None
					for child in current_branch.children:
						if child.label.plain == level:
							found_branch = child
							break
					if not found_branch:
						found_branch = current_branch.add(Text(level, style="yellow"))
					current_branch = found_branch

				for tag, tasks in tags.items():
					if not tasks:
						continue
					tag_branch = current_branch.add(Text(tag, style="blue"))


					for task_id, description, due_date, annotations in sorted(tasks, key=lambda x: (x[2] is None, x[2])):
						# Task ID in red with square brackets
						task_id_text = Text(f"[{task_id}] ", style="red")
						# Description in white
						description_text = Text(description + " ", style="white")
						# Due date in green
						due_date_text = Text(due_date.strftime("%Y-%m-%d") if due_date else "", style="green")
						# Combine texts for one line
						task_line = task_id_text + description_text + due_date_text
						task_branch = tag_branch.add(task_line)

						if annotations:
							annotation_branch = task_branch.add(Text("Annotations:", style="italic white"))
							for annotation in annotations:
								entry_datetime = datetime.strptime(annotation['entry'], "%Y%m%dT%H%M%SZ").strftime('%Y-%m-%d %H:%M:%S')
								annotation_text = Text(f"{entry_datetime} - {annotation['description']}", style="dim white")
								annotation_branch.add(annotation_text)

			console.print(tree)
		else:
			console.print("No tasks found.", style="bold red")

	from rich.console import Console
	from rich.table import Table
	from rich.prompt import Prompt

	def display_menu(console):

		# console = Console()
		table = Table(show_header=True, header_style="bold yellow")
		table.add_column("Key", style="dim", width=2)
		table.add_column("Action", min_width=20)
		table.add_row("d", "Today's Tasks")
		table.add_row("y", "Yesterday's Tasks")
		table.add_row("t", "Tomorrow's Tasks")
		table.add_row("w", "Current Week's Tasks")
		table.add_row("m", "Current Month's Tasks")
		table.add_row("l", "View Long-Term Plan")
		table.add_row("o", "Overdue Tasks")
		table.add_row("i", "Inbox Tasks")
		table.add_row("h", "Handle Tasks")
		table.add_row("b", "Back to main")
		table.add_row("", "Exit")

		console.print(table)

	def task_control_center():
		console = Console()
		while True:
			console.print("[bold cyan]Task Control Center[/bold cyan]", justify="center")
			display_menu(console)
			choice = Prompt.ask("[bold yellow]Enter your choice[/bold yellow]")
			scope_command_map = {
				'd': "task due:today +PENDING export",
				'y': "task due:yest +PENDING export",
				't': "task due:tomo +PENDING export",
				'w': "task +WEEK +PENDING export",
				'm': "task +MONTH +PENDING export",
				'o': "task +OVERDUE +PENDING export"
			}

			if choice in scope_command_map:
				console.clear()
				display_tasks(scope_command_map[choice])
			elif choice == 'l':
				console.clear()
				display_due_tasks()
			elif choice == 'i':
				console.clear()
				display_inbox_tasks()
			elif choice == 'h':
				handle_task()
			elif choice == 'b':
				main_menu()
			elif choice == '':
				console.clear()
				break
			else:
				console.print("Invalid choice. Please try again.", style="bold red")



	def main_menu():
		script_directory = os.path.dirname(os.path.abspath(__file__))
		file_path = os.path.join(script_directory, "sultandb.json")
		interactive_prompt(file_path)
# ==================

	delimiter = ('-' * 40)
	if __name__ == "__main__":
		main()
		

	#script_directory = os.path.dirname(os.path.abspath(__file__))
	#file_path = os.path.join(script_directory, "sultandb.json")

	#interactive_prompt(file_path)
	

except KeyboardInterrupt:
	print("\nYou have to be your own hero.\n\nDo the impossible and you are never going to doubt yourself again!")
