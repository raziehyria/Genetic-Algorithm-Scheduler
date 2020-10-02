import prettytable
from config import Config
import pandas as pd


class DisplayMgr:

    def __init__(self):
        self.data = Config.getInstance().get_data()

    def get_coursesDisplayData(self):

        courses = self.data.get_courses()
        coursesDisplayData = []
        for i in range(0, len(courses)):
            coursesDisplayData.append(
                [courses[i].get_subject(), courses[i].get_number(), courses[i].get_description(),
                 courses[i].get_meetingPattern(),
                 courses[i].get_maxNumOfStudents(), courses[i].get_prerequisites(), courses[i].get_coreqs(),
                 courses[i].get_potentialConflicts(),
                 courses[i].get_mutuallyExclusives(), courses[i].get_roomIn(), courses[i].get_num_of_sections(),
                 courses[i].get_concurrency__max()])
        return coursesDisplayData

    def get_classroomsDisplayData(self):

        classrooms = self.data.get_classrooms()
        classroomsDisplayData = []
        for i in range(0, len(classrooms)):
            classroomsDisplayData.append([str(classrooms[i].get_building()), str(classrooms[i].get_room()),
                                          str(classrooms[i].get_seatingCapacity()), str(classrooms[i].get_type())])
        return classroomsDisplayData

    def get_meetingtimesDisplayData(self):

        meetingTimes = self.data.get_meetingTimes()
        meetingTimesDisplayData = []
        for i in range(0, len(meetingTimes)):
            meetingTimesDisplayData.append(
                [meetingTimes[i].get_days(), meetingTimes[i].get_duration(), meetingTimes[i].get_time()])
        return meetingTimesDisplayData

    def get_scheduleDisplayData(self, schedule):
        classes = schedule.get_classes()
        scheduleDisplayData = []
        for i in range(0, len(classes)):
            scheduleDisplayData.append([classes[i].get_id(), classes[i].get_course().get_name(), classes[i].get_room(),
                                        classes[i].get_meetingTime()])
        return scheduleDisplayData

    # Function for writing to excel file
    # Used: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html

    def writeSchedule(self, schedule):
        schedule_df = pd.DataFrame(self.get_scheduleDisplayData(schedule),
                                   columns=[
                                       "Class id", "Course (Subject, Number, Section)", "Classroom (Building, Room)",
                                       "Meeting Time (Day(s), Time)"])
        with pd.ExcelWriter('schedule.xlsx') as writer:
            schedule_df.to_excel(writer, sheet_name='Schedule', index=False)

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

        with pd.ExcelWriter('output.xlsx') as writer:
            courses_df.to_excel(writer, sheet_name='Courses', index=False)
            classrooms_df.to_excel(writer, sheet_name='Classrooms', index=False)
            meetingtimes_df.to_excel(writer, sheet_name='Meetingtimes', index=False)
            schedule_df.to_excel(writer, sheet_name='Schedule', index=False)

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

    def print_generation(self,
                         population):  # some parts of this function could be missing, some of the code cut off in the video
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
