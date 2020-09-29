import prettytable
from config import Config
from schedule import Schedule


class DisplayMgr:

    def __init__(self):
        self.data = Config.getInstance().get_data()

    def print_available_data(self, schedule):
        print("> All Available Data")
        self.print_course()
        self.print_classrooms()
        self.print_meeting_times()
        self.print_schedules_as_table(schedule)

    def print_course(self):
        coursesTable = prettytable.PrettyTable(
            ["subject", "number", "description", "meetingPattern", "maxNumOfStudents",
             "preReqs", "coReqs", "potentialConflicts", "mutuallyExclusives", "roomIn"
                , "# of sections", "# of concurrent sections"])
        courses = self.data.get_courses()
        for i in range(0, len(courses)):
            coursesTable.add_row(
                [courses[i].get_subject(), courses[i].get_number(), courses[i].get_description(),
                 courses[i].get_meetingPattern(),
                 courses[i].get_maxNumOfStudents(), courses[i].get_prerequisites(), courses[i].get_coreqs(),
                 courses[i].get_potentialConflicts(),
                 courses[i].get_mutuallyExclusives(), courses[i].get_roomIn(), courses[i].get_num_of_sections(),
                 courses[i].get_concurrency__max()])
        print(coursesTable)

    def print_classrooms(self):
        classroomsTable = prettytable.PrettyTable(["building", "room", "seatingCapacity", "roomType"])
        classrooms = self.data.get_classrooms()
        for i in range(0, len(classrooms)):
            classroomsTable.add_row([str(classrooms[i].get_building()), str(classrooms[i].get_room()),
                                     str(classrooms[i].get_seatingCapacity()), str(classrooms[i].get_type())])
        print(classroomsTable)

    def print_meeting_times(self):
        meetingTimesTable = prettytable.PrettyTable(["days", "duration", "time"])
        meetingTimes = self.data.get_meetingTimes()
        for i in range(0, len(meetingTimes)):
            meetingTimesTable.add_row(
                [meetingTimes[i].get_days(), meetingTimes[i].get_duration(), meetingTimes[i].get_time()])
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

    def print_schedules_as_table(self, schedule):
        classes = schedule.get_classes()
        table = prettytable.PrettyTable(
            ["Class #", "Course (Subject, Number, Section)", "Classroom (Building, Room)", "Meeting Time (Day(s), Time)"])
        for i in range(0, len(classes)):
            table.add_row([classes[i].get_id(), classes[i].get_course().get_name(), classes[i].get_room(),
                           classes[i].get_meetingTime()])
        print(table)
