from data.classroomdata import ClassroomData
from data.coursedata import CourseData
from data.meetingtimedata import MeetingTimeData
import sys
import random as rnd


class Data:
    """
    This class handles creating all the components objects list:
    courses, classrooms, meeting times
    """

    def __init__(self, file_path):
        self._classrooms = []
        self._meetingTimes = []
        self._courses = []

        # for faster look ups
        self._meetingTimes_dict = {}
        self._classrooms_dict = {}

        try:
            courses_data = CourseData(file_path)
            self._courses = courses_data.get_courses_objects_list()

            meeting_times_data = MeetingTimeData(file_path)
            self._meetingTimes = meeting_times_data.get_meeting_times_objects_list()
            self._populate_meetingTimes_dictionary()

            classroom_data = ClassroomData(file_path)
            self._classrooms = classroom_data.get_classroom_objects_list()
            self._populate_classrooms_dictionary()

        except FileNotFoundError:
            print("File not found, please ensure the full path with the file name is correct")
            sys.exit()
        except Exception:
            print("Something went wrong!")
            sys.exit()


    def _populate_meetingTimes_dictionary(self):
        """Populates meeting times dictionary: 'pattern' - list of matching meeting times object"""
        for meetingtime in self._meetingTimes:
            pattern = "{}X".format(len(meetingtime.get_days()))
            duration = meetingtime.get_duration()
            if 'min' in duration:
                pattern += duration.split()[0]
            elif 'hr' in duration:
                pattern += str(int(duration.split('hr')[0]) * 60)
            pattern = pattern + "'"  # adding the minute sign '
            pattern = pattern.upper()
            self._meetingTimes_dict.setdefault(pattern, [])
            value = self._meetingTimes_dict[pattern]
            value.append(meetingtime)

    def _populate_classrooms_dictionary(self):
        """Populates classrooms dictionary: 'room_in/type' - list of matching classrooms"""
        for classroom in self._classrooms:
            room_description = "{}{}".format(classroom.get_building(), classroom.get_room()).upper()
            room_type = classroom.get_type().upper()
            self._classrooms_dict.setdefault(room_description, [])
            self._classrooms_dict.setdefault(room_type, [])
            room_value = self._classrooms_dict[room_description]
            room_value.append(classroom)
            type_value = self._classrooms_dict[room_type]
            type_value.append(classroom)

    def get_classrooms(self, room_in=None, random=False):
        output = self._classrooms
        if room_in:
            room_in = room_in.upper().strip()
            output = self._classrooms_dict.get(room_in)

        return output[rnd.randrange(len(output))] if random else output

    def get_courses(self):
        return self._courses

    def get_meetingTimes(self, pattern=None, random=False):
        output = self._meetingTimes
        if pattern:
            pattern = pattern.upper()
            patterns = pattern.split('OR')
            output = []
            for p in patterns:
                p = p.strip()  # get rid of any extra space
                output += self._meetingTimes_dict.get(p)

        return output[rnd.randrange(len(output))] if random else output
