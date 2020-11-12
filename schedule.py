import random as rnd

from classclass import Class
from config import Config
from conflict import Conflict


class Schedule:
    def __init__(self):
        self._data = Config.getInstance().get_data()
        self._classes = []
        self._numberOfMajorConflicts = 0  # Serious conflicts that NEED to be fixed
        self._numberOfMinorConflicts = 0  # Nice to have less of these but not necessary
        self._fitness = -1
        self._classNum = 0
        self._isFitnessChanged = True
        self._majorConflicts = []  # these two lists will record all conflicts
        self._minorConflicts = []


    def initialize(self):
        courses = self._data.get_courses()

        # need to keep track of faculties with no restriction
        faculty_with_no_restrictions_dict = {}
        for course in courses:
            new_class = Class(self._classNum, course)
            self._classNum += 1
            random_meeting_time = self._data.get_meetingTimes(pattern=course.get_meetingPattern(), random=True)
            if random_meeting_time:
                new_class.set_meetingTime(random_meeting_time)
            else:
                print("MeetingTime pattern not found.. please check")
                print("Course = " + course.get_name())

            random_classroom = self._data.get_classrooms(room_in=course.get_roomIn(), random=True)
            if random_classroom:
                new_class.set_room(random_classroom)
            else:
                print("Classroom not found.. please check")
                print("Course = " + course.get_name())

            # random faculty will be picked based off random meeting time as well to minimize conflicts
            random_faculty, faculty_with_no_restrictions_dict = self._data.get_faculties(course=course, meeting_time=random_meeting_time,
                                                                                         faculty_with_no_restrictions_dict=faculty_with_no_restrictions_dict,
                                                                                         random=True)
            new_class.set_faculty(random_faculty)
            # else:
            #     print("Faculty not found.. please check")
            #     print("Course = " + course.get_name())

            self._classes.append(new_class)
        return self

    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes

    def get_majorConflicts(self):
        return self._majorConflicts

    def get_minorConflicts(self):
        return self._minorConflicts

    def get_numberofMajorConflicts(self):
        return self._numberOfMajorConflicts

    def get_numberofMinorConflicts(self):
        return self._numberOfMinorConflicts

    def set_fitness(self):
        if self._isFitnessChanged:
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False

    def get_fitness(self):
        return self._fitness

    def calculate_fitness(self):
        self._majorConflicts = []  # reset them in case calculate_fitness is called again
        self._minorConflicts = []
        self._numberOfMajorConflicts = 0
        self._numberOfMinorConflicts = 0
        classes = self.get_classes()
        faculty_contact_hours_dict = {}  # will track each faculty contact hours as we traverse through schedule

        for i, aClass in enumerate(classes):
            classroom = aClass.get_room()
            course = aClass.get_course()
            section_overlap_counter = 0

            # check and increment contact hours
            faculty = aClass.get_faculty()
            if faculty != "Staff":
                faculty_contact_hours = faculty.get_contact_hours()
                course_contact_hours = aClass.get_course().get_numContactHrs()
                if faculty not in faculty_contact_hours_dict:
                    faculty_contact_hours_dict[faculty] = 0
                faculty_contact_hours_dict[faculty] += course_contact_hours
                if faculty_contact_hours_dict[faculty] > faculty_contact_hours:
                    self._numberOfMajorConflicts += 1
                    self._majorConflicts.append(Conflict(aClass, "Faculty exceeds contact hours, current: {}, required: {}".format(
                        faculty_contact_hours_dict[faculty], faculty_contact_hours)))

                # Check availability conflict
                faculty_availability = faculty.get_availability()
                if "NO" not in faculty_availability.upper():
                    days_check = False
                    meeting_time_check = False
                    if self._data.check_matching_days(faculty_availability.split(":", 1)[0], aClass.get_meetingTime().get_days()):
                        days_check = True
                        if days_check:
                            if self._data.check_meeting_time_overlap(faculty_availability.split(":", 1)[1], aClass.get_meetingTime().get_time()):
                                meeting_time_check = True
                    if not days_check or not meeting_time_check:
                        self._numberOfMinorConflicts += 1
                        self._minorConflicts.append(Conflict(aClass, "Does not fit in faculty's available time, {}".format(faculty_availability), False))


            # check seating capacity
            if classroom.get_seatingCapacity() < course.get_maxNumOfStudents():
                self._numberOfMajorConflicts += 1
                self._majorConflicts.append(Conflict(aClass, "Insufficient room capacity"))

            # compare with all the following classes in the classes list, ignore previously considered classes
            for j, anotherClass in enumerate(classes):
                if j > i:
                    # check the following conditions if two classes are on the same meeting times
                    if aClass.get_meetingTime() == anotherClass.get_meetingTime():

                        # cannot be taught by same faculty
                        if faculty != "Staff":
                            if faculty == anotherClass.get_faculty():
                                self._numberOfMajorConflicts +=1
                                self._majorConflicts.append(Conflict(aClass, "Cannot teach two classes at same time", str(anotherClass)))

                        # cannot be held in the same room
                        if aClass.get_room() == anotherClass.get_room():
                            self._numberOfMajorConflicts += 1
                            self._majorConflicts.append(Conflict(aClass, "Scheduled on same room", str(anotherClass)))

                        # a class should not be scheduled on the same time as co-reqs
                        if anotherClass.get_course().get_name().split('_')[0] in aClass.get_course().get_coreqs():
                            self._numberOfMinorConflicts += 1
                            self._minorConflicts.append(Conflict(aClass, "Concurrent with Co-req", str(anotherClass), False))

                        # a class should not be scheduled on the same time as potential conflicts
                        if anotherClass.get_course().get_name().split('_')[
                            0] in aClass.get_course().get_potentialConflicts():
                            self._numberOfMinorConflicts += 1
                            self._minorConflicts.append(Conflict(aClass, "Concurrent with potential conflict", str(anotherClass), False))

                        # handle multiple section
                        if aClass.get_course().get_num_of_sections() > 1 and self._are_both_course_sections(aClass,
                                                                                                            anotherClass):
                            section_overlap_counter += 1
                            if section_overlap_counter > aClass.get_course().get_concurrency__max():
                                self._numberOfMinorConflicts += 1
                                self._minorConflicts.append(
                                    Conflict(aClass, "Concurrent with too many sections", str(anotherClass), False))

        return 1 / (1.0 * self._numberOfMajorConflicts + 1)

    def _are_both_course_sections(self, aClass, bClass):
        """checks if two classes are sections of the same course"""
        if '_' in aClass.get_course().get_name() and '_' in bClass.get_course().get_name():
            if aClass.get_course().get_name().split('_')[0] == bClass.get_course().get_name().split("_")[0]:
                return True
        return False

    def __str__(self):
        returnValue = ""
        for aClass in self._classes:
            returnValue += str(aClass) + ', '
        returnValue = returnValue[:-2]

        return returnValue