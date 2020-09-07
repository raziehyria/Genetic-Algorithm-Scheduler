import random as rnd

POPULATION_SIZE = 9

class Data:

    ROOMS = [['R2', 25], ['R2', 45], ['R3', 35]]
    MEETING_TIMES = [
        ["MT1", 'MWF 9 - 10'],
        ['MT2', 'MWF 10 - 11'],
        ['MT3', 'TTH 9 - 10:30'],
        ['MT4', 'TTH 10:30 - 12:00']
    ]

    INSTRUCTORS = [
        ['I1', "Dr. Vinayak Elangovan"],
        ['I2', 'Dr. Ishtiaque Hussain'],
        ['I3', 'Dr. Gokhan Ozden'],
        ['I4', 'Dr. Yi Yang']
    ]

    def __init__(self):
        self._rooms = []
        self._meetingTimes = []
        self._instructors = []

        for room in self.ROOMS:
            self._rooms.append(Room(room[0], room[1]))
        for meetingTime in self.MEETING_TIMES:
            self._meetingTimes.append(MeetingTime(meetingTime[0], meetingTime[1]))
        for instructor in self.INSTRUCTORS:
            self._instructors.append(instructor)

        course1 = Course('C1', 'CMPSC 131', [self._instructors[0], self._instructors[1]], 25)
        course2 = Course('C2', 'CMPSC 132', [self._instructors[0], self._instructors[1]], 25)
        course3 = Course('C3', 'CMPENG 144',[self._instructors[2], self._instructors[3]], 35)
        course4 = Course('C4', 'CMPSC 360', [self._instructors[1], self._instructors[2]], 30)
        course5 = Course('C5', 'MATH 144', [self._instructors[2], self._instructors[3]], 25)
        course6 = Course('C6', 'MATH 121', [self._instructors[2]], 25)
        course7 = Course('C7', 'PHY 112', [self._instructors[3]], 35)
        course8 = Course('C8', 'PHY 144', [self._instructors[2], self._instructors[3]], 30)

        self._courses = [course1, course2, course3, course4, course5, course6, course7, course8]

        dept1 = Department("CMPSC", [course1, course2, course3, course4])
        dept2 = Department('MATH', [course5, course6])
        dept3 = Department('PHY', [course7, course8])

        self._depts = [dept1, dept2, dept3]

        self._numberOfClasses = 0
        for dept in self._depts:
            self._numberOfClasses += len(dept.get_courses())

    def get_rooms(self): return self._rooms
    def get_instructors(self): return self._instructors
    def get_courses(self): return self._courses
    def get_depts(self): return self._depts
    def get_meetingTimes(self): return self._meetingTimes
    def get_numberOfClasses(self): return self._numberOfClasses


class Schedule:
    def __init__(self):
        self._data = data
        self._classes = []
        self._numberOfConflicts = 0
        self._fitness = -1
        self._classNum = 0
        self._isFitnessChanged = True

    def initialize(self):
        depts = self._data.get_depts()
        for dept in depts:
            for course in dept.get_courses():
                newClass = Class(self._classNum, dept, course)
                self._classNum += 1
                newClass.set_meetingTime(data.get_meetingTimes()[rnd.randrange(len(data.get_meetingTimes()))])
                newClass.set_room(data.get_rooms()[rnd.randrange(len(data.get_rooms()))])
                newClass.set_instructor(course.get_instructors()[rnd.randrange(len(course.get_instructors()))])


                self._classes.append(newClass)

        return self

    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes

    def get_numberofConflicts(self):
        return self._numberOfConflicts

    def get_fitness(self):
        if self._isFitnessChanged:
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness


    def calculate_fitness(self):
        self._numberOfConflicts = 0
        classes = self.get_classes()

        for i, aClass in enumerate(classes):
            if aClass.get_room().get_seatingCapacity() < aClass.get_course().get_maxNumOfStudents():
                self._numberOfConflicts += 1

            # compare with all the following classes in the classes list, ignore previously considered classes
            for j, anotherClass in enumerate(classes):
                if j > i:
                    if aClass.get_meetingTime() == anotherClass.get_meetingTime:
                        if aClass.get_room() == anotherClass.get_room():
                            self._numberOfConflicts += 1
                        if aClass.get_instructor() == anotherClass.get_instructor():
                            self._numberOfConflicts += 1

        return 1 / (self._numberOfConflicts + 1)

    def __str__(self):
        returnValue = ""
        for aClass in self._classes:
            returnValue += str(aClass) + ', '
        returnValue = returnValue[:-2]

        return returnValue


class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = []
        for _ in range(size):
            self._schedules.append(Schedule().initialize())

    def get_schedules(self):
        return self._schedules

class GeneticAlgorithm:
    """"""

class Course:
    """"""
    def __init__(self, number, name, insturctors, maxNumOfStudents):
        self._number = number
        self._name = name
        self._instructors = insturctors
        self._maxNumOfStudents = maxNumOfStudents

    def get_number(self): return self._number
    def get_name(self): return self._name
    def get_instructors(self): return self._instructors
    def get_maxNumOfStudents(self): return self._maxNumOfStudents
    def __str__(self): return self._name


class Instructor:
    """"""
    def __init__(self, id, name):
        self._id = id
        self._name = name

    def get_id(self): return self._id
    def get_name(self): return self._name
    def __str__(self): return self._name


class Room:
    """"""
    def __init__(self, number, seatingCapacity):
        self._number = number
        self._seatingCapacity = seatingCapacity

    def get_seatingCapacity(self): return self._seatingCapacity


class MeetingTime:
    """"""
    def __init__(self, id, time):
        self._id = id
        self._time = time

    def get_id(self): return self._id
    def get_time(self): return self._time


class Department:
    """"""
    def __init__(self, name, courses):
        self._name = name
        self._courses = courses

    def get_name(self): return self._name
    def get_courses(self): return self._courses


class Class:
    """"""
    def __init__(self, id, dept, course):
        self._id = id
        self._dept = dept
        self._course = course
        self._instructor = None
        self._meetingTime = None
        self._room = None

    def get_id(self): return self._id
    def get_dept(self): return self._dept
    def get_course(self): return self._course
    def get_instructor(self): return self._instructor
    def get_meetingTime(self): return self._meetingTime
    def get_room(self): return self._room
    def set_instructor(self, instructor): self._instructor = instructor
    def set_meetingTime(self, meetingTime): self._meetingTime = meetingTime
    def set_room(self, room): self._room = room
    def __str__(self):
        return str(self._dept.get_name()) + ", " + str(self._course.get_number()) + "," +  \
            str(self._room.get_number()) + ", " + str(self._instructor.get_id()) + ", " + \
            str(self._meetingTime.get_id())


data = Data()
population = Population(POPULATION_SIZE)
population.get_schedules().sort(key=lambda  x: x.get_fitness(), reverse=True)
print(population)