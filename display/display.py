import pandas as pd
import prettytable

from classclass import Class
from config import Config


class DisplayMgr:

    def __init__(self):
        self.data = Config.getInstance().get_data()

        self.course_columns = ["Subject", "Number", "Description", "Meeting Pattern", "Max Number Of Students",
                               "Prerequisites", "Corequisites", "Potential Conflicts", "Mutually Exclusives", "Room In",
                               "# of sections", "# of concurrent sections"]

        self.classroom_columns = ["Building", "Room", "Seating Capacity", "Room Type"]

        self.meeting_times_columns = ["Days", "Duration", "Time"]

        self.schedule_columns = ["Class id", "Course (Subject, Number, Section)", "Faculty", "Building", "Room",
                                 "Day(s)", "Time", "Duration"]

        self.conflicts_columns = self.schedule_columns + ["Type", "Conflicting Class", "Severity"]

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
        for aClass in classes:
            scheduleDisplayData.append(
                [aClass.get_id(), aClass.get_course().get_name(), aClass.get_faculty(), aClass.get_room().get_building(),
                 aClass.get_room().get_room(),
                 aClass.get_meetingTime().get_days(), aClass.get_meetingTime().get_time(),
                 aClass.get_meetingTime().get_duration()])
        return scheduleDisplayData

    def get_conflictsDisplayData(self, schedule):
        majorConflicts = schedule.get_majorConflicts()
        minorConflicts = schedule.get_minorConflicts()
        conflictsDisplayData = []
        for conflict in majorConflicts + minorConflicts:
            # conflict could be that a faculty is not; or assigned less contact hours.
            if isinstance(conflict.aClass, Class):
                conflictsDisplayData.append(
                    [conflict.aClass.get_id(), conflict.aClass.get_course().get_name(),
                     conflict.aClass.get_faculty(), conflict.aClass.get_room().get_building(),
                     conflict.aClass.get_room().get_room(),
                     conflict.aClass.get_meetingTime().get_days(), conflict.aClass.get_meetingTime().get_time(),
                     conflict.aClass.get_meetingTime().get_duration(), conflict.type, conflict.conflictClass,
                     conflict.severity])
            else:
                conflictsDisplayData.append(
                    ['N/A', 'N/A',
                     conflict.aClass.get_name(), 'N/A',
                     'N/A', 'N/A',
                     'N/A', 'N/A', conflict.type, conflict.conflictClass,
                     conflict.severity])
        return conflictsDisplayData

    # Function for writing to excel file
    # Used: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html

    def writeSchedule(self, schedule):
        try:
            schedule_df = pd.DataFrame(self.get_scheduleDisplayData(schedule), columns=self.schedule_columns)
            conflicts_df = pd.DataFrame(self.get_conflictsDisplayData(schedule), columns=self.conflicts_columns)

            with pd.ExcelWriter('schedule.xlsx') as writer:
                schedule_df.to_excel(writer, sheet_name='Schedule', index=False)
                conflicts_df.to_excel(writer, sheet_name='Conflicts', index=False)
        except Exception as ex:
            print("Something went wrong, please check ...\n")
            print(ex)

    def writeAllData(self, schedule):
        try:
            courses_df = pd.DataFrame(self.get_coursesDisplayData(), columns=self.course_columns)
            classrooms_df = pd.DataFrame(self.get_classroomsDisplayData(), columns=self.classroom_columns)
            meetingtimes_df = pd.DataFrame(self.get_meetingtimesDisplayData(), columns=self.meeting_times_columns)

            schedule_df = pd.DataFrame(self.get_scheduleDisplayData(schedule), columns=self.schedule_columns)
            conflicts_df = pd.DataFrame(self.get_conflictsDisplayData(schedule), columns=self.conflicts_columns)

            with pd.ExcelWriter('output.xlsx') as writer:
                courses_df.to_excel(writer, sheet_name='Courses', index=False)
                classrooms_df.to_excel(writer, sheet_name='Classrooms', index=False)
                meetingtimes_df.to_excel(writer, sheet_name='Meetingtimes', index=False)
                schedule_df.to_excel(writer, sheet_name='Schedule', index=False)
                conflicts_df.to_excel(writer, sheet_name='Conflicts', index=False)
        except Exception as ex:
            print("Something went wrong, please check ...\n")
            print(ex)

    # Functions for displaying to the console
    def print_available_data(self, schedule):
        print("> All Available Data")
        self.print_courses()
        self.print_classrooms()
        self.print_meeting_times()
        self.print_schedule(schedule)

    def print_courses(self):
        coursesTable = prettytable.PrettyTable(self.course_columns)
        courses = self.get_coursesDisplayData()
        for course in courses:
            coursesTable.add_row(course)
        print(coursesTable)

    def print_classrooms(self):
        classroomsTable = prettytable.PrettyTable(self.classroom_columns)
        classrooms = self.get_classroomsDisplayData()
        for classroom in classrooms:
            classroomsTable.add_row(classroom)
        print(classroomsTable)

    def print_meeting_times(self):
        meetingTimesTable = prettytable.PrettyTable(self.meeting_times_columns)
        meetingTimes = self.get_meetingtimesDisplayData()
        for meetingtime in meetingTimes:
            meetingTimesTable.add_row(meetingtime)
        print(meetingTimesTable)

    def print_schedule(self, schedule):
        classes = self.get_scheduleDisplayData(schedule)
        table = prettytable.PrettyTable(self.schedule_columns)
        for aclass in classes:
            table.add_row(aclass)
        print(table)

    def print_conflicts(self, schedule):
        conflicts = self.get_conflictsDisplayData(schedule)
        table = prettytable.PrettyTable(self.conflicts_columns)
        for conflict in conflicts:
            table.add_row(conflict)
        print(table)

