class Class:
    """"""

    def __init__(self, id, course):
        self._id = id
        self._course = course
        self._meetingTime = None
        self._room = None

    def get_id(self): return self._id

    def get_course(self): return self._course

    def get_meetingTime(self): return self._meetingTime

    def get_room(self): return self._room

    def set_meetingTime(self, meetingTime): self._meetingTime = meetingTime

    def set_room(self, room): self._room = room

    def __str__(self):
        return str(self._course.get_name()) + ", " + \
               str(self._room) + ", " + \
               str(self._meetingTime.get_meetingTime())
