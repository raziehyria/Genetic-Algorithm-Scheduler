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

        # reset dictionary to start fresh
        self._data.reset_faculty_assigned_hours_dict()

        for course in courses:
            new_class = Class(self._classNum, course)
            self._classNum += 1
            random_meeting_time = self._data.get_meetingTimes(pattern=course.get_meetingPattern(), random=True)
            if random_meeting_time:
                new_class.set_meetingTime(random_meeting_time)
            else:
                print("MeetingTime pattern not found.. please check")
                print("Course = " + course.get_name())
                raise Exception()

            random_classroom = self._data.get_classrooms(room_in=course.get_roomIn(), random=True)
            if random_classroom:
                new_class.set_room(random_classroom)
            else:
                print("Classroom not found.. please check")
                print("Course = " + course.get_name())
                raise Exception()

            # random faculty will be picked based off random meeting time as well to minimize conflicts
            random_faculty = self._data.get_faculties(target_class=new_class, random=True)
            if random_faculty:
                new_class.set_faculty(random_faculty)
                # keep track of how many contact hours are assigned to a particular faculty
                self._data.update_faculty_assigned_hours_dict(random_faculty,
                                                              new_class.get_course().get_numContactHrs())
            else:
                print('No faculty found to teach the course, please check ...')
                print("Course = " + course.get_name())
                raise Exception()

            # finally add the new class
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
        faculty_assigned_hours_dict = {}  # will track each faculty contact hours as we traverse through schedule

        for i, aClass in enumerate(classes):
            classroom = aClass.get_room()
            course = aClass.get_course()
            section_overlap_counter = 0

            # check and increment contact hours
            faculty = aClass.get_faculty()
            if faculty.get_name() != "Staff":
                faculty_contact_hours = faculty.get_contact_hours()
                course_contact_hours = aClass.get_course().get_numContactHrs()

                faculty_assigned_hours_dict.setdefault(faculty, 0)
                faculty_assigned_hours_dict[faculty] += course_contact_hours

                # check if faculty is assigned more hours than their contract hours
                if faculty_assigned_hours_dict[faculty] > faculty_contact_hours:
                    self._numberOfMajorConflicts += 1
                    self._majorConflicts.append(
                        Conflict(aClass, "Faculty exceeds contact hours, current: {}, required: {}".format(
                            faculty_assigned_hours_dict[faculty], faculty_contact_hours)))

                # Check availability conflict
                if not self._is_faculty_available_for_the_class(faculty, aClass):
                    self._numberOfMinorConflicts += 1
                    self._minorConflicts.append(Conflict(aClass, "Does not fit in faculty's available time, {}".format(
                        faculty.get_availability()), majorConflict=False))

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
                        if faculty.get_name() != "Staff":
                            if faculty == anotherClass.get_faculty():
                                self._numberOfMajorConflicts += 1
                                self._majorConflicts.append(
                                    Conflict(aClass, "Cannot teach two classes at same time", str(anotherClass)))

                        # cannot be held in the same room
                        if aClass.get_room() == anotherClass.get_room():
                            self._numberOfMajorConflicts += 1
                            self._majorConflicts.append(Conflict(aClass, "Scheduled on same room", str(anotherClass)))

                        # a class should not be scheduled on the same time as co-reqs
                        if anotherClass.get_course().get_name().split('_')[0] in aClass.get_course().get_coreqs():
                            self._numberOfMinorConflicts += 1
                            self._minorConflicts.append(
                                Conflict(aClass, "Concurrent with Co-req", str(anotherClass), False))

                        # a class should not be scheduled on the same time as potential conflicts
                        if anotherClass.get_course().get_name().split('_')[
                            0] in aClass.get_course().get_potentialConflicts():
                            self._numberOfMinorConflicts += 1
                            self._minorConflicts.append(
                                Conflict(aClass, "Concurrent with potential conflict", str(anotherClass), False))

                        # handle multiple section
                        if aClass.get_course().get_num_of_sections() > 1 and self._are_both_course_sections(aClass,
                                                                                                            anotherClass):
                            section_overlap_counter += 1
                            if section_overlap_counter > aClass.get_course().get_concurrency__max():
                                self._numberOfMinorConflicts += 1
                                self._minorConflicts.append(
                                    Conflict(aClass, "Concurrent with too many sections", str(anotherClass), False))

        # Let's check for under-utilized faculty members:
        faculty_members = self._data.get_faculties()
        for faculty in faculty_members:
            # faculty is not assigned any courses!
            if faculty not in faculty_assigned_hours_dict and faculty.get_name() is not 'Staff':
                self._numberOfMajorConflicts += 1
                self._majorConflicts.append(
                    # Hacking: sending in the faculty instance to be able to print his/her name
                    Conflict(faculty, "No class assigned to {} - unused contact hours: {}".format(faculty.get_name(),
                                                                                                  faculty.get_contact_hours())))
            # faculty is assigned less hours than required contact hours
            elif faculty in faculty_assigned_hours_dict and faculty.get_name() is not 'Staff':
                if faculty_assigned_hours_dict[faculty] < faculty.get_contact_hours():
                    self._numberOfMajorConflicts += 1
                    self._majorConflicts.append(
                        # Hacking: sending in the faculty instance to be able to print his/her name
                        Conflict(faculty,
                                 "Unused contact hours: {} - current: {}, required: {}".format(faculty.get_name(),
                                                                                               faculty_assigned_hours_dict[
                                                                                                   faculty],
                                                                                               faculty.get_contact_hours())))


        return 1 / (1.0 * self._numberOfMajorConflicts + 0.5 * self._numberOfMinorConflicts + 1)

    def _are_both_course_sections(self, aClass, bClass):
        """checks if two classes are sections of the same course"""
        if '_' in aClass.get_course().get_name() and '_' in bClass.get_course().get_name():
            if aClass.get_course().get_name().split('_')[0] == bClass.get_course().get_name().split("_")[0]:
                return True
        return False

    def _is_faculty_available_for_the_class(self, faculty, target_class):
        is_available = False
        # check for 'No' in 'No restriction'
        if "NO" in faculty.get_availability().upper():
            is_available = True
        else:
            faculty_available_days = faculty.get_availability().split(":", 1)[0]
            faculty_available_times = faculty.get_availability().split(":", 1)[1]

            # if faculty is available only if both days and meeting times match class days and times
            if self._data.check_days_overlap(faculty_available_days, target_class.get_meetingTime().get_days()) \
                    and self._data.check_meeting_time_overlap(faculty_available_times,
                                                              target_class.get_meetingTime().get_time()):
                is_available = True

        return is_available

    def __str__(self):
        return_value = ""
        for aClass in self._classes:
            return_value += str(aClass) + ', '
        return_value = return_value[:-2]

        return return_value
