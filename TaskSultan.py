from tasklib import TaskWarrior, Task
from taskw import TaskWarrior as Warrior
import datetime
import inquirer
from colorama import init, Fore, Back, Style
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from collections import Counter
from termcolor import colored

# from itertools import zip_longest
# import textwrap
from dateutil.parser import parse
import pytz
import questionary
from questionary import Style
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.completion import FuzzyCompleter, WordCompleter
import subprocess
import argparse
import os
import calendar
from datetime import date

# import texttable as tt
import pandas as pd
from fuzzywuzzy import process
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table

# from rich import print as rprint
from rich.panel import Panel
from rich.text import Text
from rich import box
import re
from enum import Enum
from rich.prompt import IntPrompt
from itertools import groupby

# from operator import itemgetter


from datetime import datetime, timedelta
import sys

try:
    import ujson as json
except ImportError:
    import json

import warnings

warnings.filterwarnings("ignore")


# for project trees --- Define lists of colors for levels and guide styles
level_colors = [
    "bright_red",
    "bright_green",
    "bright_yellow",
    "bright_blue",
    "bright_magenta",
    "bright_cyan",
    "bright_white",
]
guide_styles = ["red", "green", "yellow", "blue", "magenta", "cyan", "white"]


# local_tz = pytz.timezone('Europe/London')  # Replace with your local timezone
local_tz = datetime.now().astimezone().tzinfo  # Determine local timezone

colors = [
    "grey93",
    "honeydew2",
    "hot_pink",
    "hot_pink2",
    "hot_pink3",
    "indian_red",
    "indian_red1",
    "khaki1",
    "khaki3",
    "light_coral",
    "light_cyan1",
    "light_cyan3",
    "light_goldenrod1",
    "light_goldenrod2",
    "light_goldenrod3",
    "light_green",
    "light_pink1",
    "light_pink3",
    "light_pink4",
    "light_salmon1",
    "light_salmon3",
    "light_sea_green",
    "light_sky_blue1",
    "light_sky_blue3",
    "light_slate_blue",
    "light_slate_gray",
    "light_slate_grey",
    "light_steel_blue",
    "light_steel_blue1",
    "light_steel_blue3",
    "light_yellow3",
    "magenta",
    "magenta1",
    "magenta2",
    "magenta3",
    "medium_orchid",
    "medium_orchid1",
    "medium_orchid3",
    "medium_purple",
    "medium_purple1",
    "medium_purple2",
    "medium_purple3",
    "medium_purple4",
    "medium_spring_green",
    "medium_turquoise",
    "medium_violet_red",
    "misty_rose1",
    "misty_rose3",
    "navajo_white1",
    "navajo_white3",
    "navy_blue",
    "orange1",
    "orange3",
    "orange4",
    "orange_red1",
    "orchid",
    "orchid1",
    "orchid2",
    "pale_green1",
    "pale_green3",
    "pale_turquoise1",
    "pale_turquoise4",
    "pale_violet_red1",
    "pink1",
    "pink3",
    "plum1",
    "plum2",
    "plum3",
    "plum4",
    "purple",
    "purple3",
    "purple4",
    "red",
    "red1",
    "red3",
    "rosy_brown",
    "royal_blue1",
    "salmon1",
    "sandy_brown",
    "sea_green1",
    "sea_green2",
    "sea_green3",
    "sky_blue1",
    "sky_blue2",
    "sky_blue3",
    "slate_blue1",
    "slate_blue3",
    "spring_green1",
    "spring_green2",
    "spring_green3",
    "spring_green4",
    "steel_blue",
    "steel_blue1",
    "steel_blue3",
    "tan",
    "thistle1",
    "thistle3",
    "turquoise2",
    "turquoise4",
    "violet",
    "wheat1",
    "wheat4",
    "white",
    "yellow",
    "yellow1",
    "yellow2",
    "yellow3",
    "yellow4",
    "bright_blue",
    "bright_cyan",
    "bright_green",
    "bright_magenta",
    "bright_red",
    "bright_white",
    "bright_yellow",
    "cadet_blue",
    "chartreuse1",
    "chartreuse2",
    "chartreuse3",
    "chartreuse4",
    "cornflower_blue",
    "cornsilk1",
    "cyan",
    "cyan1",
    "cyan2",
    "cyan3",
    "dark_blue",
    "dark_cyan",
    "dark_goldenrod",
    "dark_green",
    "dark_khaki",
    "dark_magenta",
    "dark_olive_green1",
    "dark_olive_green2",
    "dark_olive_green3",
    "dark_orange",
    "dark_orange3",
    "dark_red",
    "dark_sea_green",
    "dark_sea_green1",
    "dark_sea_green2",
    "dark_sea_green3",
    "dark_sea_green4",
    "dark_slate_gray1",
    "dark_slate_gray2",
    "dark_slate_gray3",
    "dark_turquoise",
    "dark_violet",
    "deep_pink1",
    "deep_pink2",
    "deep_pink3",
    "deep_pink4",
    "deep_sky_blue1",
    "deep_sky_blue2",
    "deep_sky_blue3",
    "deep_sky_blue4",
    "dodger_blue1",
    "dodger_blue2",
    "dodger_blue3",
    "gold1",
    "gold3",
]


# Load project metadata
script_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_directory, "sultandb.json")


from functools import lru_cache


@lru_cache(maxsize=None)
def load_sultandb(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            sultandb = json.load(file)
    except FileNotFoundError:
        sultandb = {"aors": [], "projects": []}
    return sultandb["aors"], sultandb["projects"]


aors, projects = load_sultandb(file_path)


def save_sultandb(file_path, aors, projects):
    sultandb = {"aors": aors, "projects": projects}
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(sultandb, file, default=str, indent=4)
    # Invalidate the cache of load_sultandb
    load_sultandb.cache_clear()


warrior = Warrior()
console = Console()


def main():
    # Map each command to its corresponding function
    command_to_function = {
        "s": search_task,
        "c": clear_data,
        "b": basic_summary,
        "d": detailed_summary,
        "a": all_summary,
        "i": display_inbox_tasks,
        "tl": display_due_tasks,
        "ht": handle_task,
        "tc": task_control_center,
        "td": print_tasks_for_selected_day,
        "sp": call_and_process_task_projects,
        "o": display_overdue_tasks,
        "rr": recurrent_report,  # includes only the period type recurrent tasks
        "z": eisenhower,
        "pi": greeting_pi,
        "tm": task_manager,
        "n": next_summary,
        "rp": review_projects,
        "to": task_organizer,
        "mp": multiple_projects_view,
    }

    parser = argparse.ArgumentParser(description="Process some commands.")
    parser.add_argument(
        "command",
        metavar="CMD",
        type=str,
        nargs="?",
        default="",
        help="A command to run",
    )
    parser.add_argument(
        "arg",
        metavar="ARG",
        type=str,
        nargs="?",
        default=None,
        help="Optional argument for the command",
    )

    args = parser.parse_args()

    if args.command:
        if args.command in command_to_function:
            if args.arg:
                # If a secondary argument is provided, pass it to the function
                command_to_function[args.command](args.arg)
            else:
                # Call the corresponding function if no secondary argument is provided
                command_to_function[args.command]()
        else:
            print("Invalid command provided.")
    else:
        # Continue to the interactive prompt if no command argument is provided
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

    def sync_sultandb_with_taskwarrior(file_path):
        # import os
        # import json
        # import subprocess

        # Load existing data from sultandb.json
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                sultandb = json.load(file)
        except FileNotFoundError:
            sultandb = {"aors": [], "projects": []}

        aors = sultandb.get("aors", [])
        projects = sultandb.get("projects", [])

        # Fetch projects from Taskwarrior
        command = ["task", "_projects"]
        result = subprocess.run(command, stdout=subprocess.PIPE)
        task_projects = result.stdout.decode("utf-8").splitlines()

        # Separate AoRs and normal projects
        task_aors = [p for p in task_projects if p.startswith("AoR.")]
        task_projects = [p for p in task_projects if not p.startswith("AoR.")]

        # Create sets for fast lookup
        existing_aor_names = set(aor["name"] for aor in aors)
        existing_project_names = set(project["name"] for project in projects)

        # Add new AoRs from Taskwarrior
        new_aors = []
        for aor_name in task_aors:
            aor_name_without_prefix = aor_name[4:]  # Remove "AoR." prefix
            if aor_name_without_prefix not in existing_aor_names:
                new_aor = {
                    "name": aor_name_without_prefix,
                    "description": "",
                    "standard": "",
                    "annotations": [],
                    "workLogs": [],
                    "status": "Active",
                }
                aors.append(new_aor)
                new_aors.append(aor_name_without_prefix)

        # Add new projects from Taskwarrior
        new_projects = []
        for project_name in task_projects:
            if project_name not in existing_project_names:
                new_project = {
                    "name": project_name,
                    "description": "",
                    "outcome": "",
                    "annotations": [],
                    "workLogs": [],
                    "status": "Active",
                }
                projects.append(new_project)
                new_projects.append(project_name)

        # Update status of existing AoRs
        task_aor_names = set(aor[4:] for aor in task_aors)  # Remove "AoR." prefix
        for aor in aors:
            if aor["name"] in task_aor_names:
                if aor.get("status") != "Active":
                    aor["status"] = "Active"
            else:
                if aor.get("status") != "Completed":
                    aor["status"] = "Completed"

        # Update status of existing projects
        task_project_names = set(task_projects)
        for project in projects:
            if project["name"] in task_project_names:
                if project.get("status") != "Active":
                    project["status"] = "Active"
            else:
                if project.get("status") != "Completed":
                    project["status"] = "Completed"

        # Save the updated sultandb data
        sultandb["aors"] = aors
        sultandb["projects"] = projects

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(sultandb, file, indent=4)

        # Print status message
        print("Synchronization complete.")
        if new_aors:
            print(f"Added new AoRs: {', '.join(new_aors)}")
        if new_projects:
            print(f"\nAdded new projects: {', '.join(new_projects)}\n")
        if not new_aors and not new_projects:
            print("\nNo new AoRs or projects were added.\n")

    def display_overdue_tasks():
        tasks = warrior.load_tasks()
        print(colored("Overdue Tasks", "yellow", attrs=["bold"]))
        include_recurrent = questionary.confirm(
            "Include recurrent tasks in the search?", default=False
        ).ask()
        if include_recurrent:
            tasks = tasks["pending"]
        else:
            tasks = [task for task in tasks["pending"] if "recur" not in task]

        # Determine local timezone
        # local_tz = datetime.now().astimezone().tzinfo

        # Filter tasks for overdue tasks only
        overdue_tasks = []
        now = datetime.now(local_tz)
        for task in tasks:
            due_date_str = task.get("due")
            if due_date_str:
                due_date = datetime.strptime(due_date_str, "%Y%m%dT%H%M%SZ").replace(
                    tzinfo=pytz.UTC
                )
                due_date = due_date.astimezone(local_tz)  # Convert to local time
                if due_date < now:
                    time_remaining = now - due_date
                    task["time_remaining"] = (
                        str(time_remaining.days) + " days"
                    )  # Calculate time remaining in days
                    overdue_tasks.append(task)

        # Sort overdue tasks by due date (oldest to newest)
        overdue_tasks.sort(key=lambda task: task["due"])

        # Display overdue tasks
        if overdue_tasks:
            for task in overdue_tasks:
                task_id = colored(f"{task['id']}", "yellow")
                if task.get("value"):
                    task_value = colored(f"{int(task['value'])}", "red", attrs=["bold"])
                else:
                    task_value = ""

                description = colored(task["description"], "cyan")
                tag = colored(
                    ",".join(task.get("tags", [])), "red", attrs=["bold"]
                )  # Join tags with comma
                project = colored(task.get("project", ""), "blue", attrs=["bold"])
                time_remaining = colored(
                    task.get("time_remaining", ""), "green", attrs=["bold"]
                )  # Display time remaining

                print(
                    f"{task_id} {description} {task_value} {tag} {project} -{time_remaining}"
                )

                if "annotations" in task:  # Ensure annotations are in the task
                    for annotation in task["annotations"]:
                        entry_date = datetime.strptime(
                            annotation["entry"], "%Y%m%dT%H%M%SZ"
                        ).date()
                        print(
                            f"\t{Fore.CYAN}{entry_date}{Fore.YELLOW}: {annotation['description']}"
                        )
            print("=" * 60)
        else:
            print("No overdue tasks found.")

    def print_tasks_for_selected_day():
        # Initialize colorama
        init(autoreset=True)

        def get_deleted_tasks_due_today(date):
            # Run the 'task export' command and get the output
            result = subprocess.run(["task", "export"], stdout=subprocess.PIPE)

            # Load the output into Python as JSON
            all_tasks = json.loads(result.stdout)

            # Prepare a list to store tasks
            deleted_tasks_due_today = []

            # Iterate over all tasks
            for task in all_tasks:
                # Check if task status is 'deleted' and if it's due date is today
                if (
                    task["status"] == "deleted"
                    and "due" in task
                    and datetime.strptime(task["due"], "%Y%m%dT%H%M%SZ").date() == date
                ):
                    deleted_tasks_due_today.append(task)

            # Return the list of tasks
            return deleted_tasks_due_today

        def parse_date(date_str):
            utc_time = datetime.strptime(date_str, "%Y%m%dT%H%M%SZ")
            return utc_time.replace(tzinfo=timezone.utc).astimezone(tz=None)

        user_choice = (
            input(
                "Do you want to display tasks for yesterday (y), today (t), or tomorrow (tm)? (y/t/tm): "
            )
            .strip()
            .lower()
        )
        if user_choice not in (
            "yesterday",
            "yd",
            "y",
            "today",
            "td",
            "t",
            "tomorrow",
            "tm",
        ):
            print("Default choice, today tasks displayed.")
            user_choice = "today"

        if user_choice in ("today", "td", "t"):
            date = datetime.now().date()
            print(f"Selected tasks for {date}")
        elif user_choice in ("tomorrow", "tm"):
            date = datetime.now().date() + timedelta(days=1)
            print(f"Selected tasks for {date}")
        elif user_choice in ("yesterday", "yd", "y"):
            date = datetime.now().date() - timedelta(days=1)
            print(f"Selected tasks for {date}")
        else:
            date = datetime.now().date()
            print(f"Selected tasks for {date}")

        w = Warrior()
        pending_tasks = w.load_tasks()["pending"]
        completed_tasks = w.load_tasks()["completed"]
        deleted_tasks = get_deleted_tasks_due_today(date)

        due_tasks = sorted(
            (
                task
                for task in pending_tasks
                if task.get("due") and parse_date(task["due"]).date() == date
            ),
            key=lambda task: parse_date(task["due"]),
        )

        completed_tasks = sorted(
            (
                task
                for task in completed_tasks
                if task.get("end") and parse_date(task["end"]).date() == date
            ),
            key=lambda task: parse_date(task["end"]),
        )

        tasks_dict = {}
        for task_list in [due_tasks, completed_tasks, deleted_tasks]:
            for task in task_list:
                local_time = (
                    parse_date(task["due"])
                    if task.get("due")
                    else parse_date(task["end"])
                )
                hour = local_time.hour
                minute = local_time.minute
                time_key = (hour, minute)
                task_status = task.get("status")
                task_id_or_deleted = (
                    "[DELETED]" if task in deleted_tasks else task.get("id")
                )
                task_info = (
                    task["description"],
                    task.get("duration", 0),
                    task_id_or_deleted,
                    task.get("project"),
                    task.get("tags"),
                    task_status,
                    task.get("annotations"),
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

                    for (
                        task,
                        duration,
                        task_id,
                        project,
                        tags,
                        status,
                        annotations,
                    ) in tasks_dict[time_key]:
                        project_color = (
                            Fore.GREEN
                            if project and project.startswith("AoR.")
                            else Fore.BLUE
                        )
                        task_id_or_completed = (
                            f"{Fore.GREEN}[COMPLETED]{Fore.RESET}"
                            if status == "completed"
                            else f"{Fore.RED} {task_id}"
                        )
                        task_details = f"{Fore.YELLOW}{hour:02d}:{minute:02d} {task_id_or_completed}, {Fore.RESET}{task} [{duration} mins], {project_color}Pro:{project}, {Fore.RED}{tags}"
                        print(task_details)
                        if annotations:
                            # print(f"{Fore.MAGENTA}Annotations:")
                            for annotation in annotations:
                                entry_date = parse_date(annotation["entry"]).date()
                                print(
                                    f"\t{Fore.CYAN}{entry_date}{Fore.YELLOW}: {annotation['description']}"
                                )

                if (
                    user_choice in ("today", "td")
                    and hour == current_time.hour
                    and minute == current_time.minute
                ):
                    print(
                        f"{Fore.CYAN}{current_time.strftime('%H:%M')}{'=' * 25} {Fore.WHITE}Present Moment {Fore.RESET}{Fore.CYAN}{'=' * 25}{Fore.RESET}"
                    )

            if not hour_printed:
                print(f"{Fore.BLUE}{hour:02d}:00")

        if (
            user_choice in ("today", "td")
            and current_time.hour == 23
            and current_time.minute == 59
        ):
            print(f"{'=' * 25} {Fore.WHITE}Present Moment {Fore.RESET}{'=' * 25}")

        if len(due_tasks) == 0:
            print(
                f"\n\t{Fore.BLACK}{Back.LIGHTCYAN_EX}  No pending tasks!{Fore.RESET}{Back.RESET}"
            )
        else:
            print(
                f"\n\t\033[1m{len(due_tasks)} pending tasks out of {len(due_tasks) + len(completed_tasks)} total. {len(completed_tasks)} completed and {len(deleted_tasks)} deleted!"
            )

        print_calendar_with_marked_day(date.year, date.month, date.day)
        while True:
            action = questionary.select(
                "What do you want to do next?", choices=["Refresh", "Exit"]
            ).ask()

            # CTRL+C actionx
            action = "Exit" if action is None else action

            if action == "Refresh":
                print_tasks_for_selected_day()  # Refresh and show data again
            elif action == "Exit":
                print("Exit")
                break

    def search_task():
        tasks = warrior.load_tasks()

        include_completed = questionary.confirm(
            "Include completed tasks in the search?", default=False
        ).ask()
        if include_completed:
            tasks = tasks["pending"] + tasks["completed"]
        else:
            tasks = tasks["pending"]

        task_descriptions = [task.get("description") for task in tasks]
        completer = FuzzyWordCompleter(task_descriptions)

        task_description = prompt("Enter a task description: ", completer=completer)

        selected_task = next(
            (task for task in tasks if task.get("description") == task_description),
            None,
        )

        if selected_task:
            print(
                f"{Fore.BLUE}ID:{Fore.RESET} {Fore.RED}{selected_task.get('id')}{Fore.RESET}"
            )
            print(
                f"{Fore.BLUE}Description:{Fore.RESET} {Fore.YELLOW}{selected_task.get('description')}{Fore.RESET}"
            )
            print(
                f"{Fore.BLUE}Project:{Fore.RESET} {Fore.YELLOW}{selected_task.get('project')}{Fore.RESET}"
            )
            print(
                f"{Fore.BLUE}Tags:{Fore.RESET} {Fore.YELLOW}{', '.join(selected_task.get('tags', []))}{Fore.RESET}"
            )
            due_date_str = selected_task.get("due")
            due_date = (
                parse(due_date_str).replace(tzinfo=timezone.utc)
                if due_date_str
                else None
            )
            if due_date:
                now = datetime.now(timezone.utc)
                time_remaining = due_date - now
                print(
                    f"{Fore.BLUE}Due:{Fore.RESET} {Fore.YELLOW}{due_date}{Fore.RESET}\n{Fore.BLUE}Time Remaining:{Fore.RESET} {Fore.YELLOW}{time_remaining.days} days, {time_remaining.seconds // 3600}:{time_remaining.seconds % 3600 // 60}{Fore.RESET}"
                )
        else:
            print("No task found with that description.")

    def display_inbox_tasks():
        tasks = warrior.load_tasks()["pending"]
        delimiter = "-" * 40
        # Filter tasks with the tag "in"
        inbox_tasks = [task for task in tasks if "in" in task.get("tags", [])]

        # Parse entry dates and calculate time deltas
        for task in inbox_tasks:
            entry_date = (
                datetime.strptime(task["entry"], "%Y%m%dT%H%M%SZ")
                .replace(tzinfo=timezone.utc)
                .astimezone(tz=None)
            )
            task["time_delta"] = (
                datetime.now(timezone.utc).astimezone(tz=None) - entry_date
            )

        # Sort tasks by their time deltas
        inbox_tasks.sort(key=lambda task: task["time_delta"])

        # Print tasks
        print(f"{Fore.RED}{delimiter}{Fore.RESET}")
        for task in inbox_tasks:
            # Format time delta as days
            days = task["time_delta"].days
            formatted_days = f"-{days:02d}d"  # Adds leading zero if days < 10
            print(
                f"{Fore.CYAN}{task['id']}{Fore.RESET}, {Fore.GREEN}{formatted_days}{Fore.RESET}, {Fore.YELLOW}{task['description']}{Fore.RESET}"
            )
        print(f"{Fore.BLUE}{delimiter}{Fore.RESET}")

    def handle_task():
        print("Please enter the task command:")
        print("Examples:")
        print("'223,114,187 done' - Marks tasks 223, 114, and 187 as done.")
        # print("!!!! The operation will be done without asking for confirmation!.")
        print("To return to the main menu, press 'Enter'.\n")
        print("----------------------------------------------\n")

        while True:
            task_command = input()
            if task_command.lower() == "":
                return
            else:
                subprocess.run(f"task {task_command}", shell=True)

    def display_due_tasks():
        tasks = warrior.load_tasks()

        include_recurrent = questionary.confirm(
            "Include recurrent tasks in the search?", default=False
        ).ask()
        if include_recurrent:
            tasks = tasks["pending"]
        else:
            tasks = [task for task in tasks["pending"] if "recur" not in task]

        # Determine local timezone
        # local_tz = datetime.now().astimezone().tzinfo

        # Define time frames
        now = datetime.now(local_tz)
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_overdue = start_of_day - timedelta(days=365)
        end_of_today = start_of_day + timedelta(days=1)
        end_of_tomorrow = end_of_today + timedelta(days=1)
        # This should point to next Monday
        start_of_next_week = start_of_day + timedelta(
            days=(7 - start_of_day.weekday()) % 7
        )
        end_of_next_week = start_of_next_week + timedelta(
            days=6
        )  # This should point to next Sunday
        # This should point to day after tomorrow
        start_of_rest_of_the_week = end_of_tomorrow
        # This should point to the end of this week (Sunday)
        end_of_rest_of_the_week = start_of_next_week - timedelta(seconds=1)
        start_of_next_2_weeks = start_of_next_week
        end_of_next_2_weeks = start_of_next_2_weeks + timedelta(
            days=15
        )  # Updated to include 2 weeks + 1 day
        start_of_next_3_weeks = start_of_next_week
        end_of_next_3_weeks = start_of_next_3_weeks + timedelta(days=21)
        end_of_next_3_months = start_of_day + timedelta(days=90)
        end_of_next_6_months = start_of_day + timedelta(days=180)
        end_of_next_year = start_of_day + timedelta(days=365)
        end_of_next_3_years = start_of_day + timedelta(days=365 * 3)
        end_of_next_5_years = start_of_day + timedelta(days=365 * 5)
        end_of_next_10_years = start_of_day + timedelta(days=365 * 10)
        end_of_next_20_years = start_of_day + timedelta(days=365 * 20)

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
            ("Rest of the Week", start_of_rest_of_the_week, end_of_rest_of_the_week),
            ("Tomorrow", end_of_today, end_of_tomorrow),
            ("Today", start_of_day, end_of_today),
            ("Overdue", start_of_overdue, start_of_day),
        ]

        # Categorize tasks
        categorized_tasks = {name: [] for name, _, _ in time_frames}
        for task in tasks:
            due_date_str = task.get("due")
            if due_date_str:
                due_date = datetime.strptime(due_date_str, "%Y%m%dT%H%M%SZ").replace(
                    tzinfo=pytz.UTC
                )
                due_date = due_date.astimezone(local_tz)  # Convert to local time
                for name, start, end in time_frames:
                    if start is None or (start <= due_date < end):
                        if name == "Today":
                            delta = ""
                        else:
                            delta = due_date - now
                            days, seconds = delta.days, delta.seconds
                            hours = seconds // 3600
                            minutes = (seconds % 3600) // 60
                            task["time_remaining"] = (
                                f"{days} days, {hours}:{minutes:02d}"  # Calculate time remaining
                            )
                            categorized_tasks[name].append(task)
                        break

        # Display tasks
        for name, tasks in list(categorized_tasks.items()):
            if tasks:
                print(colored(name, "yellow", attrs=["bold"]))
                for task in tasks:
                    task_id = colored(f"[{task['id']}]", "yellow")
                    description = colored(task["description"], "white")
                    tag = colored(
                        ",".join(task.get("tags", [])), "red", attrs=["bold"]
                    )  # Join tags with comma
                    project = colored(task.get("project", ""), "blue", attrs=["bold"])
                    time_remaining = colored(
                        task.get("time_remaining", ""), "green", attrs=["bold"]
                    )  # Display time remaining

                    print(f"{task_id} {description} {tag} {project} {time_remaining}")

                    if "annotations" in task:  # Ensure annotations are in the task
                        for annotation in task["annotations"]:
                            entry_date = datetime.strptime(
                                annotation["entry"], "%Y%m%dT%H%M%SZ"
                            ).date()
                            print(
                                f"\t{Fore.CYAN}{entry_date}{Fore.YELLOW}: {annotation['description']}"
                            )
                print("=" * 60)

        # # Display tasks # each category in its own table
        # for name, tasks in list(categorized_tasks.items()):
        # 	if tasks:
        # 		table = Table(title=Text(name, style="yellow bold"), expand=True)
        # 		table.add_column("ID", style="yellow", no_wrap=True)
        # 		table.add_column("Description", style="cyan")
        # 		table.add_column("Tags", style="red")
        # 		table.add_column("Project", style="blue")
        # 		table.add_column("Time Remaining", style="green")

        # 		for task in tasks:
        # 			task_id = f"[{task['id']}]"
        # 			description = task['description']
        # 			tags = ','.join(task.get('tags', []))
        # 			project = task.get('project', '')
        # 			time_remaining = task.get('time_remaining', '')

        # 			table.add_row(task_id, description, tags, project, time_remaining)

        # 			if 'annotations' in task:
        # 				for annotation in task['annotations']:
        # 					entry_date = datetime.strptime(annotation['entry'], '%Y%m%dT%H%M%SZ').date()
        # 					table.add_row("", Text(f"{entry_date}: {annotation['description']}", style="dim italic"), "", "", "")

        # 		console.print(Panel(table, expand=False))
        # 		console.print()

    def get_item_info(user_input):
        print(user_input + "this needs work")

    def mark_item_inactive(item_name, aors, projects):
        for item in aors:
            if item["name"] == item_name:
                item["status"] = "Completed"

        for item in projects:
            if item["name"] == item_name:
                item["status"] = "Completed"

    def get_creation_date(item_name):
        tasks = warrior.load_tasks()
        for task in tasks["pending"]:
            project = task.get("project")
            if project and (
                project == item_name or project.startswith("AoR." + item_name)
            ):
                created = task.get("entry")
                if created:
                    print(datetime.strptime(created, "%Y%m%dT%H%M%SZ"))
                    return datetime.strptime(created, "%Y%m%dT%H%M%SZ")

        return None

    def get_last_modified_date(item_name):
        tasks = warrior.load_tasks()
        last_modified = None
        for task in tasks["pending"]:
            project = task.get("project")
            if project and (
                project == item_name or project.startswith("AoR." + item_name)
            ):
                modified = task.get("modified")
                if modified:
                    modified_date = datetime.strptime(modified, "%Y%m%dT%H%M%SZ")
                    if last_modified is None or modified_date > last_modified:
                        last_modified = modified_date

        return last_modified

    def get_tags_for_item(item_name):
        tasks = warrior.load_tasks()
        tags = {}
        for task in tasks["pending"]:
            project = task.get("project")
            if project and (
                project == item_name or project.startswith("AoR." + item_name)
            ):
                for tag in task.get("tags", []):
                    if not tag.startswith("project:") and tag != item_name:
                        tags[tag] = tags.get(tag, 0) + 1
        return tags

    def view_data(item, tags):
        print(f"{Fore.BLUE}Name: {Fore.YELLOW}{item['name']}{Fore.RESET}")
        print(
            f"{Fore.BLUE}Description: {Fore.YELLOW}{item.get('description', '')}{Fore.RESET}"
        )

        # Get the number of pending tasks
        pending_tasks = 0
        for tag, count in tags.items():
            if tag != "Completed":
                pending_tasks += count

        # Get the number of completed tasks
        completed_tasks = tags.get("Completed", 0)

        print(
            f"{Fore.BLUE}Pending: {Fore.YELLOW}{pending_tasks}{Fore.RESET} | "
            f"{Fore.BLUE}Completed: {Fore.YELLOW}{completed_tasks}{Fore.RESET}"
        )

        if "standard" in item:
            field_name = "Standard" if "outcome" not in item else "Outcome"
            field_value = (
                item.get("standard") if "outcome" not in item else item.get("outcome")
            )
            print(f"{Fore.BLUE}{field_name}: {Fore.YELLOW}{field_value}{Fore.RESET}")
            if field_name == "Outcome":
                print("Defining what 'DONE' means.")

        creation_date = get_creation_date(item["name"])
        if creation_date:
            current_datetime = datetime.now()
            creation_time_difference = current_datetime - creation_date
            creation_days_remaining = creation_time_difference.days
            creation_time_remaining = creation_time_difference.seconds
            creation_time_prefix = "-" if creation_days_remaining > 0 else "+"
            creation_time_remaining_formatted = str(
                timedelta(seconds=abs(creation_time_remaining))
            )
            creation_time_difference_formatted = f"({creation_time_prefix}{abs(creation_days_remaining)} days, {creation_time_remaining_formatted})"
            print(
                f"{Fore.BLUE}Creation Date: {Fore.YELLOW}{creation_date} {creation_time_difference_formatted}{Fore.RESET}"
            )

        last_modified_date = get_last_modified_date(item["name"])
        if last_modified_date:
            current_datetime = datetime.now()
            last_modified_time_difference = current_datetime - last_modified_date
            last_modified_days_remaining = last_modified_time_difference.days
            last_modified_time_remaining = last_modified_time_difference.seconds
            last_modified_time_prefix = "-" if last_modified_days_remaining > 0 else "+"
            last_modified_time_remaining_formatted = str(
                timedelta(seconds=abs(last_modified_time_remaining))
            )
            last_modified_time_difference_formatted = f"({last_modified_time_prefix}{abs(last_modified_days_remaining)} days, {last_modified_time_remaining_formatted})"
            print(
                f"{Fore.BLUE}Last Modified Date: {Fore.YELLOW}{last_modified_date} {last_modified_time_difference_formatted}{Fore.RESET}"
            )

        if "outcome" in item:
            print(f"{Fore.BLUE}Outcome: {Fore.YELLOW}{item['outcome']}{Fore.RESET}")

        print(f"{Fore.BLUE}Tags:{Fore.RESET}")
        no_tag_tasks = []  # List to store tasks without tags
        for tag, count in tags.items():
            if tag != "Completed":
                print(
                    f" - {Fore.BLACK}{Back.YELLOW}{tag}{Fore.RESET}{Back.RESET} ({count} task{'s' if count > 1 else ''})"
                )
                # Load tasks

                tasks = warrior.load_tasks()["pending"]
                # Print tasks with the current tag and same project/AoR
                for task in tasks:
                    task_tags = task.get("tags", [])
                    task_project = task.get("project", "")
                    if tag in task_tags and (
                        task_project == item["name"]
                        or task_project.startswith("AoR." + item["name"])
                    ):
                        task_id = task["id"]
                        task_description = task.get("description", "")
                        time_remaining = ""
                        if "due" in task:
                            due_date = datetime.strptime(task["due"], "%Y%m%dT%H%M%SZ")
                            time_remaining = due_date - datetime.now()
                            time_remaining = str(time_remaining).split(".")[0]
                        print(
                            f"\t{Fore.YELLOW}{task_id}{Fore.RESET}, {Fore.CYAN}{task_description}{Fore.RESET} {time_remaining}"
                        )
                    elif not task_tags and (
                        task_project == item["name"]
                        or task_project.startswith("AoR." + item["name"])
                    ):
                        if (
                            task not in no_tag_tasks
                        ):  # Add tasks without tags to the list only if not already included
                            no_tag_tasks.append(task)

        if no_tag_tasks:
            print(
                f" - \033[1;31m No Tag Tasks:\033[0m ({len(no_tag_tasks)} task{'s' if len(no_tag_tasks) > 1 else ''})"
            )
            for task in no_tag_tasks:
                task_id = task["id"]
                task_description = task.get("description", "")
                time_remaining = ""
                if "due" in task:
                    due_date = datetime.strptime(task["due"], "%Y%m%dT%H%M%SZ")
                    time_remaining = due_date - datetime.now()
                    time_remaining = str(time_remaining).split(".")[0]
                print(
                    f"\t{Fore.RED}{task_id}{Fore.RESET}, {Fore.CYAN}{task_description}{Fore.RESET} {time_remaining}"
                )
        else:
            print("No tags found.")

        if "annotations" in item:
            print(f"\n{Fore.BLUE}Annotations:{Fore.RESET}")
            for annotation in item["annotations"]:
                timestamp = annotation.get("timestamp")
                content = annotation.get("content", "")
                print(
                    f" - {Fore.YELLOW}{timestamp}{Fore.RESET}: {Fore.YELLOW}{content}{Fore.RESET}"
                )

        if "workLogs" in item:
            print(f"{Fore.BLUE}Work Logs:{Fore.RESET}")
            for work_log in item["workLogs"]:
                timestamp = work_log.get("timestamp")
                content = work_log.get("content", "")
                print(
                    f" - {Fore.YELLOW}{timestamp}{Fore.RESET}: {Fore.YELLOW}{content}{Fore.RESET}"
                )

    def execute_taskwarrior_command(command):
        """Execute a TaskWarrior command and return its output."""
        try:
            # Start the process
            proc = subprocess.Popen(
                command,
                shell=True,
                text=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            while True:
                # Read from stdout and stderr
                stdout_line = proc.stdout.readline()
                stderr_line = proc.stderr.readline()

                # Display stdout and stderr to the user
                if stdout_line:
                    sys.stdout.write(stdout_line)
                    sys.stdout.flush()
                if stderr_line:
                    sys.stderr.write(stderr_line)
                    sys.stderr.flush()

                # Check if there's a prompt in stderr for user input
                if stderr_line and "prompt" in stderr_line.lower():
                    user_input = input("Please provide input: ")
                    proc.stdin.write(user_input + "\n")
                    proc.stdin.flush()

                # Check if process is still running
                if proc.poll() is not None:
                    break

            # Get the final output
            stdout, stderr = proc.communicate()

            if stdout:
                return stdout.strip()  # Remove extra whitespace
            if stderr:
                print(f"Error: {stderr.strip()}")

        except Exception as e:
            print(f"An error occurred while executing the TaskWarrior command: {e}")

        return ""

    # def get_task_count(item_name, status):
    # 	"""Get the count of tasks by status for a specific project."""
    # 	command = f"task count project:{item_name} status:{status}"
    # 	return execute_taskwarrior_command(command)

    def view_project_metadata(item, tags, item_name):
        console = Console()
        # Display creation date
        creation_date = get_creation_date(item["name"])
        if creation_date:
            current_datetime = datetime.now()
            creation_time_difference = current_datetime - creation_date
            creation_days_remaining = creation_time_difference.days
            creation_time_remaining = creation_time_difference.seconds
            creation_time_prefix = "-" if creation_days_remaining > 0 else "+"
            creation_time_remaining_formatted = str(
                timedelta(seconds=abs(creation_time_remaining))
            )
            creation_time_difference_formatted = f"({creation_time_prefix}{abs(creation_days_remaining)} days, {creation_time_remaining_formatted})"
            console.print(
                Panel(
                    f"[blue]Creation Date: [yellow]{creation_date.strftime('%Y-%m-%d %H:%M')} {creation_time_difference_formatted}[/yellow]",
                    title="Creation Date",
                    expand=False,
                )
            )

        # Display last modified date
        last_modified_date = get_last_modified_date(item["name"])
        if last_modified_date:
            current_datetime = datetime.now()
            last_modified_time_difference = current_datetime - last_modified_date
            last_modified_days_remaining = last_modified_time_difference.days
            last_modified_time_remaining = last_modified_time_difference.seconds
            last_modified_time_prefix = "-" if last_modified_days_remaining > 0 else "+"
            last_modified_time_remaining_formatted = str(
                timedelta(seconds=abs(last_modified_time_remaining))
            )
            last_modified_time_difference_formatted = f"({last_modified_time_prefix}{abs(last_modified_days_remaining)} days, {last_modified_time_remaining_formatted})"
            console.print(
                Panel(
                    f"[blue]Last Modified Date: [yellow]{last_modified_date.strftime('%Y-%m-%d %H:%M')} {last_modified_time_difference_formatted}[/yellow]",
                    title="Last Modified Date",
                    expand=False,
                )
            )

        # Display item name and description
        console.print(
            Panel(
                f"[blue]Name: [yellow]{item['name']}[/yellow]",
                title="Item Name",
                expand=False,
            )
        )
        console.print(
            Panel(
                f"[blue]Description:\n [cornflower_blue]{item.get('description', '')}[/cornflower_blue]",
                title="Description",
                expand=False,
            )
        )

        # # Display task counts
        # pending_tasks = get_task_count(item_name, 'pending')
        # completed_tasks = get_task_count(item_name, 'completed')
        # deleted_tasks = get_task_count(item_name, 'deleted')

        # task_counts = Text.assemble(
        # 	("Pending: ", "yellow"), (f"{pending_tasks}", "yellow"), (" | Completed: ", "yellow"), (f"{completed_tasks}", "green"), (" | Deleted: ", "yellow"), (f"{deleted_tasks}", "blue")
        # )
        # console.print(Panel(task_counts, title="Task Counts", expand=False))

        # console.print("\n")

        # Display standard or outcome
        if "standard" in item or "outcome" in item:
            field_name = "Standard" if "outcome" not in item else "Outcome"
            field_value = (
                item.get("standard") if "outcome" not in item else item.get("outcome")
            )
            console.print(
                Panel(
                    f"[blue]{field_name}: [yellow]{field_value}[/yellow]",
                    title=field_name,
                    expand=False,
                )
            )

        # # Display outcome
        # if 'outcome' in item:
        # 	console.print(Panel(f"[blue]Outcome: [yellow]{item['outcome']}[/yellow]", title="Outcome", expand=False))

        # Display annotations
        if "annotations" in item:
            table = Table(title="Annotations", box=box.SIMPLE)
            table.add_column("Timestamp", style="dim", width=20)
            table.add_column("Content", style="yellow")

            for i, annotation in enumerate(item["annotations"]):
                timestamp_str = annotation.get("timestamp")
                content = annotation.get("content", "")

                # Remove milliseconds if present
                if "." in timestamp_str:
                    timestamp_str = timestamp_str.split(".")[0]

                row_style = "gold1" if i % 2 == 0 else "cornflower_blue"
                table.add_row(timestamp_str, content, style=row_style)

            console.print(table)

        # Display work logs
        if "workLogs" in item:
            table = Table(title="Work Logs", box=box.SIMPLE)
            table.add_column("Timestamp", style="dim", width=20)
            table.add_column("Content", style="yellow")

            for i, work_log in enumerate(item["workLogs"]):
                timestamp_str = work_log.get("timestamp")
                content = work_log.get("content", "")

                # Remove milliseconds if present
                if "." in timestamp_str:
                    timestamp_str = timestamp_str.split(".")[0]

                row_style = "deep_pink1" if i % 2 == 0 else "cornflower_blue"
                table.add_row(timestamp_str, content, style=row_style)

            console.print(table)

    from prompt_toolkit import PromptSession
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.application import get_app
    from prompt_toolkit.filters import Condition
    from prompt_toolkit.shortcuts import prompt
    # from prompt_toolkit.shortcuts.prompt import CompleteStyle
    from prompt_toolkit.formatted_text import HTML
    from prompt_toolkit.styles import Style
    import inquirer

    def get_multiline_input(prompt_message):
        session = PromptSession()
        bindings = KeyBindings()

        @bindings.add("c-c")
        def _(event):
            event.app.exit()

        @bindings.add("c-s")
        def _(event):
            event.app.exit(result=event.app.current_buffer.text)

        return session.prompt(
            HTML(f"<skyblue>{prompt_message}</skyblue>\n> "),
            multiline=True,
            key_bindings=bindings,
            complete_while_typing=False,
            style=Style.from_dict({"prompt": "bg:#008800 #ffffff"}),
        )

    def update_item(items, item_index, file_path, specific_field, aors, projects):
        commands = [
            "Add description",
            "Add annotation",
            "Add work log entry",
            f"Add {specific_field}",
            "Go back",
        ]
        print("Use CTRL+C to exit or CTRL+S to exit and save from edit screen.")
        while True:
            questions = [
                inquirer.List(
                    "command",
                    message="Please select a command",
                    choices=commands,
                ),
            ]
            answers = inquirer.prompt(questions)

            if answers["command"] == "Add description":
                text = get_multiline_input("Enter Description: ")
                items[item_index]["description"] = text
                print(f"Added Description: {text}")
                save_sultandb(file_path, aors, projects)

            elif answers["command"] == "Add annotation":
                text = get_multiline_input("Enter Annotation: ")
                timestamp = datetime.now()
                entry = {"content": text, "timestamp": timestamp}
                if "annotations" not in items[item_index]:
                    items[item_index]["annotations"] = []
                items[item_index]["annotations"].append(entry)
                print(f"Added Annotation: {text} at {timestamp}")
                save_sultandb(file_path, aors, projects)

            elif answers["command"] == "Add work log entry":
                text = get_multiline_input("Enter Work Log Entry: ")
                timestamp = datetime.now()
                entry = {"content": text, "timestamp": timestamp}
                if "workLogs" not in items[item_index]:
                    items[item_index]["workLogs"] = []
                items[item_index]["workLogs"].append(entry)
                print(f"Added Work Log Entry: {text} at {timestamp}")
                save_sultandb(file_path, aors, projects)

            elif answers["command"] == f"Add {specific_field}":
                text = get_multiline_input(f"Enter {specific_field.capitalize()}: ")
                items[item_index][specific_field] = text
                print(f"Added {specific_field.capitalize()}: {text}")
                save_sultandb(file_path, aors, projects)

            elif answers["command"] == "Go back":
                break

    def call_and_process_task_projects():
        # Call 'task projects' and capture its output
        result = subprocess.run(["task", "projects"], capture_output=True, text=True)
        lines = result.stdout.splitlines()

        # Process the output from 'task projects'
        project_list = process_input(
            lines
        )  # project_list is now a list of all processed projects

        # Use the processed output as input to search_project()
        search_project(project_list)

    def process_input(lines):
        level_text = {0: ""}
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
                raise ValueError("Invalid indentation level in input")

            level //= spaces_per_level

            if level > last_level + 1:
                raise ValueError("Indentation level increased by more than 1")

            level_text[level] = text

            # Clear all deeper levels
            level_text = {k: v for k, v in level_text.items() if k <= level}

            output_line = ".".join(level_text[l] for l in range(level + 1))

            output_lines.append(output_line)  # Add each processed project to the list

            last_level = level
        print(output_lines)
        return output_lines  # Return the list of all processed projects

    def dependency_tree(selected_item):
        # from rich import print
        from rich.tree import Tree
        from rich.text import Text

        from datetime import datetime
        import pytz
        from dateutil.parser import parse

        tasks = warrior.load_tasks()
        selected_project = selected_item

        task_dict = {}
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)
        all_tasks = {task["uuid"]: task for task in tasks["pending"]}
        uuid_to_real_id = {task["uuid"]: task["id"] for task in tasks["pending"]}

        def is_relevant(task):
            project = task.get("project")
            return project and (
                project == selected_project
                or project.startswith(selected_project + ".")
            )

        def collect_tasks(task_uuid, visited=set()):
            if task_uuid in visited or task_uuid not in all_tasks:
                return
            visited.add(task_uuid)
            task = all_tasks[task_uuid]
            dependencies = task.get("depends", [])

            task_dict[task_uuid] = {
                "project": task.get("project"),
                "description": task.get("description", ""),
                "due_date": task.get("due"),
                "time_remaining": calculate_time_remaining(task.get("due"), now),
                "annotations": task.get("annotations", []),
                "tags": task.get("tags", []),
                "dependencies": dependencies,
            }

            for dep_uuid in dependencies:
                collect_tasks(dep_uuid, visited)

        for task_uuid, task in all_tasks.items():
            if is_relevant(task):
                collect_tasks(task_uuid)

        tree = Tree(f"Dependency Tree: {selected_project}", style="green")
        # local_tz = datetime.now().astimezone().tzinfo

        def add_task_to_tree(task_uuid, parent_branch):
            if task_uuid not in task_dict:
                return
            task = task_dict[task_uuid]
            real_id = uuid_to_real_id[task_uuid]
            task_description = task["description"]
            task_id_text = Text(f"[{real_id}] ", style="red")
            task_description_text = Text(task_description, style="white")
            task_id_text.append(task_description_text)

            due_date = task.get("due_date")
            if due_date:
                formatted_due_date = parse(due_date).strftime("%Y-%m-%d")
                time_remaining, time_style = calculate_time_remaining(due_date, now)
                due_text = Text(f" {formatted_due_date} ", style="blue")
                time_remaining_text = Text(time_remaining, style=time_style)
                due_text.append(time_remaining_text)
                task_id_text.append(due_text)

            # Display tags in red bold
            if task.get("tags"):
                tags_text = Text(f" +{', '.join(task['tags'])} ", style="bold red")
                task_id_text.append(tags_text)

            # Display project in blue bold if different from the selected or if no project is assigned
            if task.get("project") != selected_project:
                project_text = Text(
                    f" {task.get('project', 'No Project')} ", style="magenta"
                )
                task_id_text.append(project_text)

            task_branch = parent_branch.add(task_id_text)

            annotations = task.get("annotations", [])
            if annotations:
                annotation_branch = task_branch.add(Text("Annotations:", style="white"))
                for annotation in annotations:
                    entry_datetime = parse(annotation["entry"])
                    if (
                        entry_datetime.tzinfo is None
                        or entry_datetime.tzinfo.utcoffset(entry_datetime) is None
                    ):
                        entry_datetime = entry_datetime.replace(tzinfo=local_tz)
                    else:
                        entry_datetime = entry_datetime.astimezone(local_tz)
                    annotation_text = Text(
                        f"{entry_datetime.strftime('%Y-%m-%d %H:%M:%S')} - {annotation['description']}",
                        style="dim white",
                    )
                    annotation_branch.add(annotation_text)

            for dep_uuid in task["dependencies"]:
                add_task_to_tree(dep_uuid, task_branch)

        for task_uuid in task_dict:
            if not any(
                task_uuid in task_dict[dep_uuid]["dependencies"]
                for dep_uuid in task_dict
            ):
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
                formatted_time = (
                    f"{days}d {hours}h {minutes}m" if days else f"{hours}h {minutes}m"
                )
            else:
                formatted_time = "0m"  # Show 0 minutes if time remaining is very short

            return formatted_time, time_style
        return None  # Return None when no due date

    def search_project(project_list):
        completer = FuzzyWordCompleter(project_list)

        # Define the style for the completer
        style = Style.from_dict(
            {
                "completion-menu.completion": "bg:black black green",
            }
        )

        # Prompt the user for a project or AoR name with custom styles
        item_name = prompt(
            "Enter a project or AoR name: ", completer=completer, style=style
        )

        # Run the dependency_tree with the selected project
        console = Console()
        if item_name == "mp":
            print("Right, lets get to work and getting things done!")
            multiple_projects_view()
        else:
            display_tasks(f"task project:{item_name} +PENDING export")

        while True:
            console.print("\n" + "-:" * 40)

            # Create a table for menu options
            table = Table(
                box=box.ROUNDED, expand=False, show_header=False, border_style="cyan"
            )
            table.add_column("Option", style="orange_red1", no_wrap=True)
            table.add_column("Description", style="light_sea_green")

            # Project Management options
            table.add_row("", "[bold underline]Project Management:[/bold underline]")
            table.add_row("R", "Refresh")
            table.add_row("DT", "Display dependency tree")
            table.add_row("SD", "Set dependencies")
            table.add_row("RD", "Remove dependencies")
            table.add_row("DE", "Show Details")
            table.add_row("SP", "Search another project")
            table.add_row("MP", "Display multiple projects")
            table.add_row("MA", "Main menu")
            table.add_row("", "")  # Separator

            # Update Metadata options
            table.add_row("", "[bold underline]Update Metadata:[/bold underline]")
            table.add_row("UD", "Update Description")
            table.add_row("UO", "Update Standard/Outcome")
            table.add_row("AA", "Add Annotation")
            table.add_row("AW", "Add Work Log")
            table.add_row("SYDB", "Sync sultanDB to TW DB")
            table.add_row("", "")  # Separator

            # Task Management options
            table.add_row("", "[bold underline]Task Management:[/bold underline]")
            table.add_row("TW", "TW prompt")
            table.add_row("TM", "Task Manager")
            table.add_row("NT", "Add new task")
            table.add_row("AN", "Annotate task")
            table.add_row("TD", "Mark task as completed")
            table.add_row("DD", "Assign due date")
            table.add_row("", "")  # Separator

            # Exit option
            table.add_row("", "[bold underline]Exit:[/bold underline]")
            table.add_row("", "|_>")

            console.print(
                Panel(table, title="Project Management Options", expand=False)
            )

            choice = console.input("[yellow]Enter your choice: ").upper()

            if choice == "R":
                console.clear()
                display_tasks(f"task project:{item_name} +PENDING export")
            elif choice == "DT":
                dependency_tree(item_name)
            elif choice == "SD":
                dependency_input = ""
                manual_sort_dependencies(dependency_input)
                dependency_tree(item_name)
            elif choice == "DE":
                display_tasks(
                    f"task project:{item_name} +PENDING export", show_details=True
                )
            elif choice == "RD":
                task_ids_input = console.input(
                    "Enter the IDs of the tasks to remove dependencies (comma-separated):\n"
                )
                remove_task_dependencies(task_ids_input)
                dependency_tree(item_name)
            elif choice == "SP":
                call_and_process_task_projects()
            elif choice == "MP":
                multiple_projects_view()
            elif choice == "MA":
                main_menu()
            elif choice == "UD":
                update_metadata_field(item_name, "description")
            elif choice == "UO":
                update_metadata_field(item_name, "standard_or_outcome")
            elif choice == "AA":
                update_metadata_field(item_name, "annotations")
            elif choice == "AW":
                update_metadata_field(item_name, "workLogs")
            elif choice == "SYDB":
                sync_sultandb_with_taskwarrior(file_path)
                display_tasks(f"task project:{item_name} +PENDING export")
            elif choice == "TW":
                handle_task()
                display_tasks(f"task project:{item_name} +PENDING export")
            elif choice == "TM":
                task_ID = console.input("[cyan]Please enter the task ID: ")
                if task_ID:
                    console.clear()
                    task_manager(task_ID)
            elif choice == "NT":
                add_task_to_project(item_name)
                display_tasks(f"task project:{item_name} +PENDING export")
            elif choice == "AN":
                task_id = console.input("Enter the task ID to annotate: ")
                annotation = console.input("Enter the annotation: ")
                command = f"task {task_id} annotate {annotation}"
                execute_task_command(command)
                annotate_task(task_id, annotation)
            elif choice == "TD":
                task_id = console.input("Enter the task ID to mark as completed: ")
                command = f"task {task_id} done"
                execute_task_command(command)
            elif choice == "DD":
                task_id = console.input("Enter the task ID to assign a due date: ")
                due_date = console.input("Enter the due date (YYYY-MM-DD): ")
                command = f"task {task_id} modify due:{due_date}"
                execute_task_command(command)
            elif choice == "":
                console.print("Exiting project management.")
                break
            else:
                console.print(
                    Panel("Invalid choice. Please try again.", style="bold red")
                )

    # x_x

    def load_project_metadata(file_path):
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        # Combine 'aors' and 'projects'
        aors = data.get("aors", [])
        projects = data.get("projects", [])

        # Add 'AoR.' prefix to AoR names
        for aor in aors:
            aor["name"] = "AoR." + aor["name"]

        items = aors + projects
        # Create a dictionary mapping project names to metadata
        project_metadata = {item["name"]: item for item in items}
        return project_metadata

    # x_x

    def multiple_projects_view():
        # Define your list of projects
        project_list = ["CN", "Biz", "ukNI"]

        # Define the list of tags to exclude
        excluded_tags = ["bean", "maybe", "docs", "domains", "grooming"]

        # Call the function to display tasks from these projects, excluding specified tags
        display_multiple_projects(project_list, excluded_tags)

    def display_multiple_projects(project_list, excluded_tags=None):
        if excluded_tags is None:
            excluded_tags = []
        console = Console()
        all_tasks = []

        # Load project metadata
        script_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_directory, "sultandb.json")
        project_metadata = load_project_metadata(file_path)

        # Fetch tasks for each project
        for project in project_list:
            # Build the command for each project, including excluded tags
            command = ["task", f'project:"{project}"', "+PENDING"]

            # Add excluded tags to the command
            for tag in excluded_tags:
                command.append(f"-{tag}")  # Use -{tag} as per your practice

            command.append("export")

            # Debug: Print the command being executed
            # print(f"Executing command: {' '.join(command)}")

            result = subprocess.run(command, capture_output=True, text=True)
            if result.stdout:
                try:
                    tasks = json.loads(result.stdout)
                    if not tasks:
                        console.print(
                            f"No tasks found for project {project}.",
                            style="bold yellow",
                        )
                    else:
                        all_tasks.extend(tasks)
                except json.JSONDecodeError as e:
                    console.print(
                        f"Error decoding JSON for project {project}: {e}",
                        style="bold red",
                    )
            else:
                console.print(
                    f"No tasks found for project {project}.", style="bold yellow"
                )

        if not all_tasks:
            console.print("No tasks found for the provided projects.", style="bold red")
            return

        # Now process the combined list of tasks
        project_tag_map = defaultdict(lambda: defaultdict(list))
        now = datetime.now(timezone.utc).astimezone()

        for task in all_tasks:
            project = task.get("project", "No Project")
            tags = task.get("tags", ["No Tag"])

            description = task["description"]
            task_id = str(task["id"])

            due_date_str = task.get("due")
            due_date = parse_datetime(due_date_str) if due_date_str else None

            annotations = task.get("annotations", [])
            duration = task.get("duration", "")
            original_priority = task.get("priority")
            value = task.get("value")

            # Convert value to float if possible
            try:
                value = float(value) if value is not None else None
            except ValueError:
                value = None

            # Determine the priority level
            if original_priority:
                priority_level = original_priority.upper()
            elif value is not None:
                if value >= 2500:
                    priority_level = "H"
                elif value >= 700:
                    priority_level = "M"
                else:
                    priority_level = "L"
            else:
                priority_level = None

            # Assign colors based on priority level
            if priority_level == "H":
                priority_color = "bold red"
            elif priority_level == "M":
                priority_color = "bold yellow"
            elif priority_level == "L":
                priority_color = "bold green"
            else:
                priority_color = "bold magenta"

            # Initialize color to a default value
            color = "default_color"
            delta_text = ""
            if due_date:
                delta = due_date - now
                if delta.total_seconds() < 0:
                    color = "red"
                elif delta.days >= 365:
                    color = "steel_blue"
                elif delta.days >= 90:
                    color = "light_slate_blue"
                elif delta.days >= 30:
                    color = "green_yellow"
                elif delta.days >= 7:
                    color = "thistle3"
                elif delta.days >= 3:
                    color = "yellow1"
                elif delta.days == 0:
                    color = "bold turquoise2"
                else:
                    color = "bold orange1"
                delta_text = format_timedelta(delta)

            for tag in tags:
                project_tag_map[project][tag].append(
                    (
                        task_id,
                        description,
                        due_date,
                        annotations,
                        delta_text,
                        color,
                        duration,
                        priority_level,
                        priority_color,
                        value,
                    )
                )

        # Define lists of colors for levels and guide styles
        # level_colors = ['bright_red', 'bright_green', 'bright_yellow', 'bright_blue',
        # 				'bright_magenta', 'bright_cyan', 'bright_white']
        # guide_styles = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

        # Build the tree with different colors and guide styles for each level
        tree = Tree("Task Overview", style="green", guide_style="green")
        for project, tags in project_tag_map.items():
            if project == "No Project" and not any(tags.values()):
                continue
            project_levels = project.split(".")
            current_branch = tree
            for i, level in enumerate(project_levels):
                # Adding or finding the branch for each project level
                found_branch = None
                for child in current_branch.children:
                    if child.label.plain == level:
                        found_branch = child
                        break
                if not found_branch:
                    color = level_colors[
                        i % len(level_colors)
                    ]  # Assign color based on level depth
                    guide_style = guide_styles[
                        i % len(guide_styles)
                    ]  # Assign guide style based on level depth
                    found_branch = current_branch.add(
                        Text(level, style=color), guide_style=guide_style
                    )
                current_branch = found_branch

            # Get the metadata for the project or its parent
            metadata = None
            project_hierarchy = project.split(".")
            for j in range(len(project_hierarchy), 0, -1):
                partial_project = ".".join(project_hierarchy[:j])
                metadata = project_metadata.get(partial_project)
                if metadata and any(metadata.values()):
                    break
                else:
                    metadata = None

            if metadata:
                add_project_metadata_to_tree(metadata, current_branch)

            for tag, tasks in tags.items():
                if not tasks:
                    continue
                tag_branch = current_branch.add(
                    Text(tag, style="blue"), guide_style="blue"
                )
                for task_info in sorted(tasks, key=lambda x: (x[2] is None, x[2])):
                    (
                        task_id,
                        description,
                        due_date,
                        annotations,
                        delta_text,
                        delta_color,
                        duration,
                        priority_level,
                        priority_color,
                        value,
                    ) = task_info
                    # Build task line as before
                    # Square brackets in red
                    left_bracket = Text("[", style="red")
                    right_bracket = Text("] ", style="red")
                    # Task ID in turquoise
                    task_id_text = Text(task_id, style="turquoise2")
                    # Priority in color based on priority level
                    if priority_level:
                        priority_text = Text(
                            f"[{priority_level}] ", style=priority_color
                        )
                    else:
                        priority_text = Text("")
                    # Value in bold cyan
                    if value is not None:
                        value_text = Text(f"[{value}] ", style="bold cyan")
                    else:
                        value_text = Text("")
                    # Duration in cyan
                    duration_text = Text(
                        f"({duration}) " if duration else "", style="cyan"
                    )
                    # Description in white
                    description_text = Text(description + " ", style="white")
                    # Due date in the color determined earlier
                    if due_date:
                        due_date_text = Text(
                            due_date.strftime("%Y-%m-%d"), style=delta_color
                        )
                    else:
                        due_date_text = Text("")
                    # Delta text in the same color
                    delta_text_output = Text(
                        f" ({delta_text})" if delta_text else "", style=delta_color
                    )
                    # Combine texts for one line
                    task_line = (
                        left_bracket
                        + task_id_text
                        + right_bracket
                        + priority_text
                        + value_text
                        + duration_text
                        + description_text
                        + due_date_text
                        + delta_text_output
                    )
                    task_branch = tag_branch.add(task_line, guide_style="dim")
                    if annotations:
                        annotation_branch = task_branch.add(
                            Text("Annotations:", style="italic white"),
                            guide_style="dim",
                        )
                        for annotation in annotations:
                            entry_datetime = datetime.strptime(
                                annotation["entry"], "%Y%m%dT%H%M%SZ"
                            ).strftime("%Y-%m-%d %H:%M:%S")
                            annotation_text = Text(
                                f"{entry_datetime} - {annotation['description']}",
                                style="dim white",
                            )
                            annotation_branch.add(annotation_text, guide_style="dim")

        console.print(tree)

    def add_project_metadata_to_tree_2(metadata, branch):
        """Add project metadata as styled sub-branches to the given branch"""
        # Check if there's any metadata to display
        has_metadata = any(
            [
                metadata.get("description"),
                metadata.get("standard"),
                metadata.get("outcome"),
                metadata.get("annotations"),
                metadata.get("workLogs"),
            ]
        )

        if not has_metadata:
            return
        metadata_branch = branch.add(
            Text("📋 Metadata", style="bold cyan"), guide_style="cyan"
        )

        # Description field
        if metadata.get("description"):
            metadata_branch.add(
                Text.from_markup(
                    f"[bold steel_blue]Description:[/bold steel_blue] [white]{metadata['description']}[/white]"
                ),
                guide_style="steel_blue",
            )

        # Standard (for AoRs) or Outcome (for Projects)
        if metadata.get("standard"):
            metadata_branch.add(
                Text.from_markup(
                    f"[bold cornflower_blue]Standard:[/bold cornflower_blue] [white]{metadata['standard']}[/white]"
                ),
                guide_style="cornflower_blue",
            )
        elif metadata.get("outcome"):
            metadata_branch.add(
                Text.from_markup(
                    f"[bold green_yellow]Outcome:[/bold green_yellow] [white]{metadata['outcome']}[/white]"
                ),
                guide_style="green_yellow",
            )

        # Annotations
        if metadata.get("annotations"):
            annotations_branch = metadata_branch.add(
                Text("📝 Annotations", style="bold orchid"), guide_style="orchid"
            )
            for annotation in metadata["annotations"]:
                timestamp = datetime.fromisoformat(annotation["timestamp"]).strftime(
                    "%Y-%m-%d %H:%M"
                )
                annotations_branch.add(
                    Text.from_markup(
                        f"[yellow]{timestamp}[/yellow] [white]{annotation['content']}[/white]"
                    ),
                    guide_style="dim orchid",
                )

        # Work Logs
        if metadata.get("workLogs"):
            worklogs_branch = metadata_branch.add(
                Text("📊 Work Logs", style="bold gold1"), guide_style="gold1"
            )
            for log in metadata["workLogs"]:
                timestamp = datetime.fromisoformat(log["timestamp"]).strftime(
                    "%Y-%m-%d %H:%M"
                )
                worklogs_branch.add(
                    Text.from_markup(
                        f"[grey70]{timestamp}[/grey70] [white]{log['content']}[/white]"
                    ),
                    guide_style="dim gold1",
                )

    def add_project_metadata_to_tree(metadata, parent_branch):
        # Determine if the project is an AoR project
        project_name = metadata.get("name", "")
        is_aor = project_name.startswith("AoR.")

        content_present = False  # Flag to check if any metadata content is present
        metadata_branch = None  # Initialize metadata_branch as None

        # Description
        description = metadata.get("description", "")
        if description:
            if not metadata_branch:
                metadata_branch = parent_branch.add(
                    Text("Metadata", style="bold light_steel_blue1"), guide_style="dim"
                )
            label_text = Text("Description: ", style="bold cyan")
            value_text = Text(description, style="white")
            metadata_branch.add(label_text + value_text, guide_style="dim")
            content_present = True

        # Display 'Standard' for AoR projects, 'Outcome' for normal projects
        if is_aor:
            standard = metadata.get("standard", "")
            if standard:
                if not metadata_branch:
                    metadata_branch = parent_branch.add(
                        Text("Metadata", style="bold light_steel_blue1"),
                        guide_style="dim",
                    )
                label_text = Text("Standard: ", style="bold cyan")
                value_text = Text(standard, style="white")
                metadata_branch.add(label_text + value_text, guide_style="dim")
                content_present = True
        else:
            outcome = metadata.get("outcome", "")
            if outcome:
                if not metadata_branch:
                    metadata_branch = parent_branch.add(
                        Text("Metadata", style="bold light_steel_blue1"),
                        guide_style="dim",
                    )
                label_text = Text("Outcome: ", style="bold cyan")
                value_text = Text(outcome, style="white")
                metadata_branch.add(label_text + value_text, guide_style="dim")
                content_present = True

        # Annotations
        annotations = metadata.get("annotations", [])
        if annotations:
            if not metadata_branch:
                metadata_branch = parent_branch.add(
                    Text("Metadata", style="bold light_steel_blue1"), guide_style="dim"
                )
            annotations_branch = metadata_branch.add(
                Text("Annotations", style="bold yellow"), guide_style="dim"
            )
            for annotation in annotations:
                timestamp_str = annotation.get("timestamp", "")
                content = annotation.get("content", "")
                label_text = Text(f"{timestamp_str} - ", style="dim green")
                value_text = Text(content, style="white")
                annotations_branch.add(label_text + value_text, guide_style="dim")
            content_present = True

        # Work Logs
        work_logs = metadata.get("workLogs", [])
        if work_logs:
            if not metadata_branch:
                metadata_branch = parent_branch.add(
                    Text("Metadata", style="bold light_steel_blue1"), guide_style="dim"
                )
            work_logs_branch = metadata_branch.add(
                Text("Work Logs", style="bold yellow"), guide_style="dim"
            )
            for work_log in work_logs:
                timestamp_str = work_log.get("timestamp", "")
                content = work_log.get("content", "")
                label_text = Text(f"{timestamp_str} - ", style="dim green")
                value_text = Text(content, style="white")
                work_logs_branch.add(label_text + value_text, guide_style="dim")
            content_present = True

        # # Creation Date
        # creation_date_str = metadata.get('creation_date', '')
        # if creation_date_str:
        # 	if not metadata_branch:
        # 		metadata_branch = parent_branch.add(Text("Metadata", style="bold light_steel_blue1"), guide_style="dim")
        # 	label_text = Text("Creation Date: ", style="bold cyan")
        # 	value_text = Text(creation_date_str, style="white")
        # 	metadata_branch.add(label_text + value_text, guide_style="dim")
        # 	content_present = True

        # # Last Modified Date
        # last_modified_date_str = metadata.get('last_modified_date', '')
        # if last_modified_date_str:
        # 	if not metadata_branch:
        # 		metadata_branch = parent_branch.add(Text("Metadata", style="bold light_steel_blue1"), guide_style="dim")
        # 	label_text = Text("Last Modified Date: ", style="bold cyan")
        # 	value_text = Text(last_modified_date_str, style="white")
        # 	metadata_branch.add(label_text + value_text, guide_style="dim")
        # 	content_present = True

        # If no content was added, remove the Metadata branch if it exists
        if not content_present and metadata_branch:
            parent_branch.children.remove(metadata_branch)

    # x_x

    def add_task_to_project(project_name):
        task_descriptions = questionary.text(
            "Enter the descriptions for the new tasks (one per line):", multiline=True
        ).ask()
        task_descriptions_list = task_descriptions.split("\n")

        tasks = []

        for task_description in task_descriptions_list:
            if not task_description.strip():
                continue

            create_command = f"task add proj:{project_name} {task_description}"
            execute_task_command(create_command)

            task_id = get_latest_task_id()
            tasks.append((task_id, task_description))

        print("\nAdded Tasks:")
        for task_id, task_description in tasks:
            print(f"Task ID: {task_id}, Description: {task_description}")

        sort_dependencies = questionary.confirm(
            "Do you want to sort the dependencies for the tasks?"
        ).ask()
        if sort_dependencies:
            action = questionary.select(
                "Individual processing or bulk?",
                choices=["1. Individual", "2. Bulk assignment"],
            ).ask()

            if action.startswith("1"):
                for task_id, task_description in tasks:
                    has_dependencies = questionary.confirm(
                        f"Does the task '{task_description}' have dependencies?"
                    ).ask()

                    if has_dependencies:
                        dependency_type = questionary.select(
                            "Is this a blocking task (secondary) or does it have dependent tasks (primary)?",
                            choices=["Secondary task", "Primary task"],
                        ).ask()

                        if dependency_type == "Secondary task":
                            blocking_task_id = questionary.text(
                                "Enter the ID of the task this is a sub-task of:"
                            ).ask()
                            modify_command = (
                                f"task {blocking_task_id} modify depends:{task_id}"
                            )
                            execute_task_command(modify_command)
                            print(
                                f"Task {task_id} is now a sub-task of {blocking_task_id}."
                            )
                        elif dependency_type == "Primary task":
                            dependent_task_ids = questionary.text(
                                "Enter the IDs of the tasks that depend on this (comma-separated):"
                            ).ask()
                            modify_dependent_tasks(task_id, dependent_task_ids)
            elif action.startswith("2"):
                manual_sort_dependencies("")

    def get_latest_task_id():
        export_command = "task +LATEST export"
        try:
            proc = subprocess.run(
                export_command, shell=True, text=True, capture_output=True
            )
            if proc.stdout:
                tasks = json.loads(proc.stdout)
                if tasks:
                    return str(tasks[0]["id"])
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

    # def modify_dependent_tasks(dependent_ids, task_id):
    # 	ids = dependent_ids.split(',')
    # 	for id in ids:
    # 		modify_command = f"task {id.strip()} modify depends:{task_id}"
    # 		execute_task_command(modify_command)
    # 		print(f"Task {task_id} now depends on task {id.strip()}.")

    def manual_sort_dependencies(sub_task_ids):
        console.print("\n[bold cyan]Manual Sorting of Dependencies:[/bold cyan]")
        for sub_task_id in sub_task_ids:
            console.print(f"- Sub-task ID: {sub_task_id}")

        console.print(
            "\nEnter the dependencies in the format 'task_id>subtask1=subtask2=subtask3>further_subtask'."
        )
        console.print(
            "Use '>' for sequential dependencies and '=' for parallel subtasks."
        )
        console.print("You can enter multiple chains separated by commas.")
        console.print("Type 'done' when finished.\n")

        while True:
            dependency_input = Prompt.ask("> ").strip()
            if dependency_input.lower() == "done":
                break

            # Split the input into individual chains
            chains = dependency_input.split(",")

            with console.status(
                "[bold green]Setting dependencies...", spinner="dots"
            ) as status:
                for chain in chains:
                    if ">" in chain or "=" in chain:
                        # Split the chain into levels
                        levels = chain.split(">")

                        for i in range(len(levels) - 1):
                            parent_tasks = levels[i].split("=")
                            child_tasks = levels[i + 1].split("=")

                            # The last task in parent_tasks depends on all child_tasks
                            parent_task = parent_tasks[-1].strip()
                            for child_task in child_tasks:
                                modify_command = f"task {parent_task} modify depends:{child_task.strip()}"
                                execute_task_command(modify_command)
                                console.print(
                                    f"Task {parent_task} now depends on task {child_task.strip()}."
                                )
                    else:
                        console.print(
                            f"[bold yellow]Warning:[/bold yellow] Skipping invalid chain: {chain}"
                        )

        console.print("[bold green]Dependency setting completed.[/bold green]")

    def remove_task_dependencies(task_ids_input):
        console.print("\n[bold cyan]Removing Task Dependencies[/bold cyan]")

        # Split the input by commas
        id_groups = task_ids_input.split(",")

        all_ids = []

        # Process each group (single ID or range)
        for group in id_groups:
            group = group.strip()
            if "-" in group:
                # This is a range
                start, end = map(int, group.split("-"))
                all_ids.extend(range(start, end + 1))
            else:
                # This is a single ID
                all_ids.append(int(group))

        with console.status(
            "[bold green]Removing dependencies...", spinner="dots"
        ) as status:
            for id in all_ids:
                modify_command = f"task {id} modify depends:"
                execute_task_command(modify_command)
                console.print(f"Dependencies removed from task {id}.")

        console.print("[bold green]Dependency removal completed.[/bold green]")

    def interactive_prompt(file_path):
        # Load from SultanDB
        # aors, projects = load_sultandb(file_path)

        # Sync with TaskWarrior to update projects and AoRs
        active_aors, inactive_aors, active_projects, inactive_projects = (
            sync_with_taskwarrior(aors, projects, file_path)
        )

        commands = {
            "ua": ("Update AoRs", ""),
            "up": ("Update Projects", ""),
            "e": ("Exit", ""),
            "s": ("Search", ""),
            "c": ("Clear Data", ""),
            "b": ("Basic summary", ""),
            "d": ("Detailed summary", ""),
            "tc": ("Task centre", ""),
            "ht": ("Handle Task", ""),
            "o": ("Overdue tasks list", ""),
            "td": ("Daily tasks", ""),
            "rr": ("Recurrent tasks report", ""),
            "z": ("Process or Value assignment", ""),
        }

        custom_style = Style(
            [
                ("qmark", "fg:#673ab7 bold"),
                ("question", "bold"),
                ("answer", "fg:#f44336 bold"),
                ("pointer", "fg:#673ab7 bold"),
                ("highlighted", "fg:#673ab7 bold"),
                ("selected", "fg:#cc5454"),
                ("separator", "fg:#cc5454"),
                ("instruction", ""),
                ("text", ""),
                ("disabled", "fg:#858585 italic"),
            ]
        )

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
                    style=custom_style,
                ).ask()

            if command == "Update AoRs":
                all_aors = active_aors + inactive_aors
                # Sort AoRs alphabetically
                all_aors.sort(key=lambda aor: aor["name"])

                # Group AoRs by prefix
                aor_groups = {}
                for aor in all_aors:
                    prefix = aor["name"].split(".")[0]
                    if prefix not in aor_groups:
                        aor_groups[prefix] = []
                    aor_groups[prefix].append(aor)

                # Prompt to select an AoR group
                aor_group_choices = list(aor_groups.keys()) + ["Back"]
                questions = [
                    inquirer.List(
                        "aor_group",
                        message="Please select an Area of Responsibility Group",
                        choices=aor_group_choices,
                    ),
                ]
                aor_group_answers = inquirer.prompt(questions)
                if aor_group_answers["aor_group"] == "Back":
                    continue

                selected_aor_group = aor_groups[aor_group_answers["aor_group"]]

                # Now prompt to select a specific AoR
                aor_choices = [aor["name"] for aor in selected_aor_group] + ["Back"]
                questions = [
                    inquirer.List(
                        "aor",
                        message="Please select an Area of Responsibility",
                        choices=aor_choices,
                    ),
                ]
                aor_answers = inquirer.prompt(questions)
                if aor_answers["aor"] == "Back":
                    continue

                selected_aor = next(
                    (
                        aor
                        for aor in selected_aor_group
                        if aor["name"] == aor_answers["aor"]
                    ),
                    None,
                )

                if selected_aor:
                    # Find the index of the selected AoR
                    item_index = all_aors.index(selected_aor)

                    # Get tags for the selected AoR
                    aor_tags = get_tags_for_item(selected_aor["name"])

                    # Prompt to view data or update
                    options = ["Update", "View Data"]
                    questions = [
                        inquirer.List(
                            "action",
                            message="Please select an action",
                            choices=options,
                        ),
                    ]
                    action_answers = inquirer.prompt(questions)

                    if action_answers["action"] == "Update":
                        # Existing code to update the selected AoR
                        update_item(
                            all_aors, item_index, file_path, "standard", aors, projects
                        )
                    elif action_answers["action"] == "View Data":
                        view_data(selected_aor, aor_tags)

            elif command == "Update Projects":
                all_projects = active_projects + inactive_projects
                # Sort projects alphabetically
                all_projects.sort(key=lambda project: project["name"])

                # Group projects by prefix
                project_groups = {}
                for project in all_projects:
                    prefix = project["name"].split(".")[0]
                    if prefix not in project_groups:
                        project_groups[prefix] = []
                    project_groups[prefix].append(project)

                # Prompt to select a project group
                project_group_choices = list(project_groups.keys()) + ["Back"]
                questions = [
                    inquirer.List(
                        "project_group",
                        message="Please select a Project Group",
                        choices=project_group_choices,
                    ),
                ]
                project_group_answers = inquirer.prompt(questions)
                if project_group_answers["project_group"] == "Back":
                    continue

                selected_project_group = project_groups[
                    project_group_answers["project_group"]
                ]

                # Now prompt to select a specific project
                project_choices = [
                    project["name"] for project in selected_project_group
                ] + ["Back"]
                questions = [
                    inquirer.List(
                        "project",
                        message="Please select a Project",
                        choices=project_choices,
                    ),
                ]
                project_answers = inquirer.prompt(questions)
                if project_answers["project"] == "Back":
                    continue

                selected_project = next(
                    (
                        project
                        for project in selected_project_group
                        if project["name"] == project_answers["project"]
                    ),
                    None,
                )

                if selected_project:
                    # Find the index of the selected project
                    item_index = all_projects.index(selected_project)

                    # Get tags for the selected project
                    project_tags = get_tags_for_item(selected_project["name"])

                    # Prompt to view data or update
                    options = ["Update", "View Data"]
                    questions = [
                        inquirer.List(
                            "action",
                            message="Please select an action",
                            choices=options,
                        ),
                    ]
                    action_answers = inquirer.prompt(questions)

                    if action_answers["action"] == "Update":
                        # Existing code to update the selected project
                        update_item(
                            all_projects,
                            item_index,
                            file_path,
                            "outcome",
                            aors,
                            projects,
                        )
                    elif action_answers["action"] == "View Data":
                        view_data(selected_project, project_tags)
            elif command == "Search":
                search_commands = [
                    "Search Data",
                    "Search Project",
                    "Search Task",
                    "Back",
                ]
                search_command = questionary.select(
                    "Please select a search command",
                    choices=search_commands,
                    style=custom_style,
                ).ask()
                if search_command == "Search Data":
                    search_data(aors, projects)
                elif command == "Search Project":
                    call_and_process_task_projects()
                elif search_command == "Search Task":
                    search_task()
            elif command == "View Data":
                all_items = active_aors + active_projects
                all_items.sort(key=lambda x: x["name"])

                item_choices = [item["name"] for item in all_items] + ["Back"]
                questions = [
                    inquirer.List(
                        "item",
                        message="Please select an item to view data",
                        choices=item_choices,
                    ),
                ]
                answers = inquirer.prompt(questions)
                if answers["item"] == "Back":
                    continue

                selected_item = next(
                    (item for item in all_items if item["name"] == answers["item"]),
                    None,
                )
                if selected_item:
                    if selected_item in active_aors:
                        item_tags = get_tags_for_item(selected_item["name"])
                    elif selected_item in active_projects:
                        item_tags = get_tags_for_item(selected_item["name"])
                    view_data(selected_item, item_tags)
                else:
                    print("Invalid item selection.")

            elif command == "Exit":
                break

            elif command == "Clear Data":
                clear_data(aors, projects, file_path)
            elif command == "Basic summary":
                basic_summary()

            elif command == "Detailed summary":
                detailed_summary()
            elif command == "Inbox":
                display_inbox_tasks()
            elif command == "Task list":
                display_due_tasks()
            elif command == "Handle Task":
                handle_task()
            elif command == "Daily tasks":
                print_tasks_for_selected_day()
            elif command == "Overdue tasks list":
                display_overdue_tasks()
            elif command == "Recurrent tasks report":
                recurrent_report()
            elif command == "Process or Value assignment":
                eisenhower()
            elif command == "Task centre":
                task_control_center()

    def search_data(aors, projects):
        search_term = input("Enter the search term: ")
        found_entries = []

        for aor in aors:
            entry = {"name": f"AoR: {aor['name']}", "matches": []}

            if search_term in aor["description"]:
                entry["matches"].append(("Description", aor["description"]))

            if search_term in aor["standard"]:
                entry["matches"].append(("Standard", aor["standard"]))

            for annotation in aor.get("annotations", []):
                if search_term in annotation["content"]:
                    entry["matches"].append(("Annotation", annotation["content"]))

            for work_log in aor.get("workLogs", []):
                if search_term in work_log["content"]:
                    entry["matches"].append(("Work Log Entry", work_log["content"]))

            if entry["matches"]:
                found_entries.append(entry)

        for project in projects:
            entry = {"name": f"Project: {project['name']}", "matches": []}

            if search_term in project["description"]:
                entry["matches"].append(("Description", project["description"]))

            if search_term in project["outcome"]:
                entry["matches"].append(("Outcome", project["outcome"]))

            for annotation in project.get("annotations", []):
                if search_term in annotation["content"]:
                    entry["matches"].append(("Annotation", annotation["content"]))

            for work_log in project.get("workLogs", []):
                if search_term in work_log["content"]:
                    entry["matches"].append(("Work Log Entry", work_log["content"]))

            if entry["matches"]:
                found_entries.append(entry)

        if found_entries:
            print(f"Search Results for '{search_term}':")
            for entry in found_entries:
                print(f"{Fore.BLUE}{entry['name']}{Fore.RESET}")
                for match in entry["matches"]:
                    field_name, field_value = match
                    field_value = field_value.replace(
                        search_term, f"{Fore.YELLOW}{search_term}{Fore.RESET}"
                    )
                    print(f" - {field_name}: {field_value}")
        else:
            print(f"No results found for '{search_term}'.")

    def clear_data(aors, projects, file_path):
        while True:
            commands = [
                "All AoR data",
                "All Projects data",
                "Everything",
                "Individual AoR or Project",
                "Go back",
            ]
            questions = [
                inquirer.List(
                    "command",
                    message="Please select a command",
                    choices=commands,
                ),
            ]
            answers = inquirer.prompt(questions)

            if answers["command"] == "All AoR data":
                confirmation = confirm_action(
                    "Are you sure you want to clear all AoR data?"
                )
                if confirmation:
                    for aor in aors:
                        aor["description"] = ""
                        aor["standard"] = ""
                        aor["annotations"] = []
                        aor["workLogs"] = []
                    print("Cleared all AoR data.")
                    save_sultandb(file_path, aors, projects)
                else:
                    print("Action canceled.")

            elif answers["command"] == "All Projects data":
                confirmation = confirm_action(
                    "Are you sure you want to clear all Projects data?"
                )
                if confirmation:
                    for project in projects:
                        project["description"] = ""
                        project["outcome"] = ""
                        project["annotations"] = []
                        project["workLogs"] = []
                    print("Cleared all Projects data.")
                    save_sultandb(file_path, aors, projects)
                else:
                    print("Action canceled.")

            elif answers["command"] == "Everything":
                confirmation = confirm_action(
                    "Are you sure you want to clear everything?"
                )
                if confirmation:
                    for aor in aors:
                        aor["description"] = ""
                        aor["standard"] = ""
                        aor["annotations"] = []
                        aor["workLogs"] = []
                    for project in projects:
                        project["description"] = ""
                        project["outcome"] = ""
                        project["annotations"] = []
                        project["workLogs"] = []
                    print("Cleared all AoR and Project data.")
                    save_sultandb(file_path, aors, projects)
                else:
                    print("Action canceled.")

            elif answers["command"] == "Individual AoR or Project":
                # Existing code for clearing individual AoR or Project
                commands = ["AoR", "Project", "Go back"]
                questions = [
                    inquirer.List(
                        "command",
                        message="Would you like to clear an AoR or a Project?",
                        choices=commands,
                    ),
                ]
                answers = inquirer.prompt(questions)

                if answers["command"] == "AoR":
                    if len(aors) == 0:
                        print("No AoRs available.")
                    else:
                        while True:
                            questions = [
                                inquirer.List(
                                    "aor",
                                    message="Please select an AoR",
                                    choices=[aor["name"] for aor in aors] + ["Go back"],
                                ),
                            ]
                            answers = inquirer.prompt(questions)

                            if answers["aor"] == "Go back":
                                break

                            item_index = next(
                                index
                                for (index, d) in enumerate(aors)
                                if d["name"] == answers["aor"]
                            )
                            aor = aors[item_index]
                            aor["description"] = ""
                            aor["standard"] = ""
                            aor["annotations"] = []
                            aor["workLogs"] = []
                            print("Cleared selected AoR data.")
                            save_sultandb(file_path, aors, projects)

                elif answers["command"] == "Project":
                    if len(projects) == 0:
                        print("No Projects available.")
                    else:
                        while True:
                            questions = [
                                inquirer.List(
                                    "project",
                                    message="Please select a Project",
                                    choices=[project["name"] for project in projects]
                                    + ["Go back"],
                                ),
                            ]
                            answers = inquirer.prompt(questions)

                            if answers["project"] == "Go back":
                                break

                            item_index = next(
                                index
                                for (index, d) in enumerate(projects)
                                if d["name"] == answers["project"]
                            )
                            project = projects[item_index]
                            project["description"] = ""
                            project["outcome"] = ""
                            project["annotations"] = []
                            project["workLogs"] = []
                            print("Cleared selected Project data.")
                            save_sultandb(file_path, aors, projects)

            elif answers["command"] == "Go back":
                break

    def confirm_action(message):
        questions = [
            inquirer.Confirm(
                "confirmation",
                message=message,
            ),
        ]
        answers = inquirer.prompt(questions)
        return answers["confirmation"]

    def get_tags_for_aor(aor_name):
        tasks = warrior.load_tasks()["pending"]
        aor_tasks = [
            task
            for task in tasks
            if "tags" in task and task.get("project") == f"AoR.{aor_name}"
        ]

        tag_counts = {}
        for task in aor_tasks:
            for tag in task["tags"]:
                if tag.startswith("AoR.") or tag.startswith("project:"):
                    continue
                if tag not in tag_counts:
                    tag_counts[tag] = 0
                tag_counts[tag] += 1

        return tag_counts

    def sync_with_taskwarrior(aors, projects, file_path):
        tasks = warrior.load_tasks()

        task_projects = set()

        for task in tasks["pending"]:
            project = task.get("project")
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
                if aor["status"] != "Completed":
                    aor["status"] = "Completed"
                completed_aors.append(aor)

        for project in projects:
            if project["name"] in task_projects:
                active_projects.append(project)
            else:
                if project["status"] != "Completed":
                    project["status"] = "Completed"
                completed_projects.append(project)

        for task_project in task_projects:
            if task_project.startswith("AoR."):
                aor_name = task_project[4:]
                if aor_name not in [aor["name"] for aor in aors]:
                    new_aor = {
                        "name": aor_name,
                        "description": "",
                        "standard": "",
                        "annotations": [],
                        "workLogs": [],
                        "status": "Active",
                    }
                    active_aors.append(new_aor)

            elif task_project not in [project["name"] for project in projects]:
                new_project = {
                    "name": task_project,
                    "description": "",
                    "outcome": "",
                    "annotations": [],
                    "workLogs": [],
                    "status": "Active",
                }
                active_projects.append(new_project)

        # Save sultandb.json
        save_sultandb(
            file_path,
            active_aors + completed_aors,
            active_projects + completed_projects,
        )

        return (
            active_aors,
            inactive_aors,
            active_projects,
            inactive_projects + completed_projects,
        )

    colors = [
        "red",
        "green",
        "yellow",
        "magenta",
        "cyan",
    ]  # colors for tree branch levels for the functions underneath

    def basic_summary():
        # from rich import print
        from rich.tree import Tree
        from rich.text import Text
        from rich.console import Console
        from collections import defaultdict

        console = Console()
        tasks = warrior.load_tasks()
        project_data = defaultdict(lambda: defaultdict(list))
        project_task_count = defaultdict(int)
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)

        for task in tasks["pending"]:
            project = task.get("project", None)
            tags = task.get("tags", [])
            description = task.get("description", "")
            task_id = task.get("id", "")
            due_date_str = task.get("due")
            due_date = (
                parse(due_date_str) if due_date_str and due_date_str != "" else None
            )

            if project:
                # Count tasks for each level of the project hierarchy
                project_levels = project.split(".")
                for i in range(1, len(project_levels) + 1):
                    project_task_count[".".join(project_levels[:i])] += 1

                if tags:
                    for tag in tags:
                        time_remaining = due_date - now if due_date else None
                        time_remaining_str = (
                            str(time_remaining)[:-7] if time_remaining else ""
                        )
                        project_data[project][tag].append(
                            [
                                f"{task_id} {description}",
                                due_date_str,
                                time_remaining_str,
                            ]
                        )
                else:
                    project_data[project]["No Tag"].append(
                        [f"{task_id} {description}", due_date_str, time_remaining_str]
                    )
            else:
                project_task_count["No Project"] += 1
                if tags:
                    for tag in tags:
                        project_data["No Project"][tag].append(
                            [
                                f"{task_id} {description}",
                                due_date_str,
                                time_remaining_str,
                            ]
                        )
                else:
                    project_data["No Project"]["No Tag"].append(
                        [f"{task_id} {description}", due_date_str, time_remaining_str]
                    )

        tree = Tree("Tasks Summary")

        for project, tag_data in sorted(project_data.items()):
            if project != "No Project":
                project_levels = project.split(".")
                project_branch = tree
                for i, level in enumerate(project_levels):
                    color = colors[i % len(colors)]
                    current_project = ".".join(project_levels[: i + 1])
                    level_text = Text(
                        f"{level} [{project_task_count[current_project]}]",
                        style=f"{color} bold",
                    )

                    if level_text not in [
                        child.label for child in project_branch.children
                    ]:
                        project_branch = project_branch.add(level_text)
                    else:
                        project_branch = next(
                            child
                            for child in project_branch.children
                            if child.label == level_text
                        )

                for tag, tasks_data in sorted(tag_data.items()):
                    tag_color = "green" if not project.startswith("AoR.") else "cyan"
                    tag_branch = project_branch.add(
                        Text(f"{tag} [{len(tasks_data)}]", style=f"{tag_color} bold")
                    )

        # Handle "No Project" separately to make sure it comes at the end
        if "No Project" in project_data:
            project_branch = tree.add(
                Text(
                    f"No Project [{project_task_count['No Project']}]", style="red bold"
                )
            )
            for tag, tasks_data in sorted(project_data["No Project"].items()):
                tag_color = "blue"
                tag_branch = project_branch.add(
                    Text(f"{tag} [{len(tasks_data)}]", style=f"{tag_color} bold")
                )

        console.print(tree)

    def next_summary():
        # the modules are imported here because of an unidentified cause: the ascii codes are getting printed in the other functions instead of coloring the output when these modules are imported in the main.
        # from rich import print
        from rich.tree import Tree
        from rich.text import Text
        from rich.console import Console

        console = Console()

        tasks = warrior.load_tasks()

        project_data = defaultdict(lambda: defaultdict(list))
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)

        for task in tasks["pending"]:
            project = task.get("project", None)
            tags = task.get("tags", [])
            description = task.get("description", "")
            task_id = task.get("id", "")
            due_date_str = task.get("due")
            due_date = (
                parse(due_date_str) if due_date_str and due_date_str != "" else None
            )

            # Only process tasks with the "next" tag
            if "next" in tags:
                if project:
                    time_remaining = due_date - now if due_date else None
                    time_remaining_str = (
                        str(time_remaining)[:-7] if time_remaining else ""
                    )
                    project_data[project]["next"] = [
                        f"{task_id} {description}",
                        due_date_str,
                        time_remaining_str,
                    ]
                else:
                    # For tasks without a project, we will put them under "No Project" key
                    project_data["No Project"]["next"].append(
                        f"{task_id} {description}"
                    )

        tree = Tree(Text("Saikou", style="green bold"))

        for project, tag_data in sorted(project_data.items()):
            if project != "No Project":
                project_levels = project.split(".")
                project_branch = tree

                for level_idx, level in enumerate(project_levels):
                    if level not in [
                        child.label.plain for child in project_branch.children
                    ]:
                        project_branch = project_branch.add(
                            Text(level, style=f"{colors[level_idx % len(colors)]} bold")
                        )
                    else:
                        project_branch = next(
                            child
                            for child in project_branch.children
                            if child.label.plain == level
                        )

                if "next" in tag_data:
                    tag_color = "blue" if not project.startswith("AoR.") else "yellow"
                    tag_branch = project_branch.add(
                        Text("next", style=f"{tag_color} bold")
                    )

                    task_data = tag_data["next"][0]
                    if task_data:
                        task_id, description = (task_data.split(" ", 1) + [""])[:2]
                        due_date = (
                            tag_data["next"][1] if len(tag_data["next"]) > 1 else None
                        )
                        try:
                            due_date_formatted = (
                                datetime.strptime(due_date, "%Y%m%dT%H%M%SZ").strftime(
                                    "%Y-%m-%d"
                                )
                                if due_date
                                else ""
                            )
                        except ValueError:
                            due_date_formatted = ""

                        time_remaining = (
                            tag_data["next"][2] if len(tag_data["next"]) > 2 else None
                        )

                        tag_branch.add(
                            f"[red bold]{task_id}[/red bold] [white bold]{description}[/white bold] [blue bold]{due_date_formatted}[/blue bold] [green bold]{time_remaining}[/green bold]"
                        )

        # Handle "No Project" separately to make sure it comes at the end
        if "No Project" in project_data:
            project_branch = tree.add(Text("No Project", style="red bold"))
            if "next" in project_data["No Project"]:
                tag_color = "blue"
                tag_branch = project_branch.add(Text("next", style=f"{tag_color} bold"))

                for task_data in project_data["No Project"]["next"]:
                    task_id, description = (task_data.split(" ", 1) + [""])[:2]
                    tag_branch.add(
                        f"[red bold]{task_id}[/red bold] [white]{description}[/white]"
                    )

        console.print(tree)

    def detailed_summary():
        # the modules are imported here because of an unidentified cause: the ascii codes are getting printed in the other functions instead of coloring the output when these modules are imported in the main.
        # from rich import print
        from rich.tree import Tree
        from rich.text import Text
        from rich.console import Console

        console = Console()

        tasks = warrior.load_tasks()

        project_data = defaultdict(lambda: defaultdict(list))
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)

        for task in tasks["pending"]:
            project = task.get("project", None)
            tags = task.get("tags", [])
            description = task.get("description", "")
            task_id = task.get("id", "")
            due_date_str = task.get("due")
            due_date = (
                parse(due_date_str) if due_date_str and due_date_str != "" else None
            )

            if project:
                if tags:
                    for tag in tags:
                        if not project_data[project][tag] or (
                            due_date
                            and (
                                not project_data[project][tag][1]
                                or due_date < parse(project_data[project][tag][1])
                            )
                        ):
                            time_remaining = due_date - now if due_date else None
                            time_remaining_str = (
                                str(time_remaining)[:-7] if time_remaining else ""
                            )
                            project_data[project][tag] = [
                                f"{task_id} {description}",
                                due_date_str,
                                time_remaining_str,
                            ]
                else:
                    time_remaining = due_date - now if due_date else None
                    time_remaining_str = (
                        str(time_remaining)[:-7] if time_remaining else ""
                    )
                    project_data[project]["No Tag"] = [
                        f"{task_id} {description}",
                        due_date_str,
                        time_remaining_str,
                    ]

            else:
                # For tasks without a project, we will put them under "No Project" key
                if tags:
                    for tag in tags:
                        project_data["No Project"][tag].append(
                            f"{task_id} {description}"
                        )
                else:
                    # For tasks without a project and without tags, we put them under "No Tag" key
                    project_data["No Project"]["No Tag"].append(
                        f"{task_id} {description}"
                    )

        tree = Tree(Text("Saikou", style="green bold"))

        for project, tag_data in sorted(project_data.items()):
            if project != "No Project":
                project_levels = project.split(".")
                project_branch = tree

                for level_idx, level in enumerate(project_levels):
                    if level not in [
                        child.label.plain for child in project_branch.children
                    ]:
                        project_branch = project_branch.add(
                            Text(level, style=f"{colors[level_idx % len(colors)]} bold")
                        )
                    else:
                        project_branch = next(
                            child
                            for child in project_branch.children
                            if child.label.plain == level
                        )

                for tag, data in sorted(tag_data.items()):
                    tag_color = "blue" if not project.startswith("AoR.") else "yellow"
                    tag_branch = project_branch.add(
                        Text(tag, style=f"{tag_color} bold")
                    )

                    task_data = data[0]
                    if task_data:
                        task_id, description = (task_data.split(" ", 1) + [""])[:2]
                        due_date = data[1] if len(data) > 1 else None
                        try:
                            due_date_formatted = (
                                datetime.strptime(due_date, "%Y%m%dT%H%M%SZ").strftime(
                                    "%Y-%m-%d"
                                )
                                if due_date
                                else ""
                            )
                        except ValueError:
                            due_date_formatted = ""

                        time_remaining = data[2] if len(data) > 2 else None

                        tag_branch.add(
                            f"[red bold]{task_id}[/red bold] [white bold]{description}[/white bold] [blue bold]{due_date_formatted}[/blue bold] [green bold]{time_remaining}[/green bold]"
                        )

        # Handle "No Project" separately to make sure it comes at the end
        if "No Project" in project_data:
            project_branch = tree.add(Text("No Project", style="red bold"))
            for tag, data in sorted(project_data["No Project"].items()):
                tag_color = "blue"
                tag_branch = project_branch.add(Text(tag, style=f"{tag_color} bold"))

                task_data = data[0]
                if task_data:
                    task_id, description = (task_data.split(" ", 1) + [""])[:2]
                    due_date = data[1] if len(data) > 1 else None
                    try:
                        due_date_formatted = (
                            datetime.strptime(due_date, "%Y%m%dT%H%M%SZ").strftime(
                                "%Y-%m-%d"
                            )
                            if due_date
                            else ""
                        )
                    except ValueError:
                        due_date_formatted = ""

                    time_remaining = data[2] if len(data) > 2 else None

                    tag_branch.add(
                        f"[red bold]{task_id}[/red bold] [white]{description}[/white] [blue bold]{due_date_formatted}[/blue bold] [green bold]{time_remaining}[/green bold]"
                    )

        console.print(tree)

    def all_summary():
        # from rich import print
        from rich.tree import Tree
        from rich.text import Text
        from rich.console import Console

        console = Console()

        tasks = warrior.load_tasks()

        project_data = defaultdict(lambda: defaultdict(list))
        no_project_data = defaultdict(list)
        no_project_no_tag_data = []
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)

        for task in tasks["pending"]:
            project = task.get("project", None)
            tags = task.get("tags", [])
            description = task.get("description", "")
            task_id = task.get("id", "")
            due_date_str = task.get("due")
            due_date = (
                parse(due_date_str) if due_date_str and due_date_str != "" else None
            )
            time_remaining = due_date - now if due_date else None
            time_remaining_str = str(time_remaining)[:-7] if time_remaining else ""
            priority = task.get("priority", "")

            if project:
                if tags:
                    for tag in tags:
                        project_data[project][tag].append(
                            [
                                f"{task_id} {description}",
                                due_date_str,
                                time_remaining_str,
                                priority,
                            ]
                        )
                else:
                    project_data[project]["No Tag"].append(
                        [
                            f"{task_id} {description}",
                            due_date_str,
                            time_remaining_str,
                            priority,
                        ]
                    )
            elif tags:
                for tag in tags:
                    no_project_data[tag].append(
                        [
                            f"{task_id} {description}",
                            due_date_str,
                            time_remaining_str,
                            priority,
                        ]
                    )
            else:
                no_project_no_tag_data.append(
                    [
                        f"{task_id} {description}",
                        due_date_str,
                        time_remaining_str,
                        priority,
                    ]
                )

        tree = Tree("Saikou", style="green bold")

        sorted_projects = sorted(
            [project for project in project_data.keys() if project != "No Project"]
        ) + ["No Project" if "No Project" in project_data else ""]

        for project in sorted_projects:
            tag_data = project_data[project]
            project_levels = project.split(".")
            project_branch = tree

            for level_idx, level in enumerate(project_levels):
                if level not in [
                    child.label.plain for child in project_branch.children
                ]:
                    project_branch = project_branch.add(
                        Text(level, style=f"{colors[level_idx % len(colors)]} bold")
                    )
                else:
                    project_branch = next(
                        child
                        for child in project_branch.children
                        if child.label.plain == level
                    )

            for tag, tasks_data in sorted(tag_data.items()):
                tag_color = "blue" if not project.startswith("AoR.") else "yellow"
                tag_branch = project_branch.add(Text(tag, style=f"{tag_color} bold"))

                for data in tasks_data:
                    task_data = data[0]
                    task_id, description = (task_data.split(" ", 1) + [""])[:2]
                    due_date = data[1] if len(data) > 1 else None
                    priority = data[3] if len(data) > 3 else "No Priority"
                    try:
                        due_date_formatted = (
                            datetime.strptime(due_date, "%Y%m%dT%H%M%SZ").strftime(
                                "%Y-%m-%d"
                            )
                            if due_date
                            else ""
                        )
                    except ValueError:
                        due_date_formatted = ""

                    time_remaining = data[2] if len(data) > 2 else None

                    color_pri = ""
                    if priority == "H":
                        color_pri = "red"
                    else:
                        color_pri = "white"

                    tag_branch.add(
                        f"[yellow bold]{priority}[/yellow bold] [red bold]{task_id}[/red bold] [{color_pri}]{description}[/{color_pri}] [blue bold]{due_date_formatted}[/blue bold] [green bold]{time_remaining}[/green bold]"
                    )

        # Handle "No Project" tasks
        no_project_branch = tree.add("No Project", style="red bold")

        for tag, tasks_data in no_project_data.items():
            tag_branch = no_project_branch.add(
                Text(f"{tag} [{len(tasks_data)} tasks]", style="blue bold")
            )

            for data in tasks_data:
                task_data = data[0]
                task_id, description = (task_data.split(" ", 1) + [""])[:2]
                due_date = data[1] if len(data) > 1 else None
                priority = data[3] if len(data) > 3 else "No Priority"
                try:
                    due_date_formatted = (
                        datetime.strptime(due_date, "%Y%m%dT%H%M%SZ").strftime(
                            "%Y-%m-%d"
                        )
                        if due_date
                        else ""
                    )
                except ValueError:
                    due_date_formatted = ""

                time_remaining = data[2] if len(data) > 2 else None

                tag_branch.add(
                    f"[yellow bold]{priority}[/yellow bold] [red bold]{task_id}[/red bold] [white]{description}[/white] [blue bold]{due_date_formatted}[/blue bold] [green bold]{time_remaining}[/green bold] "
                )

        # Handle "No Project, No Tag" tasks
        no_project_no_tag_branch = tree.add("No Project, No Tag", style="red bold")

        for data in no_project_no_tag_data:
            task_data = data[0]
            task_id, description = (task_data.split(" ", 1) + [""])[:2]
            due_date = data[1] if len(data) > 1 else None
            priority = data[3] if len(data) > 3 else "No Priority"
            try:
                due_date_formatted = (
                    datetime.strptime(due_date, "%Y%m%dT%H%M%SZ").strftime("%Y-%m-%d")
                    if due_date
                    else ""
                )
            except ValueError:
                due_date_formatted = ""

            time_remaining = data[2] if len(data) > 2 else None

            no_project_no_tag_branch.add(
                f"[yellow bold]{priority}[/yellow bold] [red bold]{task_id}[/red bold] [white]{description}[/white] [blue bold]{due_date_formatted}[/blue bold] [green bold]{time_remaining}[/green bold]"
            )

        console.print(tree)

    def recurrent_report():
        from rich.table import Table
        from rich.console import Console
        from statistics import mean

        def parse_date(date_str):
            utc_time = datetime.strptime(date_str, "%Y%m%dT%H%M%SZ")
            return utc_time.replace(tzinfo=timezone.utc).astimezone(tz=None)

        def color_code_percentage(percentage):
            if percentage > 0.75:
                return "[green]", "[/green]"
            elif 0.5 <= percentage <= 0.75:
                return "[yellow]", "[/yellow]"
            elif 0.25 <= percentage < 0.5:
                return "[magenta]", "[/magenta]"
            else:
                return "[red]", "[/red]"

        def get_all_deleted_tasks():
            # Run the 'task export' command and get the output
            result = subprocess.run(["task", "export"], stdout=subprocess.PIPE)

            # Load the output into Python as JSON
            all_tasks = json.loads(result.stdout)

            # Prepare a list to store tasks
            deleted_tasks = []

            # Iterate over all tasks
            for task in all_tasks:
                # Check if task status is 'deleted'
                if task["status"] == "deleted" and "due" in task:
                    task["due"] = datetime.strptime(
                        task["due"], "%Y%m%dT%H%M%SZ"
                    ).date()  # convert to datetime.date object
                    deleted_tasks.append(task)

            # Return the list of tasks
            return deleted_tasks

        quote = "We are what we repeatedly do. Excellence, then, is not an act, but a habit."
        print(quote)

        all_tasks = warrior.load_tasks()

        completed_tasks = all_tasks["completed"]
        pending_tasks = all_tasks["pending"]

        tasks_today = [
            task
            for task in pending_tasks + completed_tasks
            if "recur" in task
            and "due" in task
            and parse_date(task["due"]).date() == datetime.now().date()
        ]

        deleted_tasks = get_all_deleted_tasks()

        weekly_report = {}
        task_counter = 1  # Start task_counter from 1
        task_map = {}
        completion_rates = []
        total_status_counter = Counter()
        for task in tasks_today:
            status_counter = Counter()
            task_description = task["description"]
            task_id = task["id"]

            weekly_report[task_counter] = {}

            for i in range(8):
                date = datetime.now().date() - timedelta(days=i)

                completed = any(
                    task
                    for task in completed_tasks
                    if task.get("end")
                    and parse_date(task["end"]).date() == date
                    and task["description"] == task_description
                )
                pending = any(
                    task
                    for task in pending_tasks
                    if "due" in task
                    and parse_date(task["due"]).date() == date
                    and task["description"] == task_description
                )
                deleted = any(
                    task
                    for task in deleted_tasks
                    if task["description"] == task_description and task["due"] == date
                )

                due = pending

                if completed:
                    weekly_report[task_counter][date.strftime("%m-%d")] = (
                        "[green]C[/green]"
                    )
                    status_counter["C"] += 1
                elif deleted:
                    weekly_report[task_counter][date.strftime("%m-%d")] = "[red]D[/red]"
                    status_counter["D"] += 1
                elif due:
                    weekly_report[task_counter][date.strftime("%m-%d")] = (
                        "[red bold]P[/red bold]"
                    )
                    status_counter["P"] += 1
                else:
                    weekly_report[task_counter][date.strftime("%m-%d")] = "-"

            completion_percentage = status_counter["C"] / sum(status_counter.values())
            completion_rates.append(completion_percentage)
            color_open, color_close = color_code_percentage(completion_percentage)

            if completion_percentage >= 0.80:
                task_description = f"[white bold]{task_description}[/white bold]"
            task_map[task_counter] = (
                f"{color_open}{completion_percentage:.0%}{color_close} {task_description} [{task_id:02}]"
            )

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

    def run_taskwarrior_command(command):
        try:
            result = subprocess.check_output(command, shell=True, text=True)
            return result
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
            return None

    def get_tasks(filter_query):
        command = f"task {filter_query} +PENDING export"
        output = run_taskwarrior_command(command)
        if output:
            # Parse the JSON output into Python objects
            tasks = json.loads(output)
            return tasks
        else:
            return []



    dimensions = {
        "Importance": {
            "question": "How important is this task to achieving your goals?",
            "options": [
                ("Critical to core goals/mission", 5),
                ("Very important strategic objective", 4),
                ("Supports important goals", 3),
                ("Nice to have, but not essential", 2),
                ("Minimal impact on goals", 1),
                ("No relevance to goals", 0),
            ],
            "weight": 5,
        },
        "Urgency": {
            "question": "How soon does this task need to be completed?",
            "options": [
                ("Must be done immediately/today", 5),
                ("Needed this week", 4),
                ("Needed this month", 3),
                ("Needed this quarter", 2),
                ("Needed this year", 1),
                ("No time pressure", 0),
            ],
            "weight": 4,
        },
        "Consequences": {
            "question": "What are the consequences if this task is not completed?",
            "options": [
                ("Severe negative impact if not done", 5),
                ("Major problems will arise", 4),
                ("Moderate issues will occur", 3),
                ("Minor inconveniences", 2),
                ("Very little impact", 1),
                ("No consequences", 0),
            ],
            "weight": 4,
        },
        "Uncertainty": {
            "question": "How clear are the requirements and expected outcomes?",
            "options": [
                ("Complete lack of clarity", 5),
                ("Major unknowns present", 4),
                ("Several unclear aspects", 3),
                ("Minor uncertainties", 2),
                ("Mostly clear path", 1),
                ("Crystal clear requirements", 0),
            ],
            "weight": 2,
        },
        "Effort": {
            "question": "How much effort (time/resources) will this task require?",
            "options": [
                ("Massive project (months)", 5),
                ("Large project (weeks)", 4),
                ("Medium project (days)", 3),
                ("Small task (hours)", 2),
                ("Quick task (< 1 hour)", 1),
                ("Minimal effort (minutes)", 0),
            ],
            "weight": 3,
        },
    }

    def display_options(dimension_name, dimension_data):
        # Create a table with no header, simple box, and minimal styling
        table = Table(
            show_header=False,
            box=box.SIMPLE,
            show_edge=False,
            pad_edge=False,
            style="dim",
            padding=(0, 2),  # Add padding for better spacing
        )

        # Define a list of colors for the options
        colors = ["red", "orange3", "yellow", "green", "blue", "purple"]

        # Add rows to the table with colored values and descriptions
        for (description, value), color in zip(dimension_data["options"], colors):
            table.add_row(
                f"[bold {color}]{value}[/bold {color}]",
                "—",  # Use an em dash for a cleaner separator
                description,
            )

        # Create a panel with the table, adjusting the width to fit the content
        return Panel(
            table,
            title=f"[bold]{dimension_name}[/bold]",
            title_align="left",
            subtitle=dimension_data["question"],
            box=box.ROUNDED,
            expand=False,  # Ensure the panel does not expand to terminal width
            width=None,    # Let the panel adjust its width to the content
            padding=(1, 2),  # Add padding around the panel content
            style="dim",  # Apply a subtle style to the panel
        )

    def get_score(dimension_name, dimension_data):
        console.print()
        console.print(display_options(dimension_name, dimension_data))

        while True:
            try:
                value = IntPrompt.ask("[bold cyan]Enter rating (0-5)[/bold cyan]")
                if 0 <= value <= 5:
                    selected_description = next(
                        desc
                        for desc, val in dimension_data["options"]
                        if val == value
                    )
                    console.print(f"[dim]Selected: {selected_description}[/dim]")
                    return value
                console.print(
                    "[bold red]Please enter a value between 0 and 5[/bold red]"
                )
            except ValueError:
                console.print("[bold red]Please enter a valid number[/bold red]")


    def display_filter_options(filter_options):
        """
        Display the filter options in a formatted table using Rich.
        """
        table = Table(title="[bold cyan]Preset Filters[/bold cyan]", box=box.ROUNDED)
        table.add_column("Number", style="cyan", justify="center")
        table.add_column("Filter Name", style="green")
        table.add_column("Filter Query", style="dim")

        for key, (name, query) in filter_options.items():
            table.add_row(key, name, query)

        console.print(table)

    def get_filter_choice(filter_options):
        """
        Prompt the user to select a filter or enter a custom one.
        """
        display_filter_options(filter_options)

        filter_query = Prompt.ask(
            "[bold cyan]Enter your Taskwarrior filter or select a number:[/bold cyan]",
            choices=list(filter_options.keys()) + ["custom"],
            default="custom",
        )

        if filter_query in filter_options:
            selected_filter = filter_options[filter_query]
            console.print(
                f"[bold green]Using preset filter:[/bold green] [dim]{selected_filter[1]}[/dim]"
            )
            return selected_filter[1]
        else:
            custom_filter = Prompt.ask("[bold cyan]Enter your custom filter:[/bold cyan]")
            console.print(f"[bold green]Using custom filter:[/bold green] [dim]{custom_filter}[/dim]")
            return custom_filter

    def get_fork_choice():
        """
        Prompt the user to choose between priority assessment, processing, or Eisenhower matrix.
        Displays a description of each option.
        """
        # Create a table to display the options and their descriptions
        table = Table(title="[bold cyan]Choose an Action[/bold cyan]", box=box.ROUNDED)
        table.add_column("Option", style="cyan", justify="center")
        table.add_column("Description", style="green")

        # Add rows for each option
        table.add_row(
            "i",
            "Assess priority: Evaluate the task's priority based on importance, urgency, and other factors.",
        )
        table.add_row(
            "o",
            "Process: Mark tasks as done, delete them, or skip them without assessing priority.",
        )
        table.add_row(
            "e",
            "Eisenhower Matrix: Categorize tasks into the Eisenhower Matrix (Urgent/Important, Not Urgent/Important, etc.).",
        )

        # Display the table
        console.print(table)

        # Prompt the user to choose an option
        fork = Prompt.ask(
            "[bold cyan]Choose an action (i/o/e):[/bold cyan]",
            choices=["i", "o", "e"],
            default="i",
        )
        return fork

    def eisenhower():
        try:
            # Define filter options
            filter_options = {
                "1": ("Overdue", "+OVERDUE +PENDING"),
                "2": ("Due Today", "due:today"),
                "3": ("Due Tomorrow", "due:tomorrow"),
            }

            # Get the filter choice from the user
            filter_query = get_filter_choice(filter_options)

            # Get the fork choice from the user
            fork = get_fork_choice()

            if fork == "i":
                tasks = get_tasks(filter_query)


                for task in tasks:
                    print(delimiter)
                    display_task_details(task["uuid"])
                    print(Fore.CYAN + f"\nProcessing task: {task['description']}")

                    # Ask the user what action to take for this task
                    if task.get("value", 0) > 0:
                        print(
                            Fore.YELLOW
                            + f"Task has already a value of {task['value']}."
                        )
                    action = Prompt.ask(
                        "[bold cyan]Choose an action:[/bold cyan]",
                        choices=["rate", "done", "delete", "skip"],
                        default="rate",
                    )

                    if action == "done":
                        run_taskwarrior_command(f"task {task['uuid']} done")
                        console.print("[bold green]Task marked as done.[/bold green]")
                        continue  # Move to the next task
                    elif action == "delete":
                        run_taskwarrior_command(f"task {task['uuid']} delete -y")
                        console.print("[bold green]Task deleted.[/bold green]")
                        continue  # Move to the next task
                    elif action == "skip":
                        console.print("[bold blue]Skipping task.[/bold blue]")
                        continue  # Move to the next task
                    elif action == "rate":
                        # Collect scores for each dimension
                        scores = {}
                        for dimension_name, dimension_data in dimensions.items():
                            # Prompt the user to rate the task for the current dimension
                            score = get_score(dimension_name, dimension_data)
                            # Store the score in the scores dictionary
                            scores[dimension_name] = score

                        # Calculate the base value of the task
                        # The base value is the weighted sum of scores for the dimensions:
                        # Importance, Urgency, and Consequences.
                        base_value = sum(
                            scores[dim] * data["weight"]  # Multiply the score by the dimension's weight
                            for dim, data in dimensions.items()
                            if dim in ["Importance", "Urgency", "Consequences"]  # Only include these dimensions
                        )

                        # Calculate the uncertainty factor
                        # Uncertainty reduces the base value. Higher uncertainty means a lower factor.
                        # For example, if the Uncertainty score is 5, the factor is 1 - (5 * 0.1) = 0.5.
                        uncertainty_factor = 1 - (scores["Uncertainty"] * 0.1)

                        # Calculate the effort factor
                        # Effort increases the base value. Higher effort means a higher factor.
                        # For example, if the Effort score is 5, the factor is 1 + (5 * 0.5) = 3.5.
                        effort_factor = 1 + (scores["Effort"] * 0.5)

                        # Calculate the maximum possible value
                        # This is the sum of the maximum scores (5) for Importance, Urgency, and Consequences,
                        # each multiplied by their respective weights.
                        max_possible_value = sum(
                            5 * data["weight"]  # Maximum score (5) multiplied by the dimension's weight
                            for dim, data in dimensions.items()
                            if dim in ["Importance", "Urgency", "Consequences"]  # Only include these dimensions
                        )

                        # Calculate the final value
                        # The final value is the base value adjusted by the uncertainty and effort factors.
                        # Higher uncertainty reduces the value, while higher effort increases it.
                        final_value = base_value * uncertainty_factor / effort_factor

                        # Normalize the final value to a percentage (0-100)
                        # This makes it easier to compare tasks and determine priority.
                        normalized_value = round((final_value / max_possible_value) * 100, 2)


                        # ### Example Calculation:

                        # Let’s assume the following scores and weights:

                        # |Dimension|   Score|Weight|
                        #               |--- |---   |
                        # |Importance   |4   |     5|
                        # |Urgency      |3   |     4|
                        # |Consequences |5   |     4|
                        # |Uncertainty  |2   |     2|
                        # |Effort       |3   |     3|

                        # 1. **Base Value**:
                            
                        #     - Importance: 4×5=20
                                
                        #     - Urgency: 3×4=12
                                
                        #     - Consequences: 5×4=20
                                
                        #     - **Base Value**: 20+12+20=52
                                
                        # 2. **Uncertainty Factor**:
                            
                        #     - 1−(2×0.1)=0.8
                                
                        # 3. **Effort Factor**:
                            
                        #     - 1+(3×0.5)=2.5
                                
                        # 4. **Final Value**:
                            
                        #     - 52×0.8/2.5=16.64
                                
                        # 5. **Max Possible Value**:
                            
                        #     - Importance: 5×5=25
                                
                        #     - Urgency: 5×4=20
                                
                        #     - Consequences: 5×4=20
                                
                        #     - **Max Possible Value**: 25+20+20=65
                                
                        # 6. **Normalized Value**:
                            
                        #     - (16.64/65)×100=25.6

                        
                      # Determine priority level
                        priority_level = (
                            "HIGH"
                            if normalized_value >= 70
                            else "MEDIUM"
                            if normalized_value >= 40
                            else "LOW"
                        )
                        priority_color = (
                            "bold red"
                            if normalized_value >= 70
                            else "bold yellow"
                            if normalized_value >= 40
                            else "bold blue"
                        )

                        # Display results
                        result_table = Table(box=box.ROUNDED, show_header=False)
                        result_table.add_column("Metric", style="cyan")
                        result_table.add_column("Value", style="white")

                        for dimension_name, score in scores.items():
                            selected_description = next(
                                desc
                                for desc, val in dimensions[dimension_name]["options"]
                                if val == score
                            )
                            result_table.add_row(
                                dimension_name, f"[bold]{score}[/bold] - {selected_description}"
                            )

                        result_table.add_row("Final Score", f"[bold]{normalized_value}[/bold]")
                        result_table.add_row(
                            "Priority Level", f"[{priority_color}]{priority_level}[/{priority_color}]"
                        )

                        console.print()
                        console.print(
                            Panel(
                                result_table,
                                title=f"[bold cyan]Results for {task['description']}[/bold cyan]",
                                box=box.ROUNDED,
                            )
                        )

                        # Update task with value and priority
                        if normalized_value >= 70:
                            priority = "H"  # High Priority
                        elif normalized_value >= 40:
                            priority = "M"  # Medium Priority
                        else:
                            priority = "L"  # Low Priority

                        update_command = f"task {task['uuid']} modify value:{normalized_value:.2f} priority:{priority}"
                        run_taskwarrior_command(update_command)
                        console.print(
                            f"[bold green]Updated task with value: {normalized_value:.2f} and priority: {priority}[/bold green]"
                        )

            elif fork == "o":
                tasks = get_tasks(filter_query)
                for task in tasks:
                    
                    process_task(task)
            elif fork == "e":
                tasks = get_tasks(filter_query)
                for task in tasks:
                    print(delimiter)
                    display_task_details(task["uuid"])
                    print(
                        Fore.CYAN
                        + f"\nAssessing task using the Eisenhower matrix: {task['description']}"
                    )
                    matrix_section = ask_eisenhower_matrix()
                    if matrix_section in ["skip", "done", "del"]:
                        if matrix_section == "skip":
                            print(Fore.BLUE + "Skipping task.")
                        elif matrix_section == "done":
                            run_taskwarrior_command(f"task {task['uuid']} done")
                            print(Fore.GREEN + "Marked task as done.")
                        elif matrix_section == "del":
                            run_taskwarrior_command(f"task {task['uuid']} delete -y")
                            print(Fore.GREEN + f"Deleted task {task['uuid']}")
                        continue

                    # Assign attributes based on the Eisenhower matrix section
                    if matrix_section == 1:
                        update_command = (
                            f"task {task['uuid']} modify +IU-do-now priority:H"
                        )
                    elif matrix_section == 2:
                        update_command = (
                            f"task {task['uuid']} modify +INU-schedule priority:M"
                        )
                    elif matrix_section == 3:
                        update_command = (
                            f"task {task['uuid']} modify +UNI-delegate priority:L"
                        )
                    elif matrix_section == 4:
                        update_command = f"task {task['uuid']} modify +NINU-eliminate"
                    run_taskwarrior_command(update_command)
                    print(
                        Fore.GREEN
                        + "Updated task with Eisenhower matrix section attributes."
                    )
            else:
                print(Fore.RED + "Invalid option selected. Exiting.")
                return
        except KeyboardInterrupt:
            print(Fore.RED + "\nProcess interrupted. Exiting.")
            return

    def ask_eisenhower_matrix():
        while True:
            response = (
                input(
                    Fore.YELLOW
                    + "In which section of the Eisenhower matrix is this task?\n1 - Important and Urgent\n2 - Important and Not Urgent\n3 - Not Important and Urgent\n4 - Not Important and Not Urgent\n('skip', 'done', 'del'): \n:=> "
                )
                .strip()
                .lower()
            )
            if response in ["skip", "done", "del"]:
                return response
            try:
                response = int(response)
                if 1 <= response <= 4:
                    return response
                else:
                    print(Fore.RED + "Please enter a number between 1 and 4.")
            except ValueError:
                print(
                    Fore.RED
                    + "Invalid input. Please enter a number between 1 and 4, 'skip', 'done', or 'del'."
                )

    # def display_task_details(task_uuid):
    # 	command = f"task {task_uuid} export"
    # 	output = run_taskwarrior_command(command)
    # 	if output:
    # 		task_details = json.loads(output)
    # 		if task_details:
    # 			task = task_details[0]  # Assuming the first item is the task we want
    # 			for key, value in task.items():
    # 				print(f"{key}: {value}")
    # 		else:
    # 			print(Fore.RED + "No task details found.")
    # 	else:
    # 		print(Fore.RED + "Failed to retrieve task details.")

    # =========================================================

    def short_uuid(uuid):
        """Return the short version of the UUID (up to the first dash)."""
        return uuid.split("-")[0]

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
        level_text = {0: ""}
        last_level = -1
        spaces_per_level = 2  # adjust this if needed

        # Ignore the first 4 and last 3 lines
        lines = lines[4:] if len(lines) <= 7 else lines[4:-2]

        output_lines = []  # Initialize the list to store all processed projects

        for i, line in enumerate(lines):
            stripped = line.lstrip()
            level = len(line) - len(stripped)

            # Split the line into text and number, and only keep the text
            parts = stripped.split()
            if len(parts) < 2:
                continue  # Skip lines that don't have both text and a number

            text = parts[0]

            if level % spaces_per_level != 0:
                raise ValueError(f"Invalid indentation level in input on line {i + 5}")

            level //= spaces_per_level

            if level > last_level + 1:
                raise ValueError(
                    f"Indentation level increased by more than 1 on line {i + 5}"
                )

            level_text[level] = text

            # Clear all deeper levels
            level_text = {k: v for k, v in level_text.items() if k <= level}

            output_line = ".".join(level_text[l] for l in range(level + 1))
            output_lines.append(output_line)  # Add each processed project to the list

            last_level = level

        return output_lines  # Return the list of all processed projects

    def call_and_process_task_projects2():
        result = subprocess.run(["task", "projects"], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        project_list = process_input(lines)
        # for project in project_list:
        # 	print(f"{project}\n")
        return project_list

    def review_projects():
        lines = call_and_process_task_projects2()

        # Ask user where they want to start
        start_choice = console.input(
            "[deep_sky_blue1]Do you want to start from the beginning (B), from a specific project (S), or skip to No Project / Overdue tasks (K)? "
        )

        if start_choice.lower() == "k":
            lines = []  # Skip all projects
        elif start_choice.lower() == "s":
            project_list = call_and_process_task_projects2()
            project_name = search_project3(project_list)
            try:
                start_index = lines.index(project_name)
                lines = lines[start_index:]
            except ValueError:
                console.print(
                    Panel(
                        f"Project '{project_name}' not found. Starting from the beginning.",
                        style="bold yellow",
                    )
                )
        # If 'B' or any other key, start from the beginning

        for project in lines:
            # Check if the project has pending tasks
            if not has_pending_tasks(project):
                continue  # Skip to the next project if there are no pending tasks

            while True:
                # Display tasks for the current project
                display_tasks(
                    f"task project:{project} project.not:{project}. +PENDING export"
                )
                print("\n")
                # Create a table for menu options
                table = Table(
                    box=box.ROUNDED,
                    expand=False,
                    show_header=False,
                    border_style="cyan",
                )
                table.add_column("Option", style="orange_red1")
                table.add_column("Description", style="deep_sky_blue1")

                table.add_row("TM", "Task Manager")
                table.add_row("NT", "Add new task")
                table.add_row("TW", "TW prompt")
                table.add_row("DT", "View Dependency Tree")
                table.add_row("AN", "Annotate task")
                table.add_row("DD", "Assign due date")
                table.add_row("TD", "Mark task as completed")
                table.add_row("NP", "Next project")
                table.add_row("SP", "Save progress and exit")
                table.add_row("Enter", "Exit review")
                table.add_row("R", "Refresh")

                console.print(
                    Panel(table, title=f"Reviewing project: {project}", expand=False)
                )

                choice = console.input("[deep_sky_blue1]Enter your choice: ")

                if choice.lower() == "tm":
                    task_ID = console.input("[cyan]Please enter the task ID: ")
                    if task_ID:
                        task_manager(task_ID)
                elif choice.lower() == "nt":
                    add_task_to_project(project)
                elif choice.lower() == "tw":
                    handle_task()
                elif choice.lower() == "dt":
                    dependency_tree(project)
                elif choice.lower() == "td":
                    task_id = console.input("Enter the task ID to mark as completed: ")
                    command = f"task {task_id} done"
                    execute_task_command(command)
                elif choice.lower() == "an":
                    task_ID = console.input("[cyan]Please enter the task ID: ")
                    if task_ID:
                        annotation = console.input("[cyan]Enter the annotation: ")
                        subprocess.run(["task", task_ID, "annotate", annotation])
                elif choice.lower() == "dd":
                    task_ID = console.input("[cyan]Please enter the task ID: ")
                    if task_ID:
                        due_date = console.input("[cyan]Enter the due date: ")
                        subprocess.run(["task", task_ID, "modify", f"due:{due_date}"])
                elif choice.lower() == "np":
                    break  # Move to the next project
                elif choice.lower() == "r":
                    console.clear()
                elif choice.lower() == "sp":
                    console.print(
                        Panel(
                            f"Progress saved. You can resume from project '{project}' next time.",
                            style="bold green",
                        )
                    )
                    return  # Exit the review process
                elif choice == "":
                    return  # Exit the entire review process
                else:
                    console.print(
                        Panel("Invalid choice. Please try again.", style="bold red")
                    )

        console.print(
            Panel(
                "All projects with pending tasks have been processed.",
                style="bold green",
            )
        )

        # Review tasks without a project
        while True:
            # Check if there are any tasks without a project
            try:
                result = subprocess.run(
                    ["task", "project:", "+PENDING", "count"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                task_count = int(result.stdout.strip())
            except subprocess.CalledProcessError as e:
                console.print(
                    Panel(f"Error running task command: {e}", style="bold red")
                )
                return
            except ValueError:
                console.print(Panel("Error parsing task count", style="bold red"))
                return

            if task_count == 0:
                console.print(
                    Panel(
                        "No tasks without a project. Moving to overdue tasks.",
                        style="bold green",
                    )
                )
                break

            console.print(
                Panel(
                    f"Found {task_count} tasks without a project. Starting review.",
                    style="bold green",
                )
            )

            # Display tasks without a project
            display_tasks("task project: +PENDING export")
            print("\n")
            # Create a table for menu options
            table = Table(
                box=box.ROUNDED, expand=False, show_header=False, border_style="cyan"
            )
            table.add_column("Option", style="orange_red1")
            table.add_column("Description", style="deep_sky_blue1")

            table.add_row("TM", "Task Manager")
            table.add_row("NT", "Add new task")
            table.add_row("TW", "TW prompt")
            table.add_row("AN", "Annotate task")
            table.add_row("DD", "Assign due date")
            table.add_row("TD", "Mark task as completed")
            table.add_row("SP", "Save progress and exit")
            table.add_row("Enter", "Continue to overdue tasks")
            table.add_row("R", "Refresh")

            console.print(
                Panel(table, title="Reviewing tasks without a project", expand=False)
            )

            choice = console.input("[deep_sky_blue1]Enter your choice: ")

            if choice.lower() == "tm":
                task_ID = console.input("[cyan]Please enter the task ID: ")
                if task_ID:
                    task_manager(task_ID)
            elif choice.lower() == "nt":
                add_task_to_project(
                    ""
                )  # Assuming this function can handle empty project name
            elif choice.lower() == "tw":
                handle_task()
            elif choice.lower() == "td":
                task_id = console.input("Enter the task ID to mark as completed: ")
                command = f"task {task_id} done"
                execute_task_command(command)
            elif choice.lower() == "an":
                task_ID = console.input("[cyan]Please enter the task ID: ")
                if task_ID:
                    annotation = console.input("[cyan]Enter the annotation: ")
                    subprocess.run(["task", task_ID, "annotate", annotation])
            elif choice.lower() == "dd":
                task_ID = console.input("[cyan]Please enter the task ID: ")
                if task_ID:
                    due_date = console.input("[cyan]Enter the due date: ")
                    subprocess.run(["task", task_ID, "modify", f"due:{due_date}"])
            elif choice.lower() == "r":
                console.clear()
            elif choice.lower() == "sp":
                console.print(
                    Panel("Progress saved. Exiting review.", style="bold green")
                )
                return  # Exit the review process
            elif choice == "":
                break  # Proceed to overdue tasks
            else:
                console.print(
                    Panel("Invalid choice. Please try again.", style="bold red")
                )

        # Review overdue tasks
        while True:
            # Check if there are any overdue tasks
            try:
                result = subprocess.run(
                    ["task", "due.before:today", "+PENDING", "count"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                overdue_count = int(result.stdout.strip())
            except subprocess.CalledProcessError as e:
                console.print(
                    Panel(f"Error running task command: {e}", style="bold red")
                )
                return
            except ValueError:
                console.print(
                    Panel("Error parsing overdue task count", style="bold red")
                )
                return

            if overdue_count == 0:
                console.print(
                    Panel("No overdue tasks. Review complete.", style="bold green")
                )
                break

            console.print(
                Panel(
                    f"Found {overdue_count} overdue tasks. Starting review.",
                    style="bold green",
                )
            )

            # Display overdue tasks
            display_tasks("task due.before:today +PENDING export")
            print("\n")
            # Create a table for menu options
            table = Table(
                box=box.ROUNDED, expand=False, show_header=False, border_style="cyan"
            )
            table.add_column("Option", style="orange_red1")
            table.add_column("Description", style="deep_sky_blue1")

            table.add_row("TM", "Task Manager")
            table.add_row("AN", "Annotate task")
            table.add_row("DD", "Change due date")
            table.add_row("TD", "Mark task as completed")
            table.add_row("SP", "Save progress and exit")
            table.add_row("Enter", "Exit review")
            table.add_row("R", "Refresh")

            console.print(Panel(table, title="Reviewing overdue tasks", expand=False))

            choice = console.input("[deep_sky_blue1]Enter your choice: ")

            if choice.lower() == "tm":
                task_ID = console.input("[cyan]Please enter the task ID: ")
                if task_ID:
                    task_manager(task_ID)
            elif choice.lower() == "an":
                task_ID = console.input("[cyan]Please enter the task ID: ")
                if task_ID:
                    annotation = console.input("[cyan]Enter the annotation: ")
                    subprocess.run(["task", task_ID, "annotate", annotation])
            elif choice.lower() == "dd":
                task_ID = console.input("[cyan]Please enter the task ID: ")
                if task_ID:
                    new_due_date = console.input("[cyan]Enter the new due date: ")
                    subprocess.run(["task", task_ID, "modify", f"due:{new_due_date}"])
            elif choice.lower() == "td":
                task_id = console.input("Enter the task ID to mark as completed: ")
                command = f"task {task_id} done"
                execute_task_command(command)
            elif choice.lower() == "r":
                console.clear()
            elif choice.lower() == "sp":
                console.print(
                    Panel("Progress saved. Exiting review.", style="bold green")
                )
                return  # Exit the review process
            elif choice == "":
                break  # Exit the overdue tasks review
            else:
                console.print(
                    Panel("Invalid choice. Please try again.", style="bold red")
                )

        console.print(
            Panel(
                "Review complete. All projects, tasks without a project, and overdue tasks have been processed.",
                style="bold green",
            )
        )

    def has_pending_tasks(project):
        # Use Taskwarrior to get pending tasks for the project
        command = f"task project:{project} project.not:{project}. status:pending count"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        count = int(result.stdout.strip())
        return count > 0

    def search_project2(project_list):
        completer = FuzzyWordCompleter(project_list)
        item_name = prompt("Enter a project name: ", completer=completer)
        closest_match, match_score = process.extractOne(item_name, project_list)

        # You can adjust the threshold based on how strict you want the matching to be
        MATCH_THRESHOLD = 100  # For example, 80 out of 100

        if match_score >= MATCH_THRESHOLD:
            return closest_match
        else:
            return item_name  # Use the new name entered by the user

    def display_task_details(task_uuid):
        """Display a task's details in a Rich-styled tree structure."""
        console = Console()

        # Retrieve the task details from Taskwarrior
        command = f"task {task_uuid} export"
        output = run_taskwarrior_command(command)

        if not output:
            console.print("[red]Failed to retrieve task details.[/red]")
            return

        task_details = json.loads(output)
        if not task_details:
            console.print("[red]No task details found.[/red]")
            return

        task = task_details[0]
        
        # Create the main tree
        main_tree = Tree(
            Text(f"Task {task_uuid}", style="bold cyan"),
            guide_style="cyan"
        )

        # Helper function to format values appropriately
        def format_value(value):
            if isinstance(value, bool):
                return "✓" if value else "✗"
            elif isinstance(value, (int, float)):
                return str(value)
            elif isinstance(value, dict):
                return "nested dictionary"  # Placeholder for nested structures
            elif isinstance(value, list):
                return ", ".join(map(str, value))
            elif value is None:
                return "—"
            return str(value)

        # Group related fields
        field_groups = {
            "Basic Information": ["description", "status", "project", "priority"],
            "Dates": ["entry", "modified", "due", "scheduled", "until"],
            "Tags and Dependencies": ["tags", "depends"],
            "Task Status": ["waiting", "recur", "parent"],
            "Metadata": ["uuid", "urgency", "modified", "id"]
        }

        # Create branches for each group
        for group_name, fields in field_groups.items():
            # Only create group if at least one field exists
            existing_fields = [f for f in fields if f in task]
            if existing_fields:
                group_branch = main_tree.add(Text(group_name, style="bold yellow"))
                
                for field in existing_fields:
                    value = format_value(task[field])
                    # Style based on field type
                    if field in ["due", "scheduled"] and task.get(field):
                        style = "red" if field == "due" else "green"
                    elif field == "priority":
                        style = {"H": "red", "M": "yellow", "L": "blue"}.get(value, "white")
                    else:
                        style = "white"
                    
                    field_text = Text(f"{field}: ", style="blue")
                    field_text.append(value, style=style)
                    group_branch.add(field_text)

        # Add remaining fields that weren't in any group
        all_grouped_fields = [f for fields in field_groups.values() for f in fields]
        remaining_fields = [f for f in task.keys() if f not in all_grouped_fields]
        
        if remaining_fields:
            other_branch = main_tree.add(Text("Other Fields", style="bold yellow"))
            for field in remaining_fields:
                value = format_value(task[field])
                field_text = Text(f"{field}: ", style="blue")
                field_text.append(value, style="white")
                other_branch.add(field_text)

        # Print the tree
        console.print(main_tree)

    def add_new_task_to_project(project_name):
        while True:
            new_task_description = input(
                "Enter the description for the new task (or press Enter to stop adding tasks): "
            )
            if new_task_description.lower() in ["exit", ""]:
                break

            if new_task_description:
                command = f"task add {new_task_description} project:{project_name} -in"
                run_taskwarrior_command(command)
                print(Fore.GREEN + "New task added to the project.")

    def process_task(task):
        print(Fore.YELLOW + f"\nProcessing task: {task['description']}")
        display_task_details(task["uuid"])
        action = (
            input("Choose action: modify (mod) /skip (s) /delete (del) /done (d)):\n ")
            .strip()
            .lower()
        )

        if action == "mod":
            print(Fore.YELLOW + "Task details:")
        
            mod_confirm = (
                input("Do you want to modify this task? (yes/no):\n ").strip().lower()
            )
            if mod_confirm in ["yes", "y"]:
                modification = input(
                    "Enter modification (e.g., '+tag @context priority'):\n "
                )
                run_taskwarrior_command(
                    f"task {task['uuid']} modify {modification} -in"
                )

            pro_confirm = (
                input("Do you want to assign this task to a project? (yes/no):\n ")
                .strip()
                .lower()
            )
            if pro_confirm in ["yes", "y"]:
                project_list = call_and_process_task_projects2()
                selected_project = search_project2(project_list)
                run_taskwarrior_command(
                    f"task {task['uuid']} modify project:{selected_project} -in"
                )
                print(
                    Fore.GREEN + f"Task categorized under project: {selected_project}\n"
                )

                # Ask if user wants to add another task to the same project
                add_another = (
                    input("Do you want to add another task to this project? (yes/no): ")
                    .strip()
                    .lower()
                )
                if add_another in ["yes", "y"]:
                    add_new_task_to_project(selected_project)
        elif action == "skip":
            print(Fore.BLUE + "Skipping task.")
        elif action == "del":
            run_taskwarrior_command(f"task {task['uuid']} delete -y")
            print(Fore.RED + f"Deleted task {task['uuid']}")
        elif action == "d":
            run_taskwarrior_command(f"task {task['uuid']} done")
            print(Fore.GREEN + f"Marked = {task['uuid']} = as done.")

            # =========================================================

    def parse_datetime(due_date_str):
        try:
            return (
                datetime.strptime(due_date_str, "%Y%m%dT%H%M%SZ")
                if due_date_str
                else None
            )
        except ValueError:
            return None

    def parse_iso_duration(duration_str):
        """Convert ISO-8601 duration string to hours"""
        if not duration_str:
            return 0

        try:
            # Remove PT prefix
            duration = duration_str.replace("PT", "")
            hours = 0.0

            # Handle hours
            if "H" in duration:
                h_split = duration.split("H")
                hours += float(h_split[0])
                duration = h_split[1]

            # Handle minutes
            if "M" in duration:
                m_split = duration.split("M")
                hours += float(m_split[0]) / 60

            return hours
        except (ValueError, AttributeError):
            return 0

    def format_metrics_text(metrics):
        """Format metrics into aligned columns"""
        return (
            f"Tasks: {metrics['task_count']:,d} | "
            f"Value: {metrics['total_value']:,.0f} (avg: {metrics['avg_value']:,.0f}) | "
            f"Hours: {metrics['total_duration']:.1f}"
        )

    def display_tasks(command, show_details=False):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        console = Console()

        if not result.stdout:
            console.print("No tasks found.", style="bold red")
            return

        tasks = json.loads(result.stdout)
        if not tasks:
            console.print("No tasks found.", style="bold red")
            return

        project_metadata = load_project_metadata(file_path)
        project_tag_map = defaultdict(lambda: defaultdict(list))
        project_values = defaultdict(list)
        project_durations = defaultdict(list)
        tag_values = defaultdict(
            float
        )  # New dictionary to store sum of values for each tag
        now = datetime.now(timezone.utc).astimezone()

        # Precompute reusable values
        guide_styles = ["grey50", "grey50"]  # Example styles, adjust as needed

        # Process tasks and collect metrics
        for task in tasks:
            project = task.get("project", "No Project")
            tags = task.get("tags", ["No Tag"])
            description = task["description"]
            task_id = str(task["id"])

            # Entry / creation date
            created_date = None
            delta_created_str = ""
            if "entry" in task:
                try:
                    created_date = datetime.strptime(
                        task["entry"], "%Y%m%dT%H%M%SZ"
                    ).replace(tzinfo=timezone.utc)
                    delta_created = now - created_date
                    delta_created_str = f"{delta_created.days} days, {delta_created.seconds // 3600} hours ago"
                except ValueError:
                    created_date = task["entry"]

            # Due date processing
            due_date_str = task.get("due")
            due_date = parse_datetime(due_date_str) if due_date_str else None

            # Duration processing
            duration = task.get("duration", "")
            duration_hours = parse_iso_duration(duration)
            project_durations[project].append(duration_hours)

            # Value processing
            value = task.get("value")
            try:
                value = float(value) if value is not None else 0
                project_values[project].append(value)
            except ValueError:
                value = 0

            # Accumulate the value for each tag
            for tag in tags:
                tag_values[tag] += value

            # Priority level determination
            original_priority = task.get("priority")
            if original_priority:
                priority_level = original_priority.upper()
            elif value is not None:
                priority_level = "H" if value >= 2500 else "M" if value >= 700 else "L"
            else:
                priority_level = None

            # Priority color mapping
            priority_color = {
                "H": "bold red",
                "M": "bold yellow",
                "L": "dim green",
            }.get(priority_level, "bold magenta")

            # Due date color and text
            due_color = "default_color"
            delta_text = ""
            if due_date:
                delta = due_date - now
                if delta.total_seconds() < 0:
                    due_color = "red"
                elif delta.days >= 365:
                    due_color = "steel_blue"
                elif delta.days >= 90:
                    due_color = "light_slate_blue"
                elif delta.days >= 30:
                    due_color = "green_yellow"
                elif delta.days >= 7:
                    due_color = "thistle3"
                elif delta.days >= 3:
                    due_color = "yellow1"
                elif delta.days == 0:
                    due_color = "bold turquoise2"
                else:
                    due_color = "bold orange1"
                delta_text = format_timedelta(delta)

            # Map tasks to projects and tags
            for tag in tags:
                project_tag_map[project][tag].append(
                    (
                        task_id,
                        description,
                        due_date,
                        task.get("annotations", []),
                        delta_text,
                        due_color,
                        duration,
                        priority_level,
                        priority_color,
                        value,
                        created_date,
                        delta_created_str,
                    )
                )

        # Function to calculate project totals
        def get_project_totals(project_name):
            total_value = sum(project_values[project_name])
            total_duration = sum(project_durations[project_name])
            task_count = len(project_values[project_name])
            for other_project in project_values:
                if other_project.startswith(project_name + "."):
                    sub_value, sub_duration, sub_count = get_project_totals(
                        other_project
                    )
                    total_value += sub_value
                    total_duration += sub_duration
                    task_count += sub_count
            return total_value, total_duration, task_count

        # Function to create task details panel
        def create_task_details(task_info):
            (
                task_id,
                description,
                due_date,
                annotations,
                delta_text,
                due_color,
                duration,
                priority_level,
                priority_color,
                value,
                created_date,
                delta_created_str,
            ) = task_info

            details = []
            if priority_level:
                details.append(
                    Text(f"Priority: {priority_level}", style=priority_color)
                )
            if value:
                details.append(Text(f"Value: {value}", style="green"))
            if duration:
                details.append(Text(f"Duration: {duration}", style="magenta"))

            if due_date:
                formatted_due = due_date.strftime("%Y-%m-%d")
                details.append(
                    Text(f"Due: {formatted_due} ({delta_text})", style=due_color)
                )

            if created_date:
                created_str = (
                    created_date.strftime("%Y-%m-%d %H:%M:%S")
                    if isinstance(created_date, datetime)
                    else str(created_date)
                )
                details.append(
                    Text(f"Added: {created_str} ({delta_created_str})", style="blue")
                )

            if annotations:
                details.append(Text("\nAnnotations:", style="cyan bold"))
                for annotation in annotations:
                    entry_datetime = datetime.strptime(
                        annotation["entry"], "%Y%m%dT%H%M%SZ"
                    ).strftime("%Y-%m-%d %H:%M:%S")
                    # Split the entry time and description into separate Text objects with different styles
                    entry_text = Text(f"  • {entry_datetime} - ", style="yellow")
                    description_text = Text(annotation["description"], style="white")
                    # Combine the two Text objects
                    details.append(entry_text + description_text)

            return Panel.fit(
                Text("\n").join(details), border_style="blue", padding=(1, 2)
            )

        # Build the task tree
        tree = Tree("Task Overview", style="blue", guide_style="grey50")
        for project, tags in project_tag_map.items():
            if project == "No Project" and not any(tags.values()):
                continue

            # Create project hierarchy
            project_levels = project.split(".")
            current_branch = tree
            current_path = []

            for i, level in enumerate(project_levels):
                current_path.append(level)
                current_project = ".".join(current_path)
                if show_details:
                    total_value, total_duration, task_count = get_project_totals(
                        current_project
                    )
                    metrics_summary = f"[grey70]({task_count} tasks"
                    if total_value > 0:
                        metrics_summary += f" | ♦️ {total_value:,.0f}"
                    if total_duration > 0:
                        metrics_summary += f" | {total_duration:.1f}h"
                    metrics_summary += ")[/grey70]"
                    branch_label = f"[cyan1]{level}[/cyan1] {metrics_summary}"
                else:
                    branch_label = f"[cyan1]{level}[/cyan1]"

                found_branch = next(
                    (
                        child
                        for child in current_branch.children
                        if child.label.plain.startswith(level)
                    ),
                    None,
                )
                if not found_branch:
                    found_branch = current_branch.add(
                        Text.from_markup(branch_label), guide_style="grey50"
                    )
                current_branch = found_branch

            # Add project metadata
            metadata = None
            project_hierarchy = project.split(".")
            for j in range(len(project_hierarchy), 0, -1):
                partial_project = ".".join(project_hierarchy[:j])
                metadata = project_metadata.get(partial_project)
                if metadata and any(metadata.values()):
                    break
            if metadata:
                add_project_metadata_to_tree_2(metadata, current_branch)

            # Add tags and tasks
            for tag, tasks in tags.items():
                if not tasks:
                    continue

                # Add the sum of values for the tag to the tag label
                tag_value = tag_values[tag]
                tag_label = (
                    f"{tag} [green](♦️ {tag_value:,.0f})[/green]"
                    if tag_value > 0
                    else tag
                )
                tag_branch = current_branch.add(
                    Text.from_markup(tag_label), guide_style="yellow"
                )

                for task_info in sorted(tasks, key=lambda x: (x[2] is None, x[2])):
                    task_id, description, due_date, *_ = task_info
                    task_line = f"[red][[/red][medium_spring_green]{task_id}[/medium_spring_green][red]][/red] [white bold]{description}[/white bold]"
                    if due_date:
                        days_until = (due_date - now).days
                        if days_until < 0:
                            task_line += f" [red](Overdue: {abs(days_until)}d)[/red]"
                        elif days_until == 0:
                            task_line += " [yellow](Due today)[/yellow]"
                        elif days_until <= 7:
                            task_line += f" [yellow]({days_until}d left)[/yellow]"

                    task_branch = tag_branch.add(Text.from_markup(task_line))
                    if show_details:
                        details_panel = create_task_details(task_info)
                        task_branch.add(details_panel, guide_style="grey50")

        console.print(tree)

    def parse_datetime(date_string):
        # Parse the UTC datetime
        utc_time = datetime.strptime(date_string, "%Y%m%dT%H%M%SZ")
        utc_time = utc_time.replace(tzinfo=timezone.utc)
        # Convert to local time
        local_time = utc_time.astimezone(local_tz)
        return local_time

    def format_timedelta(delta):
        is_overdue = delta.total_seconds() < 0
        if is_overdue:
            delta = abs(delta)  # Make delta positive for overdue tasks

        total_seconds = int(delta.total_seconds())
        years, remainder = divmod(total_seconds, 31536000)  # 365 days
        months, remainder = divmod(remainder, 2592000)  # 30 days
        weeks, remainder = divmod(remainder, 604800)  # 7 days
        days, remainder = divmod(remainder, 86400)  # 1 day
        hours, _ = divmod(remainder, 3600)  # 1 hour

        parts = []
        if years > 0:
            parts.append(f"{years} year{'s' if years != 1 else ''}")
        if months > 0:
            parts.append(f"{months} month{'s' if months != 1 else ''}")
        if weeks > 0:
            parts.append(f"{weeks} week{'s' if weeks != 1 else ''}")
        if days > 0:
            parts.append(f"{days} day{'s' if days != 1 else ''}")
        if hours > 0 or (years == 0 and months == 0 and weeks == 0 and days == 0):
            parts.append(f"{hours} hour{'s' if hours != 1 else ''}")

        detailed_str = " ".join(parts)

        if is_overdue:
            if delta.days == 0:
                if hours == 0:
                    return "Due NOW!"
                else:
                    return f"Overdue by {hours} hour{'s' if hours != 1 else ''}"
            else:
                return (
                    f"Overdue by {delta.days} day{'s' if delta.days != 1 else ''}"
                    + (f" ~ {detailed_str}" if len(parts) > 1 else "")
                )
        else:
            if delta.days == 0:
                if hours == 0:
                    return "Due NOW!"
                else:
                    return f"Due in {hours} hour{'s' if hours != 1 else ''}"
            else:
                return f"Due in {delta.days} day{'s' if delta.days != 1 else ''}" + (
                    f" ~ {detailed_str}" if len(parts) > 1 else ""
                )

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
        table.add_row("Enter", "Exit")

        console.print(table)

    def task_control_center(choice=None):
        console = Console()
        scope_command_map = {
            "d": "task due:today +PENDING export",
            "y": "task due:yesterday +PENDING export",
            "t": "task due:tomorrow status:pending export",
            "w": "task +WEEK +PENDING export",
            "m": "task +MONTH +PENDING export",
            "o": "task due.before:today +PENDING export",
        }

        if choice is None:
            while True:
                console.print(
                    "[bold cyan]Task Control Center[/bold cyan]", justify="center"
                )
                display_menu(console)
                choice = Prompt.ask("[bold yellow]Enter your choice[/bold yellow]")

                if choice == "":
                    # console.clear()
                    break

                process_choice(choice, console, scope_command_map)
        else:
            process_choice(choice, console, scope_command_map)

    def process_choice(choice, console, scope_command_map):
        if choice in scope_command_map:
            # console.clear()
            display_tasks(scope_command_map[choice])
        elif choice == "l":
            # console.clear()
            display_due_tasks()
        elif choice == "i":
            # console.clear()
            display_inbox_tasks()
        elif choice == "h":
            handle_task()
        elif choice == "b":
            main_menu()
        else:
            console.print("Invalid choice. Please try again.", style="bold red")

    # ------------------------------------------------------------------------------------
    # Inbox Processing - GTD Style

    def greeting_pi():
        action = questionary.select(
            "What would you like to do?",
            choices=["Process inbox tasks", "Do a mind dump", "Both", "Exit"],
        ).ask()

        if action == "Do a mind dump" or action == "Both":
            lines = gtd_prompt()
            if lines:
                print("Adding the tasks to TaskWarrior database...")
                uuids = [add_task_to_taskwarrior(line) for line in lines]
                for uuid in uuids:
                    process_gtd(uuid)
            console.print("Mind dump completed.", style="bold green")

        if action == "Process inbox tasks" or action == "Both":
            process_inbox_tasks()
            console.print("Inbox tasks have been processed.", style="bold green")

        if action == "Exit":
            console.print("Goodbye!", style="bold blue")
            return

        console.print(
            "All selected tasks have been processed and stored in the database.",
            style="bold blue",
        )

    def gtd_prompt():
        console.print(Panel("Mind Dump (GTD Style)", style="bold magenta"))
        console.print(
            "Enter everything on your mind, line by line. When you're done, add empty line.",
            style="cyan",
        )
        lines = []
        while True:
            line = Prompt.ask("> ")
            if line.strip().lower() == "":
                break
            if line:
                lines.append(line)
        return lines

    def add_task_to_taskwarrior(description):
        tw = TaskWarrior()
        task = Task(tw, description=description, tags=["dump"])
        task.save()
        return task["uuid"]

    # def process_input(lines):
    # 	level_text = {0: ''}
    # 	last_level = -1
    # 	spaces_per_level = 2  # adjust this if needed

    # 	# Ignore the first 4 and last 3 lines
    # 	lines = lines[4:-3]

    # 	output_lines = []  # Initialize the list to store all processed projects

    # 	for line in lines:
    # 		stripped = line.lstrip()
    # 		level = len(line) - len(stripped)

    # 		# Split the line into text and number, and only keep the text
    # 		text = stripped.split()[0]

    # 		if level % spaces_per_level != 0:
    # 			raise ValueError('Invalid indentation level in input')

    # 		level //= spaces_per_level

    # 		if level > last_level + 1:
    # 			raise ValueError('Indentation level increased by more than 1')

    # 		level_text[level] = text

    # 		# Clear all deeper levels
    # 		level_text = {k: v for k, v in level_text.items() if k <= level}

    # 		output_line = '.'.join(level_text[l] for l in range(level + 1))

    # 		output_lines.append(output_line)  # Add each processed project to the list

    # 		last_level = level

    # 	return output_lines  # Return the list of all processed projects

    # def call_and_process_task_projects2():
    # 	result = subprocess.run(['task', 'projects'], capture_output=True, text=True)
    # 	lines = result.stdout.splitlines()
    # 	project_list = process_input(lines)
    # 	return project_list

    def search_project3(project_list):
        if callable(project_list):
            project_list = (
                project_list()
            )  # Ensure project_list is a list if it's a callable function

        if not project_list:
            print("No projects available.")
            return None, None  # Return None if project list is empty or invalid

        completer = FuzzyCompleter(WordCompleter(project_list, ignore_case=True))
        item_name = prompt("Enter a project name: ", completer=completer)
        closest_match, match_score = process.extractOne(item_name, project_list)

        MATCH_THRESHOLD = 100  # Adjust the threshold based on your preference

        if match_score >= MATCH_THRESHOLD:
            return closest_match
        else:
            return item_name  # Use the new name entered by the user if no close match found

    def add_task_to_project2(project_name):
        task_description = questionary.text(
            "Enter the description for the new task:"
        ).ask()

        create_command = f"task add proj:'{project_name}' {task_description}"
        execute_task_command(create_command)

        task_id = get_latest_task_id()
        if task_id:
            has_dependencies = questionary.confirm(
                "Does this task have dependencies?"
            ).ask()
            if has_dependencies:
                add_dependent_tasks(task_description, project_name, task_id)
        else:
            print("Failed to retrieve the task ID.")

    # def execute_task_command(command):
    # 	subprocess.run(command, shell=True)

    # def get_latest_task_id():
    # 	try:
    # 		result = subprocess.run(['task', '+LATEST', 'rc.json.array=on', 'export'], capture_output=True, text=True)
    # 		tasks = json.loads(result.stdout)
    # 		if tasks:
    # 			return tasks[-1]['id']
    # 	except (IndexError, json.JSONDecodeError) as e:
    # 		print(f"Error retrieving latest task ID: {e}")
    # 	return None

    def modify_dependent_tasks(task_id, dependent_task_ids):
        tw = TaskWarrior()
        for dep_id in dependent_task_ids.split(","):
            try:
                dep_task = tw.tasks.get(id=dep_id)
                modify_command = f"task {task_id} modify depends:{dep_id}"
                execute_task_command(modify_command)
                print(f"Task {task_id} now depends on task {dep_id}.")
            except Task.DoesNotExist:
                print(f"Task with ID {dep_id} does not exist. Skipping.")

    def add_dependent_tasks(task_description, project_name, task_id):
        print("\nMain Task Description:")
        print(task_description)
        print("\nHelpful Questions:")
        print("What needs to happen for this to be possible?")
        print("What are the sub-tasks?")
        print("What are the consequences?\n")

        print("Enter each sub-task on a new line. Type 'done' when you are finished.\n")

        sub_tasks = []
        while True:
            sub_task = input("> ").strip()
            if sub_task.lower() == "done":
                break
            if sub_task:
                sub_tasks.append(sub_task)

        print("\nMain Task Description:")
        print(task_description)
        print("Sub-tasks entered:")

        sub_task_ids = []
        for sub_task in sub_tasks:
            print(f"- {sub_task}")
            create_command = f"task add proj:'{project_name}' {sub_task}"
            execute_task_command(create_command)
            sub_task_id = get_latest_task_id()
            if sub_task_id:
                sub_task_ids.append(sub_task_id)  # collect task IDs as strings
                print(f"  ID: {sub_task_id}")
            else:
                print("Failed to retrieve sub-task ID. Skipping.")

        if sub_task_ids:  # ensure we have valid IDs before proceeding
            action = questionary.select(
                "How would you like to handle these sub-tasks?",
                choices=[
                    "1. Add them as sub-tasks of the main task",
                    "2. Manual sort dependencies",
                ],
            ).ask()

            if action.startswith("1"):
                modify_dependent_tasks(
                    task_id, ",".join(map(str, sub_task_ids))
                )  # Convert IDs to strings
            elif action.startswith("2"):
                manual_sort_dependencies(sub_task_ids)
            else:
                print("No valid sub-tasks were added for processing.")

    # def manual_sort_dependencies(sub_task_ids):
    # 	console.print("\n[bold cyan]Manual Sorting of Dependencies:[/bold cyan]")
    # 	for sub_task_id in sub_task_ids:
    # 		console.print(f"- Sub-task ID: {sub_task_id}")

    # 	console.print("\nEnter the dependencies in the format 'task_id>subtask1=subtask2=subtask3>further_subtask'.")
    # 	console.print("Use '>' for sequential dependencies and '=' for parallel subtasks.")
    # 	console.print("You can enter multiple chains separated by commas.")
    # 	console.print("Type 'done' when finished.\n")

    # 	while True:
    # 		dependency_input = Prompt.ask("> ").strip()
    # 		if dependency_input.lower() == 'done':
    # 			break

    # 		# Split the input into individual chains
    # 		chains = dependency_input.split(',')

    # 		with console.status("[bold green]Setting dependencies...", spinner="dots") as status:
    # 			for chain in chains:
    # 				if '>' in chain or '=' in chain:
    # 					# Split the chain into levels
    # 					levels = chain.split('>')

    # 					for i in range(len(levels) - 1):
    # 						parent_tasks = levels[i].split('=')
    # 						child_tasks = levels[i+1].split('=')

    # 						# The last task in parent_tasks depends on all child_tasks
    # 						parent_task = parent_tasks[-1].strip()
    # 						for child_task in child_tasks:
    # 							modify_command = f"task {parent_task} modify depends:{child_task.strip()}"
    # 							execute_task_command(modify_command)
    # 							console.print(f"Task {parent_task} now depends on task {child_task.strip()}.")
    # 				else:
    # 					console.print(f"[bold yellow]Warning:[/bold yellow] Skipping invalid chain: {chain}")

    # 	console.print("[bold green]Dependency setting completed.[/bold green]")

    def set_task_dependencies(dependency_input):
        chains = dependency_input.split(",")
        for chain in chains:
            tasks = chain.split(">")
            # Reverse to set up each as blocking the previous
            tasks.reverse()
            for i in range(len(tasks) - 1):
                dependent_id = tasks[i].strip()
                task_id = tasks[i + 1].strip()
                modify_command = f"task {task_id} modify depends:{dependent_id}"
                execute_task_command(modify_command)
                print(f"Task {dependent_id} now depends on task {task_id}.")

    # Constants
    TAG_DUMP = "dump"
    TAG_IN = "in"
    TAG_SOMEDAY = "someday"
    TAG_REFERENCE = "unsorted"
    TAG_NEXT = "next"
    PROJECT_MAYBE = "Maybe"
    PROJECT_RESOURCES = "Resources.References"
    PROJECT_WAITING_FOR = "WaitingFor"

    # Action Categories Enum for readability
    class ActionCategory(Enum):
        DELETE = "1"
        SOMEDAY = "2"
        REFERENCE = "3"
        COMPLETED = "4"

    def update_task_tags(task, add_tags, remove_tags):
        # Use set operations to optimize tag updates
        task["tags"].update(add_tags)
        task["tags"].difference_update(remove_tags)

    def ask_task_description(task):
        """Helper function to ask for task description."""
        task["description"] = Prompt.ask("Please provide a better description")
        task.save()

    def set_task_due_date(task):
        """Helper function to set due date."""
        due_date = console.input("Enter the due date: ")
        task["due"] = due_date
        task.save()

    def ask_project_selection(task):
        """Helper function for project selection."""
        project_list = call_and_process_task_projects2()
        project = search_project3(project_list)
        task["project"] = project
        update_task_tags(task, [], [TAG_IN, TAG_DUMP])
        return project

    def process_gtd(uuid):
        tw = TaskWarrior()
        task = tw.tasks.get(uuid=uuid)
        task["tags"].discard(TAG_DUMP)
        console.print(
            Panel(
                f"Processing: {task['description']} uuid:{short_uuid(task['uuid'])}",
                style="bold green",
            )
        )

        if Confirm.ask("Do you want to elaborate on this or proceed?", default=False):
            ask_task_description(task)

        if not Confirm.ask("Is this actionable?", default=False):
            process_non_actionable(task)
        else:
            process_actionable(task)

    def process_non_actionable(task):
        console.print("Choose a category for this item:", style="yellow")
        choice = Prompt.ask(
            "1. Forget (delete)\n2. Someday/Maybe list\n3. Reference\n4. Mark as completed!",
            choices=["1", "2", "3", "4"],
            default="4",
        )
        category = ActionCategory(choice)

        if category == ActionCategory.DELETE:
            task.delete()
        elif category == ActionCategory.SOMEDAY:
            update_task_tags(task, [TAG_SOMEDAY], [TAG_IN, TAG_DUMP])
            task["project"] = PROJECT_MAYBE
        elif category == ActionCategory.REFERENCE:
            update_task_tags(task, [TAG_REFERENCE], [TAG_IN, TAG_DUMP])
            task["project"] = PROJECT_RESOURCES
            ref_category = Prompt.ask("Add a category (tag) for this reference item?")
            if ref_category:
                task["tags"].add(f"{ref_category}")
        elif category == ActionCategory.COMPLETED:
            task.done()
        else:
            task["tags"].add("miscellaneous")

        task.save()

    def process_actionable(task):
        if Confirm.ask(
            "Is this a single-step task (not part of a project)?", default=False
        ):
            process_single_step(task)
        else:
            process_project_task(task)

    def process_single_step(task):
        if Confirm.ask("Is this a 2 minute task?", default=False):
            if Confirm.ask("Do you want to do it now?", default=False):
                task.done()
                return

        if not Confirm.ask("For me?", default=False):
            to_whom = Prompt.ask("To whom?")
            update_task_tags(task, [to_whom], [TAG_IN, TAG_DUMP])
            task["project"] = PROJECT_WAITING_FOR
            follow_up_date = Prompt.ask("When should you follow up? (YYYY-MM-DD)")
            task["due"] = follow_up_date
        else:
            due_date = Prompt.ask("Assign due date (YYYY-MM-DD or leave blank)")
            update_task_tags(task, [TAG_NEXT], [TAG_IN, TAG_DUMP])
            if due_date:
                task["due"] = due_date

        task.save()

    def process_project_task(task):
        if Confirm.ask("See a basic project list before selecting?", default=False):
            basic_summary()

        project = ask_project_selection(task)

        if Confirm.ask("Do you want to set a due date to task?", default=False):
            set_task_due_date(task)

        console.print("Choose a category for this item:", style="yellow")
        choice = Prompt.ask(
            "1. Add dependent tasks\n2. Set dependency\nEnter.Continue\nEnter the number of your choice",
            choices=["1", "2", ""],
        )

        if choice == "1":
            display_tasks(f"task pro:{project} +PENDING export")
            add_dependent_tasks(task["description"], project, task["uuid"])
        elif choice == "2":
            dependency_tree(project)
            manual_sort_dependencies()
        else:
            while Confirm.ask(
                f"Do you want to add another task for project: {project}?",
                default=False,
            ):
                add_task_to_project2(project)
        task.save()

    def process_inbox_tasks():
        tw = TaskWarrior()

        # Process dumped tasks
        dump_tasks = tw.tasks.filter(status="pending", tags=[TAG_DUMP])
        if dump_tasks:
            console.print(Panel("Dumped tasks found.", style="bold yellow"))
            for task in dump_tasks:
                process_gtd(task["uuid"])

        # Process inbox tasks
        inbox_tasks = tw.tasks.filter(status="pending", tags=[TAG_IN])
        if inbox_tasks:
            console.print(
                Panel("Starting processing inbox tasks.", style="bold yellow")
            )
            for task in inbox_tasks:
                process_gtd(task["uuid"])

    # ------------------------------------------------------------------------------------
    # TASK MANAGER
    from rich.tree import Tree

    def display_task_details2(task):
        console = Console()

        # Create the main tree
        task_tree = Tree("Task Details")

        # Add main task details
        task_tree.add(Text(f"Task UUID: {short_uuid(task['uuid'])}", style="cyan"))
        task_tree.add(Text(f"Description: {task['description']}", style="bold"))

        # Handle the 'entry' date
        if "entry" in task:
            try:
                created_date = datetime.strptime(
                    task["entry"], "%Y%m%dT%H%M%SZ"
                ).replace(tzinfo=timezone.utc)
                delta = datetime.now(timezone.utc) - created_date
                delta_str = f"{delta.days} days, {delta.seconds // 3600} hours ago"
                task_tree.add(
                    Text(
                        f"Added on: {created_date.strftime('%Y-%m-%d %H:%M:%S')} ({delta_str})",
                        style="light_sea_green",
                    )
                )
            except ValueError:
                task_tree.add(
                    Text(f"Added on: {task['entry']}", style="light_sea_green")
                )

        # Handle the 'due' date
        if "due" in task:
            try:
                due_date = datetime.strptime(task["due"], "%Y%m%dT%H%M%SZ").replace(
                    tzinfo=timezone.utc
                )
                delta = due_date - datetime.now(timezone.utc)
                if delta.total_seconds() < 0:
                    delta_str = f"{abs(delta.days)} days, {abs(delta.seconds) // 3600} hours overdue"
                    task_tree.add(
                        Text(
                            f"Due Date: {due_date.strftime('%Y-%m-%d %H:%M:%S')} ({delta_str})",
                            style="red",
                        )
                    )
                else:
                    delta_str = (
                        f"{delta.days} days, {delta.seconds // 3600} hours remaining"
                    )
                    task_tree.add(
                        Text(
                            f"Due Date: {due_date.strftime('%Y-%m-%d %H:%M:%S')} ({delta_str})",
                            style="light_green",
                        )
                    )
            except ValueError:
                task_tree.add(Text(f"Due Date: {task['due']}", style="red"))

        if "project" in task:
            task_tree.add(Text(f"Project: {task['project']}", style="green"))

        if "tags" in task:
            task_tree.add(Text(f"Tags: {', '.join(task['tags'])}", style="yellow"))

        if "ctx" in task:
            task_tree.add(Text(f"Context: {task['ctx']}", style="magenta"))

        # Handle annotations
        annotations = task.get("annotations", [])
        if annotations:
            annotation_branch = task_tree.add(Text("Annotations:", style="white"))
            for annotation in annotations:
                entry_datetime = parse(annotation["entry"])
                if (
                    entry_datetime.tzinfo is None
                    or entry_datetime.tzinfo.utcoffset(entry_datetime) is None
                ):
                    entry_datetime = entry_datetime.replace(tzinfo=timezone.utc)
                entry_datetime = entry_datetime.astimezone(timezone.utc)
                annotation_text = Text(
                    f"{entry_datetime.strftime('%Y-%m-%d %H:%M:%S')} - {annotation['description']}",
                    style="dim white",
                )
                annotation_branch.add(annotation_text)

        # Create a panel with the tree
        panel = Panel(
            task_tree,
            title="Task Details",
            border_style="blue",
            padding=(1, 1),
            expand=False,
        )

        # Print the panel
        console.print(panel)

    def task_manager(task_uuid):
        while True:
            tasks = get_tasks(task_uuid)
            if not tasks:
                console.print(
                    Panel("No tasks found with the provided UUID.", style="bold red")
                )
                return
            current_task = tasks[0]
            display_task_details2(current_task)

            # Create a table for menu options
            table = Table(
                box=box.ROUNDED, expand=False, show_header=False, border_style="cyan"
            )
            table.add_column("Option", style="orange_red1")
            table.add_column("Description", style="cornflower_blue")

            # Add the existing options
            if "project" in current_task and current_task["project"]:
                table.add_row("CP", "Change project")
                table.add_row("AS", "Add Sub-tasks")
                table.add_row("DT", "View Dependency Tree")
                table.add_row("LT", "View logical tree")
                table.add_row("SD", "Set Dependency")
                table.add_row("RD", "Remove Dependency")
            else:
                table.add_row("AP", "Assign project")

            # Add the new "Update Context" option
            table.add_row("CM", "Context Menu")

            # Add the remaining options
            table.add_row("TW", "TW prompt")
            table.add_row("SP", "Search Project & Manage")
            table.add_row("SA", "Select Another Task")
            table.add_row("Enter", "Exit")

            console.print(Panel(table, title="Task Management Options", expand=False))
            choice = console.input("[yellow]Enter your choice: ")

            if choice == "cm":
                context_menu(current_task)
            elif choice == "dt":
                if "project" in current_task and current_task["project"]:
                    dependency_tree(current_task["project"])
                else:
                    console.print(
                        Panel(
                            "This task does not belong to any project.",
                            style="bold red",
                        )
                    )
            elif choice in ["cp", "ap"]:
                tw = TaskWarrior()
                task = tw.get_task(uuid=task_uuid)
                project_list = call_and_process_task_projects2()
                project = search_project3(project_list)
                command = ["task", task_uuid, "modify", f"project:{project}"]
                subprocess.run(command, check=True)
                console.print(
                    Panel(
                        f"Updated task {task_uuid} to project {project}.",
                        style="bold green",
                    )
                )
            elif choice == "lt":
                if "project" in current_task and current_task["project"]:
                    display_tasks(f"task pro:{current_task['project']} +PENDING export")
                else:
                    console.print(
                        Panel("No project associated with this task.", style="bold red")
                    )
            elif choice == "as":
                add_dependent_tasks(
                    current_task["description"],
                    current_task.get("project", ""),
                    current_task["uuid"],
                )
                if "project" in current_task and current_task["project"]:
                    dependency_tree(
                        current_task["project"]
                    )  # refresh the dependency tree
            elif choice == "sd":
                # dependency_input = console.input("Enter the tasks and their dependencies in the format 'ID>ID>ID, ID>ID':\n")
                manual_sort_dependencies("")
                if "project" in current_task and current_task["project"]:
                    dependency_tree(
                        current_task["project"]
                    )  # refresh the dependency tree
            elif choice == "rd":
                task_ids_input = console.input(
                    "Enter the IDs of the tasks to remove dependencies (comma-separated):\n"
                )
                remove_task_dependencies(task_ids_input)
                if "project" in current_task and current_task["project"]:
                    dependency_tree(
                        current_task["project"]
                    )  # refresh the dependency tree
            elif choice == "tw":
                handle_task()
            elif choice == "sp":
                call_and_process_task_projects()
            elif choice == "sa":
                new_task = console.input("Enter the IDs of the new task to load:\n")
                tasks = get_tasks(new_task)
                if not tasks:
                    console.print(
                        Panel(
                            "No tasks found with the provided UUID.", style="bold red"
                        )
                    )
                    return
                current_task = tasks[0]
            elif choice == "":
                console.print(Panel("Exiting task manager.", style="bold green"))
                break
            else:
                console.print(
                    Panel("Invalid choice. Please try again.", style="bold red")
                )

            # Refresh the task details after each operation
            task_uuid = current_task["uuid"]  # Ensure we're using the correct UUID

    def context_menu(task):
        console = Console()
        while True:
            console.print(Panel("Context Menu", style="bold cyan"))
            table = Table(
                box=box.ROUNDED, expand=False, show_header=False, border_style="cyan"
            )
            table.add_column("Option", style="orange_red1")
            table.add_column("Description", style="cornflower_blue")
            table.add_row("AC", "Add Context")
            table.add_row("RC", "Remove Context")
            table.add_row("VAC", "View All Contexts")
            table.add_row("Enter", "Return to Main Menu")

            console.print(table)
            choice = console.input("[yellow]Enter your choice: ").upper()

            if choice == "AC":
                add_context(task)
            elif choice == "RC":
                remove_context(task)
            elif choice == "VAC":
                view_all_contexts()
            elif choice == "":
                break
            else:
                console.print(
                    Panel("Invalid choice. Please try again.", style="bold red")
                )

    def add_context(task):
        console = Console()
        current_context = task.get("ctx", "")
        console.print(f"Current context: {current_context}")

        new_context = console.input("Enter the context to add: ").strip()
        existing_contexts = current_context.split(",") if current_context else []

        if new_context and new_context not in existing_contexts:
            existing_contexts.append(new_context)
            new_context_string = ",".join(existing_contexts)
            command = ["task", task["uuid"], "modify", f"ctx:{new_context_string}"]
            subprocess.run(command, check=True)
            console.print(
                Panel(
                    f"Updated task context to: {new_context_string}", style="bold green"
                )
            )
        else:
            console.print(
                Panel(
                    "Context already exists or invalid input. No changes made.",
                    style="bold yellow",
                )
            )

    def remove_context(task):
        console = Console()
        current_context = task.get("ctx", "")
        console.print(f"Current context: {current_context}")

        existing_contexts = current_context.split(",") if current_context else []
        if not existing_contexts:
            console.print(Panel("No contexts to remove.", style="bold yellow"))
            return

        console.print("Existing contexts:")
        for i, ctx in enumerate(existing_contexts, 1):
            console.print(f"{i}. {ctx}")

        choice = console.input(
            "Enter the number of the context to remove or type the context name: "
        )
        if choice.isdigit() and 1 <= int(choice) <= len(existing_contexts):
            removed_context = existing_contexts.pop(int(choice) - 1)
        elif choice in existing_contexts:
            existing_contexts.remove(choice)
        else:
            console.print(
                Panel("Invalid choice. No context removed.", style="bold red")
            )
            return

        new_context_string = ",".join(existing_contexts)
        command = ["task", task["uuid"], "modify", f"ctx:{new_context_string}"]
        subprocess.run(command, check=True)
        console.print(
            Panel(f"Updated task context to: {new_context_string}", style="bold green")
        )

    def view_all_contexts():
        console = Console()

        command = ["task", "status:pending", "export"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        tasks = json.loads(result.stdout)

        context_data = {}
        for task in tasks:
            contexts = task.get("ctx", "").split(",")
            for context in contexts:
                context = context.strip()
                if context:
                    if context not in context_data:
                        context_data[context] = {"count": 0, "tasks": []}
                    context_data[context]["count"] += 1
                    context_data[context]["tasks"].append(
                        (task["id"], task.get("description", "No description"))
                    )

        table = Table(title="All Contexts in Use", box=box.ROUNDED)
        table.add_column("Context", style="cyan")
        table.add_column("#", style="magenta")
        table.add_column("Task IDs and Descriptions", style="green")

        for context, data in sorted(
            context_data.items(), key=lambda x: x[1]["count"], reverse=True
        ):
            task_info = ", ".join([f"{id}, {desc}\n" for id, desc in data["tasks"]])
            table.add_row(context, str(data["count"]), task_info)

        console.print(table)
        console.input("\nPress Enter to return to the Context Menu...")

    # import subprocess
    # import json
    # from datetime import datetime, timedelta
    # import re
    # import pytz
    # from collections import defaultdict
    # from rich.console import Console
    # from rich.panel import Panel
    # from rich.text import Text
    # from rich.table import Table
    # from rich import print as rprint
    # from rich.panel import Panel
    # from rich.text import Text
    # from rich import box

    def task_organizer():
        from datetime import time

        def get_tasks_for_day(date):
            command = f"task due:{date} status:pending export"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            tasks = json.loads(result.stdout)
            # console.print(tasks)
            return sorted(tasks, key=lambda x: x.get("due", ""))

        def parse_duration(duration_str):
            total_minutes = 0.0
            if "Y" in duration_str:
                total_minutes += (
                    float(re.search(r"(\d+)Y", duration_str).group(1)) * 525600
                )  # Approximate, doesn't account for leap years
            if "M" in duration_str and "T" not in duration_str:
                total_minutes += (
                    float(re.search(r"(\d+)M", duration_str).group(1)) * 43800
                )  # Approximate, assumes 30-day months
            if "D" in duration_str:
                total_minutes += (
                    float(re.search(r"(\d+)D", duration_str).group(1)) * 1440
                )
            if "H" in duration_str:
                total_minutes += float(re.search(r"(\d+)H", duration_str).group(1)) * 60
            if "M" in duration_str and "T" in duration_str:
                total_minutes += float(re.search(r"(\d+)M", duration_str).group(1))
            if "S" in duration_str:
                total_minutes += float(re.search(r"(\d+)S", duration_str).group(1)) / 60
            return total_minutes

        def format_duration(minutes):
            hours, mins = divmod(round(minutes), 60)
            return f"{int(hours):02d}:{int(mins):02d}"

        class TaskOrganizer:
            def __init__(self):
                self.console = Console()
                self.current_date = (datetime.now() + timedelta(days=1)).date()
                self.refresh_tasks()
                script_directory = os.path.dirname(os.path.abspath(__file__))
                self.notes_file = os.path.join(script_directory, "daily_notes.jsonl")
                self.load_notes()

            def load_notes(self):
                self.notes = {}
                if os.path.exists(self.notes_file):
                    with open(self.notes_file, "r") as f:
                        for line in f:
                            note = json.loads(line.strip())
                            date_str = note["date"]
                            if date_str not in self.notes:
                                self.notes[date_str] = []
                            if "color" not in note:
                                note["color"] = (
                                    "cyan"  # Set default color for old notes
                                )
                            self.notes[date_str].append(note)

            def save_notes(self):
                with open(self.notes_file, "w") as f:
                    for date_notes in self.notes.values():
                        for note in date_notes:
                            json.dump(note, f)
                            f.write("\n")

            def add_note(self, time, note, until="noend", color="cyan"):
                date_str = datetime.now().strftime("%Y-%m-%d")
                if date_str not in self.notes:
                    self.notes[date_str] = []

                max_index = max(
                    [
                        max([n["index"] for n in date_notes] + [-1])
                        for date_notes in self.notes.values()
                    ]
                    + [-1]
                )
                new_index = max_index + 1

                new_note = {
                    "date": date_str,
                    "index": new_index,
                    "time": time,
                    "content": note,
                    "until": until,
                    "color": color,
                }
                self.notes[date_str].append(new_note)
                self.save_notes()
                return new_index

            def create_compact_view(self):
                local_tz = pytz.timezone(
                    "Asia/Aden"
                )  # Replace with your local timezone
                start_of_day = datetime.combine(self.current_date, datetime.min.time())
                start_of_day = local_tz.localize(start_of_day)
                end_of_day = start_of_day.replace(hour=23, minute=59, second=59)
                project_counts = self.get_pending_counts("projects")
                tag_counts = self.get_pending_counts("tags")

                # Sort tasks by due time
                sorted_tasks = sorted(
                    self.tasks,
                    key=lambda x: datetime.strptime(x["due"], "%Y%m%dT%H%M%SZ"),
                )

                table = Table(
                    title=f"Tasks for {self.current_date.strftime('%Y-%m-%d')}",
                    expand=True,
                )
                table.add_column("Time", style="cyan", no_wrap=True)
                table.add_column("Duration", style="white")
                table.add_column("Task", style="white")
                table.add_column("Project", style="blue")
                table.add_column("Tags", style="yellow")

                current_time = start_of_day

                # Group tasks by their start time
                grouped_tasks = []
                for key, group in groupby(
                    sorted_tasks,
                    key=lambda x: datetime.strptime(x["due"], "%Y%m%dT%H%M%SZ")
                    .replace(tzinfo=pytz.UTC)
                    .astimezone(local_tz),
                ):
                    group_list = list(group)
                    total_duration = sum(
                        parse_duration(task.get("duration", "PT60M"))
                        for task in group_list
                    )
                    grouped_tasks.append((key, group_list, total_duration))

                for task_time, tasks, total_duration in grouped_tasks:
                    # Add free time if there's a gap
                    if task_time > current_time:
                        free_time = (task_time - current_time).total_seconds() / 60
                        if free_time > 0:
                            table.add_row(
                                current_time.strftime("%H:%M"),
                                format_duration(free_time),
                                "Free Time",
                                "",
                                "",
                                style="turquoise4",
                            )

                    # Add each task in the group individually
                    for i, task in enumerate(tasks):
                        task_duration = parse_duration(task.get("duration", "PT60M"))
                        task_description = f"{task['id']}, {task['description']}"
                        table.add_row(
                            (
                                task_time.strftime("%H:%M") if i == 0 else ""
                            ),  # Only show time for the first task in the group
                            format_duration(task_duration),
                            task_description,
                            task.get("project", ""),
                            ", ".join(task.get("tags", [])),
                        )

                    current_time = task_time + timedelta(minutes=total_duration)

                # Add any remaining free time at the end of the day
                if current_time < end_of_day:
                    final_free_time = (end_of_day - current_time).total_seconds() / 60
                    if final_free_time > 0:
                        table.add_row(
                            current_time.strftime("%H:%M"),
                            format_duration(final_free_time),
                            "Free Time",
                            "",
                            "",
                            style="dim",
                        )

                return table

            def display_compact_view(self):
                date_panel = self.create_date_panel()
                self.console.print(date_panel)

                compact_view = self.create_compact_view()
                self.console.print(compact_view)

                notes_panel = self.create_notes_panel()
                self.console.print(notes_panel)

            def run(self):
                view_mode = "calendar"  # Default view mode
                while True:
                    self.console.clear()
                    if view_mode == "calendar":
                        self.display_calendar_view()
                    else:
                        self.display_compact_view()
                    self.display_menu()
                    choice = self.console.input("[yellow]Enter your choice: ")
                    self.process_command(choice)
                    if choice.lower() == "v":
                        view_mode = "compact" if view_mode == "calendar" else "calendar"
                    self.refresh_tasks()

            def remove_note(self, index):
                for date_str, date_notes in self.notes.items():
                    self.notes[date_str] = [
                        note for note in date_notes if note["index"] != index
                    ]
                self.save_notes()

            def edit_note(self, index, new_content, new_color=None):
                for date_notes in self.notes.values():
                    for note in date_notes:
                        if note["index"] == index:
                            note["content"] = new_content
                            if new_color:
                                note["color"] = new_color
                            self.save_notes()
                            return

            def get_notes_for_day(self):
                all_notes = []
                for date_str, date_notes in self.notes.items():
                    note_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    for note in date_notes:
                        if (
                            note["until"] == "noend"
                            or datetime.strptime(note["until"], "%Y-%m-%d").date()
                            >= self.current_date
                        ):
                            if note_date <= self.current_date:
                                all_notes.append(note)
                return sorted(all_notes, key=lambda x: (x["time"], x["index"]))

            # def run(self):
            # 	while True:
            # 		self.console.clear()
            # 		self.display_calendar_view()
            # 		self.display_menu()
            # 		choice = self.console.input("[yellow]Enter your choice: ")
            # 		self.process_command(choice)
            # 		self.display_notes_panel()
            # 		self.refresh_tasks()

            def display_calendar_view(self):
                calendar_view = self.create_calendar_view()
                for item in calendar_view:
                    if isinstance(item, str):
                        self.console.print(item, end="")
                    else:
                        self.console.print(item)

            def display_menu(self):
                table = Table(
                    box=box.ROUNDED,
                    expand=False,
                    show_header=False,
                    border_style="cyan",
                )
                table.add_column("Option", style="orange_red1")
                table.add_column("Description", style="turquoise2")

                table.add_row("MV", "Move task")
                table.add_row("D", "Change duration")
                table.add_row("R", "Refresh")
                table.add_row("S", "Shift task")
                table.add_row("CD", "Select day")
                table.add_row("AD", "Add task")
                table.add_row("AS", "Arrange tasks by duration or value")
                table.add_row("TW", "TW prompt")
                table.add_row("V", "Toggle view (Calendar/Compact)")
                table.add_row("B", "Go back one day")
                table.add_row("F", "Go forward one day")
                table.add_row("", "Exit")
                table.add_row("==", "Note Options:")
                table.add_row("AN", "Add note")
                table.add_row("RN", "Remove note")
                table.add_row("EN", "Edit note")

                title = f"{self.current_date.strftime('%Y-%m-%d')}"
                self.console.print(Panel(table, title=title, expand=False))

            def process_command(self, choice):
                if choice.lower() == "n":
                    self.note_options()
                elif choice.lower() == "mv":
                    task_ids = self.console.input(
                        "[yellow]Enter task ID(s) separated by commas: "
                    ).split(",")
                    new_time = self.console.input("[yellow]Enter new time (HH:MM): ")
                    for task_id in task_ids:
                        self.move_task(task_id.strip(), new_time)
                elif choice.lower() == "v":
                    pass  #
                elif choice.lower() == "d":
                    task_ids = self.console.input(
                        "[yellow]Enter task ID(s) separated by commas: "
                    ).split(",")
                    new_duration = self.console.input(
                        "[yellow]Enter new duration (e.g., 1h30m): "
                    )
                    for task_id in task_ids:
                        self.change_duration(task_id.strip(), new_duration)
                elif choice.lower() == "r":
                    self.refresh_tasks()
                elif choice.lower() == "s":
                    shift_input = self.console.input(
                        "[yellow]Enter task ID(s) and shift duration (e.g., '321,322 +15min' or '321,322 -1h'): "
                    )
                    task_ids, shift_duration = shift_input.split(maxsplit=1)
                    for task_id in task_ids.split(","):
                        self.shift_task(f"{task_id.strip()} {shift_duration}")
                elif choice.lower() == "cd":
                    date = self.console.input(
                        "[yellow]Enter date (YYYY-MM-DD) or 'today' or 'tomorrow': "
                    )
                    self.select_day(date)
                elif choice.lower() == "ad":
                    self.add_task()
                elif choice.lower() == "tw":
                    handle_task()
                elif choice.lower() == "b":
                    self.current_date -= timedelta(days=1)
                    self.refresh_tasks()
                elif choice.lower() == "f":
                    self.current_date += timedelta(days=1)
                    self.refresh_tasks()
                elif choice.lower() == "an":
                    self.add_note_option()
                elif choice.lower() == "rn":
                    self.remove_note_option()
                elif choice.lower() == "en":
                    self.edit_note_option()
                elif choice.lower() == "as":
                    self.arrange_tasks()
                elif choice.lower() == "":
                    exit()
                else:
                    self.console.print(f"Unknown command: {choice}", style="bold red")

            def arrange_tasks(self):
                # local_tz = pytz.timezone('Asia/Aden')  # Replace with your local timezone
                sort_by = self.console.input(
                    "[yellow]Sort tasks by (D)uration or (V)alue: "
                ).lower()
                if sort_by not in ["d", "v"]:
                    self.console.print(
                        "Invalid choice. Task arrangement cancelled.", style="bold red"
                    )
                    return

                task_ids = self.console.input(
                    "[yellow]Enter task IDs separated by commas (or 'all' for all tasks): "
                )
                if task_ids.lower() == "all":
                    tasks_to_arrange = self.tasks
                else:
                    task_id_list = [task_id.strip() for task_id in task_ids.split(",")]
                    tasks_to_arrange = [
                        task for task in self.tasks if str(task["id"]) in task_id_list
                    ]

                start_time = self.console.input("[yellow]Enter start time (HH:MM): ")
                try:
                    start_time_dt = datetime.strptime(start_time, "%H:%M").time()
                except ValueError:
                    self.console.print(
                        "Invalid time format. Task arrangement cancelled.",
                        style="bold red",
                    )
                    return

                # Combine date and time, and then localize to the specified timezone
                current_time = datetime.combine(self.current_date, start_time_dt)
                current_time = local_tz.localize(current_time)

                if sort_by == "d":
                    sorted_tasks = sorted(
                        tasks_to_arrange,
                        key=lambda x: parse_duration(x.get("duration", "PT60M")),
                        reverse=True,
                    )
                elif sort_by == "v":
                    sorted_tasks = sorted(
                        tasks_to_arrange,
                        key=lambda x: float(x.get("value", 0)),
                        reverse=True,
                    )

                for task in sorted_tasks:
                    task_duration = parse_duration(task.get("duration", "PT60M"))
                    due_time = current_time.astimezone(pytz.utc).strftime(
                        "%Y%m%dT%H%M%SZ"
                    )  # Convert to UTC for taskwarrior
                    subprocess.run(
                        f"echo n | task {task['id']} modify due:{due_time}", shell=True
                    )
                    self.console.print(
                        f"Task {task['id']} arranged at {current_time.strftime('%H:%M %Z')}",
                        style="bold green",
                    )
                    current_time += timedelta(minutes=task_duration)

            def add_note_option(self):
                time = self.console.input(
                    "[yellow]Enter time for the note (HH:MM) or press Enter for current time: "
                )
                if not time:
                    time = datetime.now().strftime("%H:%M")

                self.console.print("[yellow]Enter note (press Enter twice to finish):")
                lines = []
                while True:
                    line = input()
                    if line == "":
                        break
                    lines.append(line)
                note = "\n".join(lines)

                until = self.console.input(
                    "[yellow]Enter 'until' date (YYYY-MM-DD) or press Enter for today's date: "
                )
                if not until:
                    until = self.current_date.strftime("%Y-%m-%d")

                color = self.console.input(
                    "[yellow]Enter note color (or press Enter for default cyan): "
                )
                if not color:
                    color = "cyan"

                index = self.add_note(time, note, until, color)
                self.console.print(f"Note added with index {index}", style="bold green")

            def remove_note_option(self):
                index = int(self.console.input("[yellow]Enter note index to remove: "))
                self.remove_note(index)
                self.console.print(
                    f"Note with index {index} removed", style="bold green"
                )

            def edit_note_option(self):
                index = int(self.console.input("[yellow]Enter note index to edit: "))
                self.console.print(
                    "[yellow]Enter new note content (press Enter twice to finish):"
                )
                lines = []
                while True:
                    line = input()
                    if line == "":
                        break
                    lines.append(line)
                new_content = "\n".join(lines)

                new_color = self.console.input(
                    "[yellow]Enter new color (or press Enter to keep current color): "
                )

                self.edit_note(index, new_content, new_color if new_color else None)
                self.console.print(
                    f"Note with index {index} edited", style="bold green"
                )

            def move_task(self, task_id, new_time):
                subprocess.run(
                    f"task {task_id.strip()} modify due:{self.current_date}T{new_time}",
                    shell=True,
                )
                self.console.print(
                    f"Task {task_id.strip()} moved to {new_time}", style="bold green"
                )

            def change_duration(self, task_id, new_duration):
                subprocess.run(
                    f"task {task_id.strip()} modify duration:{new_duration}", shell=True
                )
                self.console.print(
                    f"Duration for task {task_id.strip()} set to {new_duration}",
                    style="bold green",
                )

            def shift_task(self, shift_input):
                try:
                    task_id, shift_duration = shift_input.split(maxsplit=1)
                    subprocess.run(
                        f"task {task_id.strip()} modify due:due{shift_duration}",
                        shell=True,
                    )
                    self.console.print(
                        f"Task {task_id.strip()} shifted by {shift_duration}",
                        style="bold green",
                    )
                except ValueError:
                    self.console.print(
                        "Invalid input format. Please use 'TASK_ID DURATION' (e.g., '321 +15min').",
                        style="bold red",
                    )

            def select_day(self, date):
                if date.lower() == "today":
                    self.current_date = datetime.now().date()
                elif date.lower() == "tomorrow":
                    self.current_date = datetime.now().date() + timedelta(days=1)
                else:
                    try:
                        self.current_date = datetime.strptime(date, "%Y-%m-%d").date()
                    except ValueError:
                        self.console.print(
                            "Invalid date format. Please use YYYY-MM-DD.",
                            style="bold red",
                        )
                        return
                self.refresh_tasks()

            def add_task(self):
                option = self.console.input(
                    "[yellow]Choose option (N: From Next list, O: From Overdue list): "
                )

                if option.lower() == "n":
                    next_summary()
                    task_id = self.console.input("[yellow]Enter task ID: ")
                    due_time = self.console.input("[yellow]Enter due time (HH:MM): ")
                    command = f"task {task_id} modify due:{self.current_date}T{due_time} status:pending"
                elif option.lower() == "o":
                    display_overdue_tasks()
                    task_id = self.console.input("[yellow]Enter task ID: ")
                    due_time = self.console.input("[yellow]Enter due time (HH:MM): ")
                    command = f"task {task_id} modify due:{self.current_date}T{due_time} status:pending"
                else:
                    self.console.print(
                        "Invalid option. Task not added.", style="bold red"
                    )
                    return

                subprocess.run(command, shell=True)
                self.console.print(
                    f"Task {task_id} added for {due_time}", style="bold green"
                )
                self.refresh_tasks()

            def refresh_tasks(self):
                self.tasks = get_tasks_for_day(self.current_date)

            def create_task_panel(
                self,
                tasks,
                start_time,
                project_counts,
                tag_counts,
                local_tz,
                time_range,
            ):
                output = []

                total_duration = sum(
                    parse_duration(task.get("duration", "PT60M")) for task in tasks
                )
                new_end_time = start_time + timedelta(minutes=total_duration)

                task_content = Text()
                for task in tasks:
                    task_duration = parse_duration(task.get("duration", "PT60M"))
                    task_due_time = datetime.strptime(task["due"], "%Y%m%dT%H%M%SZ")
                    task_due_time = pytz.utc.localize(task_due_time).astimezone(
                        local_tz
                    )
                    due_time_only = task_due_time.strftime(
                        "%H:%M"
                    )  # Extract only the due time
                    duration_symbols = "# " * (int(task_duration) // 15)
                    text_padding = " " * (len(str(task["id"])) + 3)
                    task_content.append(f"\n[{task['id']}] ", style="bold yellow")
                    task_content.append(f"{task['description']}\n", style="white")
                    task_content.append(
                        f"{text_padding}Due: {due_time_only}\n", style="white"
                    )
                    task_content.append(
                        f"{text_padding}Duration: {format_duration(task_duration)} {duration_symbols}\n",
                        style="italic cyan",
                    )

                    if task.get("project"):
                        count = project_counts.get(task["project"], 0)
                        task_content.append(
                            f"{text_padding}{task['project']} ({count})\n", style="blue"
                        )

                    if task.get("tags"):
                        tags_str = ", ".join(
                            f"{tag} ({tag_counts.get(tag, 0)})" for tag in task["tags"]
                        )
                        task_content.append(
                            f"{text_padding}{tags_str}\n", style="magenta"
                        )

                    if task.get("chained") == "on" and "chained_link" in task:
                        task_content.append(
                            f"{text_padding}Link #: {task['chained_link']}\n",
                            style="bold red",
                        )

                    if task.get("value"):
                        task_content.append(
                            f"{text_padding}Value: {task['value']}\n",
                            style="bold light_sea_green",
                        )

                    task_content.append("\n")

                if len(tasks) > 1:
                    total_duration_symbols = ""
                    full_hours = int(total_duration) // 60
                    remaining_minutes = int(total_duration) % 60

                    if full_hours > 0:
                        total_duration_symbols += "@ " * full_hours

                    if remaining_minutes > 0:
                        total_duration_symbols += "# " * (remaining_minutes // 15)

                    task_content.append(
                        f"{text_padding}Total Duration: {format_duration(total_duration)}\n{text_padding}{total_duration_symbols}\n",
                        style="bold cyan",
                    )

                panel_padding = 1

                # Apply different panel styles based on the time range
                if time_range == "Morning":
                    panel_style = "deep_pink2"
                elif time_range == "Daytime":
                    panel_style = "steel_blue1"
                else:
                    panel_style = "orange_red1"

                task_panel = Panel(
                    task_content,
                    title=f"[bold {panel_style}]{start_time.strftime('%H:%M')}[/bold {panel_style}]",
                    expand=False,
                    border_style=panel_style,
                    padding=(panel_padding, 1),
                )

                output.append(task_panel)

                return output, new_end_time

            def create_calendar_view(self):
                local_tz = pytz.timezone(
                    "Europe/London"
                )  # Replace with your local timezone
                start_of_day = datetime.combine(self.current_date, datetime.min.time())
                start_of_day = local_tz.localize(start_of_day)
                end_of_day = start_of_day.replace(hour=23, minute=59, second=59)
                current_time = start_of_day
                project_counts = self.get_pending_counts("projects")
                tag_counts = self.get_pending_counts("tags")
                sorted_tasks = sorted(
                    self.tasks,
                    key=lambda x: datetime.strptime(x["due"], "%Y%m%dT%H%M%SZ"),
                )
                print(sorted_tasks)
                output = []
                all_items = []

                for task in sorted_tasks:
                    due_time = datetime.strptime(task["due"], "%Y%m%dT%H%M%SZ")
                    due_time = pytz.utc.localize(due_time).astimezone(local_tz)
                    task_duration = parse_duration(task.get("duration", "PT60M"))
                    task_end_time = due_time + timedelta(minutes=task_duration)
                    all_items.append(("task", due_time, task, task_end_time))

                all_items.sort(key=lambda x: x[1])
                print(all_items)
                next_item = None

                while current_time < end_of_day:
                    if next_item is None or next_item[1] < current_time:
                        next_item = next(
                            (item for item in all_items if item[1] >= current_time),
                            None,
                        )

                    if next_item:
                        free_time = (next_item[1] - current_time).total_seconds() / 60
                        if free_time > 0:
                            output.append(
                                self.create_free_time_panel(free_time, current_time)
                            )
                        current_time = next_item[1]
                        grouped_tasks = [next_item[2]]
                        task_end_time = next_item[3]

                        while True:
                            overlapping_task = next(
                                (
                                    item
                                    for item in all_items
                                    if item[1] < task_end_time
                                    and item[2] not in grouped_tasks
                                ),
                                None,
                            )
                            if overlapping_task:
                                grouped_tasks.append(overlapping_task[2])
                                task_end_time = max(task_end_time, overlapping_task[3])
                            else:
                                break

                        if current_time.time() < time(9):
                            time_range = "Morning"
                        elif current_time.time() < time(17):
                            time_range = "Daytime"
                        else:
                            time_range = "Evening"

                        task_panel_output, new_end_time = self.create_task_panel(
                            grouped_tasks,
                            current_time,
                            project_counts,
                            tag_counts,
                            local_tz,
                            time_range,
                        )
                        output.extend(task_panel_output)
                        current_time = new_end_time

                        # Remove all grouped tasks from all_items
                        all_items = [
                            item for item in all_items if item[2] not in grouped_tasks
                        ]
                    else:
                        free_time = (end_of_day - current_time).total_seconds() / 60
                        if free_time > 0:
                            output.append(
                                self.create_free_time_panel(free_time, current_time)
                            )
                        break

                return output

            # def create_notes_panel(self):
            # 	notes = self.get_notes_for_day()
            # 	notes_content = Text()

            # 	for note in notes:
            # 		notes_content.append(f"[{note['index']}] {note['time']}:\n", style="italic yellow")
            # 		for line in note['content'].split('\n'):
            # 			notes_content.append(f"  \n{line}", style="cyan")
            # 		notes_content.append("\n")

            # 	if not notes_content:
            # 		notes_content.append("No notes for today.\n", style="italic yellow")

            # 	notes_panel = Panel(
            # 		notes_content,
            # 		title="Notes",
            # 		border_style="steel_blue1",
            # 		padding=(1, 1)
            # 	)

            # 	return notes_panel

            def create_date_panel(self):
                from pyfiglet import Figlet
                import random

                formatted_date = self.current_date.strftime("%A       %B %d %Y")
                f = Figlet(font="doom")
                rendered_text = f.renderText(formatted_date)

                pending_count = self.get_pending_counts("pending")
                completed_count = self.get_pending_counts("completed")

                # Create the full text to display
                full_text = f"{rendered_text}\nPending: {pending_count}\nCompleted: {completed_count}"

                # Calculate the width of the panel based on the longest line in full_text
                max_line_length = max(len(line) for line in full_text.split("\n"))

                # Adjust the panel width to be slightly larger than the longest line
                panel_width = max_line_length + 4  # Adding a buffer for padding
                random_color = random.choice(colors)
                # Generate the panel
                return Panel(
                    Text(full_text, style=random_color),
                    border_style=random_color,
                    width=panel_width,
                )

            def display_calendar_view(self):
                # Create the date panel
                date_panel = self.create_date_panel()

                # Print the date panel
                self.console.print(date_panel)

                # Generate and print the calendar view
                calendar_view = self.create_calendar_view()
                for item in calendar_view:
                    self.console.print(item)

                # Print the notes panel
                self.console.print(self.create_notes_panel())

            def create_free_time_panel(self, free_time, start_time):
                free_panel_padding = 1
                return Panel(
                    Text(
                        f"Free Time: {format_duration(free_time)}",
                        style="bold chartreuse1",
                    ),
                    title=f"{start_time.strftime('%H:%M')}",
                    expand=False,
                    border_style="gray89",
                    padding=(free_panel_padding, 1),
                )

            def display_notes_panel(self):
                notes_panel = self.create_notes_panel()
                self.console.print(notes_panel)

            def create_notes_panel(self):
                notes = self.get_notes_for_day()
                notes_content = Text()

                for note in notes:
                    notes_content.append(
                        f"\n[{note['index']}] {note['time']}: \n", style="bold white"
                    )
                    if self.current_date.strftime("%Y-%m-%d") != note["until"]:
                        if note["until"] == "noend":
                            notes_content.append(
                                "Forever note!\n", style="italic white"
                            )
                        else:
                            notes_content.append(
                                f"Until:{note['until']}\n", style="italic white"
                            )
                    notes_content.append(
                        f"{note['content']}\n", style=f"italic {note['color']}"
                    )

                if not notes:
                    notes_content.append("No notes for today.\n", style="italic yellow")

                notes_panel = Panel(
                    notes_content,
                    title="[bold magenta]Notes[/bold magenta]",
                    border_style="bright_cyan",
                    padding=(1, 1),
                )

                return notes_panel

            def get_pending_counts(self, attribute):
                counts = defaultdict(int)

                def run_command(command):
                    result = subprocess.run(
                        command, shell=True, capture_output=True, text=True
                    )
                    try:
                        return int(result.stdout.strip())
                    except ValueError:
                        print(
                            f"Failed to parse count for command '{command}': {result.stdout.strip()}"
                        )
                        return 0

                if attribute == "tags":
                    unique_tags = set(
                        tag for task in self.tasks for tag in task.get("tags", [])
                    )
                    for tag in unique_tags:
                        command = f"task +{tag} +PENDING count"
                        counts[tag] = run_command(command)
                elif attribute == "projects":
                    unique_projects = set(
                        task.get("project")
                        for task in self.tasks
                        if task.get("project")
                    )
                    for project in unique_projects:
                        command = f"task project:{project} +PENDING count"
                        counts[project] = run_command(command)
                elif attribute == "pending":
                    command = f"task due:{self.current_date} status:pending count"
                    counts = run_command(command)
                elif attribute == "completed":
                    command = f"task due:{self.current_date} status:completed count"
                    counts = run_command(command)

                return counts

        TaskOrganizer().run()

        if __name__ == "__main__":
            task_organizer()

    # x_x
    def update_metadata_field(item_name, field_to_update):
        console = Console()

        # Load from SultanDB
        script_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_directory, "sultandb.json")
        aors, projects = load_sultandb(file_path)

        # Combine all items
        all_items = aors + projects

        # Try to find the selected item directly
        selected_item = next(
            (item for item in all_items if item["name"] == item_name), None
        )

        if not selected_item:
            # If not found, and item_name starts with "AoR.", try without the prefix
            if item_name.startswith("AoR."):
                item_name_no_prefix = item_name[4:]  # Remove "AoR."
                selected_item = next(
                    (item for item in all_items if item["name"] == item_name_no_prefix),
                    None,
                )
            else:
                # If not an AoR, try adding "AoR." prefix
                item_name_with_prefix = "AoR." + item_name
                selected_item = next(
                    (
                        item
                        for item in all_items
                        if item["name"] == item_name_with_prefix
                    ),
                    None,
                )

        if not selected_item:
            console.print(f"No metadata found for {item_name}.", style="bold red")
            return

        # Proceed to update the metadata field
        if field_to_update == "description":
            # Update Description
            new_description = questionary.text(
                "Enter new description:", default=selected_item.get("description", "")
            ).ask()
            selected_item["description"] = new_description
            console.print("Description updated.", style="bold green")
        elif field_to_update == "standard_or_outcome":
            # Update Standard or Outcome
            if selected_item["name"].startswith("AoR."):
                field_name = "standard"
            else:
                field_name = "outcome"
            new_value = questionary.text(
                f"Enter new {field_name}:", default=selected_item.get(field_name, "")
            ).ask()
            selected_item[field_name] = new_value
            console.print(f"{field_name.capitalize()} updated.", style="bold green")
        elif field_to_update == "annotations":
            # Add Annotation
            timestamp = datetime.now().isoformat()
            content = questionary.text("Enter annotation content:").ask()
            annotation = {"timestamp": timestamp, "content": content}
            if "annotations" not in selected_item:
                selected_item["annotations"] = []
            selected_item["annotations"].append(annotation)
            console.print("Annotation added.", style="bold green")
        elif field_to_update == "workLogs":
            # Add Work Log
            timestamp = datetime.now().isoformat()
            content = questionary.text("Enter work log content:").ask()
            work_log = {"timestamp": timestamp, "content": content}
            if "workLogs" not in selected_item:
                selected_item["workLogs"] = []
            selected_item["workLogs"].append(work_log)
            console.print("Work log added.", style="bold green")
        else:
            console.print("Invalid field to update.", style="bold red")
            return

        # Save changes to sultandb.json
        # Update the item in the original list
        if selected_item in aors:
            # Update AoRs
            for idx, aor in enumerate(aors):
                if aor["name"] == selected_item["name"]:
                    aors[idx] = selected_item
                    break
        elif selected_item in projects:
            # Update Projects
            for idx, project in enumerate(projects):
                if project["name"] == selected_item["name"]:
                    projects[idx] = selected_item
                    break

        # Save to file
        save_sultandb(file_path, aors, projects)
        console.print("Changes saved to SultanDB.", style="bold green")

    # ------------------------------------------------------------------------------------

    def main_menu():
        interactive_prompt(file_path)

    # ==================

    delimiter = "-" * 40
    if __name__ == "__main__":
        main()

    # script_directory = os.path.dirname(os.path.abspath(__file__))
    # file_path = os.path.join(script_directory, "sultandb.json")

    # interactive_prompt(file_path)


except KeyboardInterrupt:
    print(
        "\nYou have to be your own hero.\n\nDo the impossible and you are never going to doubt yourself again!\n\n\nPractice so hard that winning becomes easy."
    )
