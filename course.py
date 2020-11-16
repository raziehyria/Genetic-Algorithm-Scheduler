class Course:
    """"""

    def __init__(self, subject, number, description, numContactHrs, meetingPattern, maxNumOfStudents,
                 preReqs, coReqs, potentialConflicts, mutuallyExclusives, roomIn, sections, concurrent_max):
        self._subject = subject
        self._number = number
        self._descr = description
        self._numContactHrs = numContactHrs
        self._meetingPattern = meetingPattern
        self._maxNumOfStudents = int(maxNumOfStudents)
        self._preReqs = preReqs
        self._coReqs = coReqs
        self._potentialConflicts = potentialConflicts
        self._mutuallyExclusives = mutuallyExclusives
        self._roomIn = roomIn
        self._sections = sections
        self._concurrent_max = concurrent_max

        self._name = subject + str(number)

    def get_subject(self): return self._subject

    def get_number(self): return self._number

    def get_description(self): return self._descr

    def get_meetingPattern(self): return self._meetingPattern

    def get_maxNumOfStudents(self): return self._maxNumOfStudents

    def get_coreqs(self): return self._coReqs

    def get_prerequisites(self): return self._preReqs

    def get_potentialConflicts(self): return self._potentialConflicts

    def get_mutuallyExclusives(self): return self._mutuallyExclusives

    def get_roomIn(self): return self._roomIn

    def get_name(self): return self._name

    def get_numContactHrs(self): return self._numContactHrs

    def set_numContactHrs(self, numContactHrs): self._numContactHrs = numContactHrs

    def set_coreqs(self, coreqs): self._coReqs = coreqs

    def set_prerequisites(self, prereqs): self._preReqs = prereqs

    def set_potentialConflicts(self, conflicts): self._potentialConflicts = conflicts

    def get_num_of_sections(self): return self._sections

    def get_concurrency__max(self): return self._concurrent_max

    def __str__(self):
        return ("Name: {}, Description: {}, Number of Contact hours: {}, Meeting Pattern: {}, "
                "Max number of students: {}, Prerequisites: {}. Coorequisites: {}, "
                "Potential Conflicts: {}, Mutually Exclusives: {}, Room in: {}, Sections: {},"
                "Concurrent Max: {}".format(self._name, self._descr, self._numContactHrs,
                                            self._meetingPattern, self._maxNumOfStudents,
                                            self._preReqs, self._coReqs, self._potentialConflicts,
                                            self._mutuallyExclusives, self._roomIn, self._sections,
                                            self._concurrent_max))
