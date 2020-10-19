import prettytable
from config import Config
import pandas as pd

from schedule import Schedule


class DisplayMgr:

    def __init__(self):
        self.data = Config.getInstance().get_data()

    def get_coursesDisplayData(self):

        courses = self.data.get_courses()
        coursesDisplayData = []
        for course in courses:
            coursesDisplayData.append(
                [course.get_subject(), course.get_number(), course.get_description(),
                 course.get_meetingPattern(),
                 course.get_maxNumOfStudents(), course.get_prerequisites(), course.get_coreqs(),
                 course.get_potentialConflicts(),
                 course.get_mutuallyExclusives(), course.get_roomIn(), course.get_num_of_sections(),
                 course.get_concurrency__max()])
        return coursesDisplayData

    def get_classroomsDisplayData(self):

        classrooms = self.data.get_classrooms()
        classroomsDisplayData = []
        for classroom in classrooms:
            classroomsDisplayData.append([str(classroom.get_building()), str(classroom.get_room()),
                                          str(classroom.get_seatingCapacity()), str(classroom.get_type())])
        return classroomsDisplayData

    def get_meetingtimesDisplayData(self):

        meetingTimes = self.data.get_meetingTimes()
        meetingTimesDisplayData = []
        for meetingTime in meetingTimes:
            meetingTimesDisplayData.append(
                [meetingTime.get_days(), meetingTime.get_duration(), meetingTime.get_time()])
        return meetingTimesDisplayData

    def get_scheduleDisplayData(self, schedule):
        classes = schedule.get_classes()
        scheduleDisplayData = []
        for aclass in classes:
            scheduleDisplayData.append([aclass.get_id(), aclass.get_course().get_name(), aclass.get_room(),
                                        aclass.get_meetingTime()])
        return scheduleDisplayData

    def get_conflictsDisplayData(self, schedule):
        majorConflicts = schedule.get_majorConflicts()
        minorConflicts = schedule.get_minorConflicts()
        conflictsDisplayData = []
        for conflict in majorConflicts + minorConflicts:
            conflictsDisplayData.append([conflict.aClass, conflict.type, conflict.conflictClass, conflict.severity])
        return conflictsDisplayData

    # Function for writing to excel file
    # Used: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html

    def writeSchedule(self, schedule):
        schedule_df = pd.DataFrame(self.get_scheduleDisplayData(schedule),
                                   columns=[
                                       "Class id", "Course (Subject, Number, Section)", "Classroom (Building, Room)",
                                       "Meeting Time (Day(s), Time)"])
        conflicts_df = pd.DataFrame(self.get_conflictsDisplayData(schedule),
                                    columns=["Class", "Type", "Conflicting Class", "Severity"])
        with pd.ExcelWriter('schedule.xlsx') as writer:
            schedule_df.to_excel(writer, sheet_name='Schedule', index=False)
            conflicts_df.to_excel(writer, sheet_name='Conflicts', index=False)

    def writeAllData(self, schedule):
        courses_df = pd.DataFrame(self.get_coursesDisplayData(),
                                  columns=["Subject", "Number", "Description", "Meeting Pattern",
                                           "Max Number Of Students",
                                           "Prerequisites", "Corequisites", "Potential Conflicts",
                                           "Mutually Exclusives", "Room In"
                                      , "# of sections", "# of concurrent sections"])

        classrooms_df = pd.DataFrame(self.get_classroomsDisplayData(),
                                     columns=["Building", "Room", "Seating Capacity", "Room Type"])

        meetingtimes_df = pd.DataFrame(self.get_meetingtimesDisplayData(),
                                       columns=["Days", "Duration", "Time"])

        schedule_df = pd.DataFrame(self.get_scheduleDisplayData(schedule),
                                   columns=[
                                       "Class id", "Course (Subject, Number, Section)", "Classroom (Building, Room)",
                                       "Meeting Time (Day(s), Time)"])
        conflicts_df = pd.DataFrame(self.get_conflictsDisplayData(schedule),
                                    columns=["Class", "Type", "Conflicting Class", "Severity"])

        with pd.ExcelWriter('output.xlsx') as writer:
            courses_df.to_excel(writer, sheet_name='Courses', index=False)
            classrooms_df.to_excel(writer, sheet_name='Classrooms', index=False)
            meetingtimes_df.to_excel(writer, sheet_name='Meetingtimes', index=False)
            schedule_df.to_excel(writer, sheet_name='Schedule', index=False)
            conflicts_df.to_excel(writer, sheet_name='Conflicts', index=False)

    # Functions for displaying to the console
    def print_available_data(self, schedule):
        print("> All Available Data")
        self.print_courses()
        self.print_classrooms()
        self.print_meeting_times()
        self.print_schedule(schedule)

    def print_courses(self):
        coursesTable = prettytable.PrettyTable(
            ["subject", "number", "description", "meetingPattern", "maxNumOfStudents",
             "preReqs", "coReqs", "potentialConflicts", "mutuallyExclusives", "roomIn"
                , "# of sections", "# of concurrent sections"])
        courses = self.get_coursesDisplayData()
        for course in courses:
            coursesTable.add_row(course)
        print(coursesTable)

    def print_classrooms(self):
        classroomsTable = prettytable.PrettyTable(["building", "room", "seatingCapacity", "roomType"])
        classrooms = self.get_classroomsDisplayData()
        for classroom in classrooms:
            classroomsTable.add_row(classroom)
        print(classroomsTable)

    def print_meeting_times(self):
        meetingTimesTable = prettytable.PrettyTable(["days", "duration", "time"])
        meetingTimes = self.get_meetingtimesDisplayData()
        for meetingtime in meetingTimes:
            meetingTimesTable.add_row(meetingtime)
        print(meetingTimesTable)

    def print_generation(self, population):
        table1 = prettytable.PrettyTable(
            ["schedule #", "fitness", "# of conflicts", "classes [dept,class,room instructor]"])
        schedules = population.get_schedules()
        for i in range(0, len(schedules)):
            table1.add_row(
                [str(i), round(schedules[i].get_fitness(), 3), schedules[i].get_numberofConflicts(), schedules[i]])
        print(table1)

    def print_schedule(self, schedule):
        classes = self.get_scheduleDisplayData(schedule)
        table = prettytable.PrettyTable(
            ["Class id", "Course (Subject, Number, Section)", "Classroom (Building, Room)",
             "Meeting Time (Day(s), Time)"])
        for aclass in classes:
            table.add_row(aclass)
        print(table)

    def print_conflicts(self, schedule):
        conflicts = self.get_conflictsDisplayData(schedule)
        table = prettytable.PrettyTable(
            ["Course", "Type", "Conflicting Course", "Severity"])
        for conflict in conflicts:
            table.add_row(conflict)
        print(table)
test=Schedule()
test.initialize()
test.set_fitness()
dmgr=DisplayMgr()
dmgr.writeSchedule(test)
dmgr.print_conflicts(test)