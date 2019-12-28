# -*- coding: utf-8 -*-
#
# This file is part of https://github.com/marcus67/ics2toodledo

import sys
import icalendar
import csv
import argparse
import datetime

ATTR_NAME_DESCRIPTION = "DESCRIPTION"
ATTR_NAME_SUBJECT = "SUMMARY"
ATTR_NAME_DATE = "DTSTART"

TIME_FORMAT = "%H:%M"
DATE_FORMAT = "%d.%m.%Y"

class Reminder(object):
    
    def __init__(self, p_due_datetime, p_subject, p_description):
        
        self.due_datetime = p_due_datetime
        self.subject = p_subject
        self.description = p_description
        
class Context(object):
    
    def __init__(self, p_folder, p_tags, p_priority, p_delta, p_due_time, p_ics_filename, p_csv_filename, p_include_overdue):
        
        self.folder = p_folder
        self.tags = p_tags
        self.priority = p_priority 
        self.delta = p_delta
        self.due_time = p_due_time
        self.ics_filename = p_ics_filename
        self.csv_filename = p_csv_filename
        self.include_overdue = p_include_overdue

def read_icalendar_file(p_filename, p_context):
    
    reminders = []
    
    today = datetime.datetime.today().date()
    
    with open(p_filename,'rb') as g: 
        calendar = icalendar.Calendar.from_ical(g.read())
        
        for subcomponent in calendar.subcomponents:     
            if isinstance(subcomponent, icalendar.Event):        
                due_date = subcomponent[ATTR_NAME_DATE].dt
                
                if due_date > today or p_context.include_overdue:           
                    reminder = Reminder(
                        p_due_datetime=due_date,
                        p_subject=subcomponent[ATTR_NAME_SUBJECT],
                        p_description=subcomponent[ATTR_NAME_DESCRIPTION])
                                
                    reminders.append(reminder)  
        
    return reminders


def process_reminders(p_reminders, p_context):
    
    for reminder in p_reminders:
        # shift due date if required
        reminder.due_datetime = reminder.due_datetime + datetime.timedelta(days=p_context.delta)
        # set due time if required
        reminder.due_datetime = datetime.datetime.combine(reminder.due_datetime, p_context.due_time.time())


def write_csv_file(p_reminders, p_context):

    with open(p_context.csv_filename, 'w', newline='') as csv_file:
        fieldnames = ["TASK","FOLDER","CONTEXT","GOAL","LOCATION","STARTDATE","STARTTIME","DUEDATE",
                      "DUETIME","REPEAT","LENGTH","TIMER","PRIORITY","TAG","STATUS","STAR","NOTE"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
        writer.writeheader()
        
        for reminder in p_reminders:
            writer.writerow({"TASK" : reminder.subject,
                             "FOLDER" : p_context.folder,
                             "DUEDATE" : reminder.due_datetime.strftime(DATE_FORMAT),
                             "DUETIME" : reminder.due_datetime.strftime(TIME_FORMAT),
                             "TAG" : p_context.tags,
                             "PRIORITY" : p_context.priority,
                             "NOTE" : reminder.description})
            
            
def read_options():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', '-f', dest='folder',
                        help='target folder for reminders')
    parser.add_argument('--tag', '-t', dest='tags', default=[], action="append",
                        help='tag for reminders')
    parser.add_argument('--priority', '-p', dest='priority', default=[],
                        help='priority for reminders')
    parser.add_argument('--due-time', '-T', dest='time', 
                        help='due time for reminders')
    parser.add_argument('--delta', '-d', dest='delta', 
                        help='delta time in days for reminder', default = "0")
    parser.add_argument('--include-overdue', '-o', dest='include_overdue', 
                        help='include overdue reminders', default = False)
    parser.add_argument('filenames', nargs=2, help='ICS_INPUT_FILE CSV_OUTPUT_FILE')

    try:
        arguments = parser.parse_args()
        
    except Exception as e: 
        parser.print_help()
        raise e 
    
    if arguments.time is not None:
        try:
            due_time = datetime.datetime.strptime(arguments.time, TIME_FORMAT)
            
        except:
            raise Exception("Invalid time format '{option}'".format(option=arguments.time))
        
    else:
        due_time = None 

    if arguments.delta is not None:    
        try: 
            delta = int(arguments.delta)
            
        except:
            raise Exception("Invalid integer format '{option}'".format(option=arguments.delta))

    else:
        delta = 0
        
    context = Context(
        p_folder=arguments.folder, 
        p_priority=arguments.priority,
        p_due_time=due_time,
        p_delta=delta, 
        p_tags=",".join(arguments.tags),
        p_ics_filename=arguments.filenames[0],
        p_csv_filename=arguments.filenames[1],
        p_include_overdue=arguments.include_overdue)
    
    return context

def main():

    try:            
        context = read_options()        
        reminders = read_icalendar_file(p_filename=context.ics_filename, p_context=context)
        process_reminders(p_reminders=reminders, p_context=context)
        write_csv_file(p_reminders=reminders, p_context=context)
    
    except Exception as e:
        sys.stderr.write("Exception '{exception}'\n".format(exception=str(e)))
        return 1
    
    return 0    
    
if __name__ == '__main__':
    sys.exit(main())
    
    