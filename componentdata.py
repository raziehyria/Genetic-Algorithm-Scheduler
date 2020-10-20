from data.classroomdata import ClassroomData
from data.coursedata import CourseData
from data.meetingtimedata import MeetingTimeData
import sys


class Data:
    """
    This class handles creating all the components objects list:
    courses, classrooms, meeting times
    """

    def __init__(self, file_path):
        self._classrooms = []
        self._meetingTimes = []
        self._courses = []

        try:
            courses_data = CourseData(file_path)
            self._courses = courses_data.get_courses_objects_list()

            meeting_times_data = MeetingTimeData(file_path)
            self._meetingTimes = meeting_times_data.get_meeting_times_objects_list()

            classroom_data = ClassroomData(file_path)
            self._classrooms = classroom_data.get_classroom_objects_list()

        except FileNotFoundError:
            print("File not found, please ensure the full path with the file name is correct")
        except Exception:
            print("Something went wrong!")
        # finally:      # prevented ClassScheduling.py from running
        #     sys.exit()



    def get_classrooms(self):
        return self._classrooms

    def get_courses(self):
        return self._courses

    def get_meetingTimes(self):
        return self._meetingTimes

