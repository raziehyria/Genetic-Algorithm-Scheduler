from data.classroomdata import ClassroomData
from data.coursedata import CourseData
from data.meetingtimedata import MeetingTimeData


class Data:
    """
    This class handles creating all the components objects list:
    courses, classrooms, meeting times
    """

    def __init__(self):
        self._classrooms = []
        self._meetingTimes = []
        self._courses = []

        courses_data = CourseData()
        self._courses = courses_data.get_courses_objects_list()

        meeting_times_data = MeetingTimeData()
        self._meetingTimes = meeting_times_data.get_meeting_times_objects_list()

        classroom_data = ClassroomData()
        self._classrooms = classroom_data.get_classroom_objects_list()



    def get_classrooms(self):
        return self._classrooms

    def get_courses(self):
        return self._courses

    def get_meetingTimes(self):
        return self._meetingTimes

