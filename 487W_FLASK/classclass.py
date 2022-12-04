class Class:
    """Represents the combination of all data structures into a single class object which is makes up a schedule"""

    def __init__(self, id, course):
        self._id = id
        self._course = course
        self._meetingTime = None
        self._room = None
        self._faculty = None

    def get_id(self): return self._id

    def get_course(self): return self._course

    def get_meetingTime(self): return self._meetingTime

    def get_room(self): return self._room

    def get_faculty(self): return self._faculty

    def set_faculty(self, faculty): self._faculty = faculty

    def set_meetingTime(self, meetingTime): self._meetingTime = meetingTime

    def set_room(self, room): self._room = room

    def __str__(self):
        return str(self._course.get_name()) + ", " + \
               str(self._faculty.get_name()) + ", " + \
               str(self._room) + ", " + \
               str(self._meetingTime.get_meetingTime())
