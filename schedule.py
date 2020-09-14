import random as rnd

from .classclass import Class
from .config import Config


class Schedule:
    def __init__(self):
        self._data = Config.getInstance().get_data()
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
                newClass.set_meetingTime(
                    self._data.get_meetingTimes()[rnd.randrange(len(self._data.get_meetingTimes()))])
                newClass.set_room(self._data.get_rooms()[rnd.randrange(len(self._data.get_rooms()))])
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

        return 1 / (1.0 * self._numberOfConflicts + 1)

    def __str__(self):
        returnValue = ""
        for aClass in self._classes:
            returnValue += str(aClass) + ', '
        returnValue = returnValue[:-2]

        return returnValue
