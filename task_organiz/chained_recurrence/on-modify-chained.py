#!/usr/bin/env python

# chained recurrence duration
# uda.cp.type=duration
# uda.cp.label=Chain Link Period
# uda.chained_link.type=numeric
# uda.chained_link.label=Chain Link Number


import sys
import json
from datetime import datetime, timedelta
import re

from tasklib import TaskWarrior, Task

def parse_duration(duration_str):
    """
    Parse an ISO-8601 duration string into a timedelta object.
    """
    if not duration_str.startswith('P'):
        raise ValueError("Invalid ISO-8601 duration format")

    duration_str = duration_str[1:]  # Remove the leading 'P'
    time_part = False
    years = months = days = hours = minutes = seconds = 0

    for part in re.findall(r'\d+[YMWDHMS]', duration_str):
        value = int(part[:-1])
        unit = part[-1]

        if unit == 'T':
            time_part = True
        elif unit == 'Y':
            years = value
        elif unit == 'M':
            if time_part:
                minutes = value
            else:
                months = value
        elif unit == 'W':
            days += value * 7
        elif unit == 'D':
            days += value
        elif unit == 'H':
            hours = value
        elif unit == 'S':
            seconds = value

    return timedelta(days=days + years*365 + months*30, hours=hours, minutes=minutes, seconds=seconds)

def short_uuid(uuid):
    """Return the short version of the UUID (up to the first dash)."""
    return uuid.split('-')[0]


def create_chained_task(tw, original_task):
    """
    Creates a new chained task based on the original task.
    """
    new_task = Task(tw)

    # Ensure we copy the description
    if 'description' in original_task:
        new_task['description'] = original_task['description']
    else:
        raise ValueError("Original task must have a description")

    # Copy other relevant attributes from the original task
    for attr in ['project', 'tags', 'priority', 'cp']:
        if attr in original_task:
            new_task[attr] = original_task[attr]

    # Set the due date based on the chain duration
    if 'cp' in original_task and 'end' in original_task:
        chained_duration = parse_duration(original_task['cp'])
        end_date = datetime.strptime(original_task['end'], "%Y%m%dT%H%M%SZ")
        new_due_date = end_date + chained_duration
        new_task['due'] = new_due_date.strftime("%Y%m%dT%H%M%SZ")

    # Set other attributes
    new_task['status'] = 'pending'

    # Increment chained_link
    new_task['chained_link'] = int(original_task.get('chained_link', 0)) + 1

    # Set chainedPrev to the original task's short UUID
    new_task['chainedPrev'] = short_uuid(original_task['uuid'])

    # Set uda.chained to "on" for the new task
    new_task['chained'] = 'on'

    # Save the new task
    new_task.save()

    # Update the original task with chainedNext (short UUID)
    original_task['chainedNext'] = short_uuid(new_task['uuid'])

    print(f"Created new chained task: {short_uuid(new_task['uuid'])}", file=sys.stderr)
    return short_uuid(new_task['uuid'])

def main():
    # Read all lines from stdin
    input_lines = sys.stdin.readlines()

    # The last line is the modified task
    modified_task = json.loads(input_lines[-1])

    # Initialize TaskWarrior
    tw = TaskWarrior()

    # Check if the task was just completed, has a cp attribute,
    # and uda.chained is "on" (or not set, defaulting to "on" for backward compatibility)
    if (modified_task['status'] == 'completed' and
        modified_task.get('cp') and
        modified_task.get('end') and
        modified_task.get('chained', 'on') == 'on'):

        try:
            chained_next_uuid = create_chained_task(tw, modified_task)
            modified_task['chainedNext'] = chained_next_uuid
        except Exception as e:
            print(f"Error creating chained task: {str(e)}", file=sys.stderr)

    # Print only the modified task back to Taskwarrior
    print(json.dumps(modified_task))

if __name__ == "__main__":
    main()