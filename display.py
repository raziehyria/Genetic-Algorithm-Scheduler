import prettytable
from cs.config import Config


class DisplayMgr:

    def __init__(self):
        self.data = Config.getInstance().get_data()

    def print_available_data(self):
        print("> All Available Data")
        self.print_dept()
        self.print_course()
        self.print_room()
        self.print_instructor()
        self.print_meeting_times()

    def print_dept(self):
        depts = self.data.get_depts()
        availableDeptsTable = prettytable.PrettyTable(["dept", "courses"])
        for i in range(0, len(depts)):
            courses = depts.__getitem__(i).get_courses()
            tempStr = "["
            for j in range(0, len(courses) - 1):
                tempStr += courses[j].__str__() + ", "
            tempStr += courses[len(courses) - 1].__str__() + "]"
            availableDeptsTable.add_row([depts.__getitem__(i).get_name(), tempStr])
        print(availableDeptsTable)

    def print_course(self):
        availableCoursesTable = prettytable.PrettyTable(["id", "course #", "max # of students", "instructors"])
        courses = self.data.get_courses()
        for i in range(0, len(courses)):
            instructors = courses[i].get_instructors()
            tempStr = ""
            for j in range(0, len(instructors) - 1):
                tempStr += instructors[j].__str__() + ", "
            tempStr += instructors[len(instructors) - 1].__str__()
            availableCoursesTable.add_row(
                [courses[i].get_number(), courses[i].get_name(), str(courses[i].get_maxNumOfStudents()), tempStr])
        print(availableCoursesTable)

    def print_instructor(self):
        availableInstructorsTable = prettytable.PrettyTable(["id", "instructor"])
        instructors = self.data.get_instructors()
        for i in range(0, len(instructors)):
            availableInstructorsTable.add_row([instructors[i].get_id(), instructors[i].get_name()])
        print(availableInstructorsTable)

    def print_room(self):
        availableRoomsTable = prettytable.PrettyTable(["room #", "max seating capacity"])
        rooms = self.data.get_rooms()
        for i in range(0, len(rooms)):
            availableRoomsTable.add_row([str(rooms[i].get_number()), str(rooms[i].get_seatingCapacity())])
        print(availableRoomsTable)

    def print_meeting_times(self):
        availableMeetingTimeTable = prettytable.PrettyTable(["rid", "Meeting Time"])
        meetingTimes = self.data.get_meetingTimes()
        for i in range(0, len(meetingTimes)):
            availableMeetingTimeTable.add_row([meetingTimes[i].get_id(), meetingTimes[i].get_time()])
        print(availableMeetingTimeTable)

    def print_generation(self,
                         population):  # some parts of this function could be missing, some of the code cut off in the video
        table1 = prettytable.PrettyTable(
            ["schedule #", "fitness", "# of conflicts", "classes [dept,class,room instructor]"])
        schedules = population.get_schedules()
        for i in range(0, len(schedules)):
            table1.add_row(
                [str(i), round(schedules[i].get_fitness(), 3), schedules[i].get_numberofConflicts(), schedules[i]])
        print(table1)

    def print_schedules_as_table(self,
                                 schedule):  # some parts of this function could be missing, some of the code cut off in the video
        classes = schedule.get_classes()
        table = prettytable.PrettyTable(
            ["Class #", "Dept", "Course (number, max # of students)", "Room (Capacity, Instructor name, id)",
             "Meeting Time (id)"])
        for i in range(0, len(classes)):
            table.add_row([str(i), classes[i].get_dept().get_name(), classes[i].get_course().get_name() + " (" +
                           classes[i].get_course().get_number() + ", " +
                           str(classes[i].get_course().get_maxNumOfStudents()) + ")",
                           classes[i].get_room().get_number() + " (" + str(
                               classes[i].get_room().get_seatingCapacity()) + ", " +
                           classes[i].get_instructor().get_name() + ", " + str(
                               classes[i].get_instructor().get_id()) + ")",
                           classes[i].get_meetingTime().get_time() + " (" + str(
                               classes[i].get_meetingTime().get_id()) + ")"])
        print(table)
