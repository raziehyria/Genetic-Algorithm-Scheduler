import random as rnd

from classclass import Class
from config import Config


class Schedule:
    def __init__(self):
        self._data = Config.getInstance().get_data()
        self._classes = []
        self._numberOfConflicts = 0
        self._fitness = -1
        self._classNum = 0
        self._isFitnessChanged = True

    def initialize(self):
        courses = self._data.get_courses()
        for course in courses:
            new_class = Class(self._classNum, course)
            self._classNum += 1
            counter = 0
            while counter < Config.getInstance().get_MAX_ITERATION():
                random_meeting_time = self._data.get_meetingTimes()[rnd.randrange(len(self._data.get_meetingTimes()))]
                if self._meeting_pattern_matched(course, random_meeting_time):
                    new_class.set_meetingTime(random_meeting_time)
                    break
                else:
                    counter += 1
                    if counter == Config.getInstance().get_MAX_ITERATION():
                        print("MeetingTime pattern not found.. please check")
                        print("Course = " + course.get_name())

            # reinitialize the counter
            counter = 0
            while counter < Config.getInstance().get_MAX_ITERATION():
                random_classroom = self._data.get_classrooms()[rnd.randrange(len(self._data.get_classrooms()))]
                if self._classroom_requirement_matched(course, random_classroom):
                    new_class.set_room(random_classroom)
                    break
                else:
                    counter += 1
                    if counter == Config.getInstance().get_MAX_ITERATION():
                        print("Classroom not found.. please check")
                        print("Course = " + course.get_name())

            self._classes.append(new_class)

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
            classroom = aClass.get_room()
            course = aClass.get_course()
            section_overlap_counter = 0

            # check seating capacity
            if classroom.get_seatingCapacity() < course.get_maxNumOfStudents():
                self._numberOfConflicts += 1

            # # check room in requirement
            # if len(course.get_roomIn()) != 0:
            #     if course.get_roomIn() != classroom.get_room():
            #         self._numberOfConflicts += 1

            # # check meeting pattern (e.g., 3X50')
            # if not self._meeting_pattern_matched(aClass):
            #     self._numberOfConflicts += 10

            # compare with all the following classes in the classes list, ignore previously considered classes
            for j, anotherClass in enumerate(classes):
                if j > i:
                    # check the following conditions if two classes are on the same meeting times
                    if aClass.get_meetingTime() == anotherClass.get_meetingTime():

                        # cannot be held in the same room
                        if aClass.get_room() == anotherClass.get_room():
                            self._numberOfConflicts += 5

                        # a class should not be scheduled on the same time as co-reqs
                        if anotherClass.get_course().get_name().split('_')[0] in aClass.get_course().get_coreqs():
                            self._numberOfConflicts += 1

                        # a class should not be scheduled on the same time as potential conflicts
                        if anotherClass.get_course().get_name().split('_')[
                            0] in aClass.get_course().get_potentialConflicts():
                            self._numberOfConflicts += 3

                        # handle multiple section
                        if aClass.get_course().get_num_of_sections() > 1 and self._are_both_course_sections(aClass,
                                                                                                            anotherClass):
                            section_overlap_counter += 1
                            if section_overlap_counter > aClass.get_course().get_concurrency__max():
                                self._numberOfConflicts += 2

        return 1 / (1.0 * self._numberOfConflicts + 1)

    def _are_both_course_sections(self, aClass, bClass):
        """checks if two classes are sections of the same course"""
        if '_' in aClass.get_course().get_name() and '_' in bClass.get_course().get_name():
            if aClass.get_course().get_name().split('_')[0] == bClass.get_course().get_name().split("_")[0]:
                return True

        return False

    def _meeting_pattern_matched(self, course, meeting_time):
        """Finds if a course matched its pattern with the assigned meeting times"""
        required_meeting_pattern = course.get_meetingPattern()
        assigned_meeting_pattern = str(len(meeting_time.get_days())) + 'X'
        if 'min' in meeting_time.get_duration():
            assigned_meeting_pattern += meeting_time.get_duration().split()[0]
        elif 'hr' in meeting_time.get_duration():
            assigned_meeting_pattern += str(int(meeting_time.get_duration().split('hr')[0]) * 60)


        if required_meeting_pattern is None: # TODO: fix
            return True

        return True if assigned_meeting_pattern in required_meeting_pattern else False

    def _classroom_requirement_matched(self, course, classroom):
        """Checks if a course is in its required room"""
        required_room = course.get_roomIn()
        # if no room specified (None or empty) it can hold in any room
        if required_room is None or len(required_room) == 0:
            return True

        room_assigned = classroom.get_building() + str(classroom.get_room())

        # required room could be just a type, e.g., PC LAB
        if required_room == room_assigned or required_room == classroom.get_type():
            return True
        else:
            False


    def __str__(self):
        returnValue = ""
        for aClass in self._classes:
            returnValue += str(aClass) + ', '
        returnValue = returnValue[:-2]

        return returnValue