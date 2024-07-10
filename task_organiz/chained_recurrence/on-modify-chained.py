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

    # Copy all attributes from the original task, except for specific ones we want to set differently
    exclude_attrs = ['uuid', 'id', 'status', 'end', 'modified', 'entry', 'chained_link', 'chainedPrev', 'chainedNext', 'annotations']
    for attr, value in original_task.items():
        if attr not in exclude_attrs:
            new_task[attr] = value

    # Explicitly copy UDAs
    if 'value' in original_task:
        new_task['value'] = original_task['value']

    # Set the due date based on the chain duration
    if 'cp' in original_task and 'end' in original_task:
        chained_duration = parse_duration(original_task['cp'])
        end_date = datetime.strptime(original_task['end'], "%Y%m%dT%H%M%SZ")
        new_due_date = end_date + chained_duration
        new_task['due'] = new_due_date.strftime("%Y%m%dT%H%M%SZ")

    # Set other attributes
    new_task['status'] = 'pending'
    new_task['chained_link'] = int(original_task.get('chained_link', 0)) + 1
    new_task['chainedPrev'] = short_uuid(original_task['uuid'])
    new_task['chained'] = 'on'

    # Save the new task before adding annotations
    new_task.save()

    # Copy annotations from the original task to the new task
    if 'annotations' in original_task:
        for annotation in original_task['annotations']:
            if isinstance(annotation, dict) and 'description' in annotation:
                new_task.add_annotation(annotation['description'])
            elif isinstance(annotation, str):
                new_task.add_annotation(annotation)

    # Save the task again to ensure annotations are stored
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