import random as rnd
import sys

from data.classroomdata import ClassroomData
from data.coursedata import CourseData
from data.facultydata import FacultyData
from data.meetingtimedata import MeetingTimeData


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
        self._meetingTimesPattern_days_dict = {}
        self._classroomType_rooms_dict = {}
        self._courses_faculties_dict = {}


        try:
            courses_data = CourseData(file_path)
            self._courses = courses_data.get_courses_objects_list()

            meeting_times_data = MeetingTimeData(file_path)
            self._meetingTimes = meeting_times_data.get_meeting_times_objects_list()
            self._populate_meetingTimesPattern_days_dictionary()

            classroom_data = ClassroomData(file_path)
            self._classrooms = classroom_data.get_classroom_objects_list()
            self._populate_classroomTypes_classrooms_dictionary()

            faculty_data = FacultyData(file_path)
            self._faculties = faculty_data.get_faculty()
            self._populate_course_faculties_dictionary()

        except FileNotFoundError:
            print("File not found, please ensure the full path with the file name is correct")
            sys.exit()
        except Exception as e:
            print("Something went wrong! Please check...")
            print(e)
            sys.exit()

    def _populate_meetingTimesPattern_days_dictionary(self):
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
            self._meetingTimesPattern_days_dict.setdefault(pattern, [])
            value = self._meetingTimesPattern_days_dict[pattern]
            value.append(meetingtime)

    def _populate_classroomTypes_classrooms_dictionary(self):
        """Populates classrooms dictionary: 'room_in/type' - list of matching classrooms"""
        for classroom in self._classrooms:
            room_description = "{}{}".format(classroom.get_building(), classroom.get_room()).upper()
            room_type = classroom.get_type().upper()
            self._classroomType_rooms_dict.setdefault(room_description, [])
            self._classroomType_rooms_dict.setdefault(room_type, [])
            room_value = self._classroomType_rooms_dict[room_description]
            room_value.append(classroom)
            type_value = self._classroomType_rooms_dict[room_type]
            type_value.append(classroom)

    def _populate_course_faculties_dictionary(self):
        """Populates a dictionary: each 'course' as key - list of faculties who can teach the course as values"""

        # all unique courses are not available in the Faculty Preference tab, need to get it from the courses list
        # course names can have sections, e.g., MATH140_001, MATH140_002, we need to consider just MATH140 prefix
        unique_courses = set([course.get_name().split('_')[0] for course in self._courses])
        for faculty in self._faculties:
            for course in faculty.get_courses():
                course = course.upper()
                #  faculty can have MATH1XX as his courses, get all courses that have MATH1 as prefix
                # some courses can have single X, e.g., BIOL16X, so the prefix can vary in length
                # find('X') gives us the index of first occurrence of 'X', course[:course.find('X')] gets the prefix
                if 'X' in course:
                    matching_courses = set([uc for uc in unique_courses if course[:course.find('X')] in uc])
                    for each_course in matching_courses:
                        self._courses_faculties_dict.setdefault(each_course,
                                                                [])  # we need setdefault for the first time
                        faculty_members = self._courses_faculties_dict.get(each_course)
                        faculty_members.append(faculty)
                else:
                    self._courses_faculties_dict.setdefault(course, [])
                    faculty_members = self._courses_faculties_dict.get(course)
                    faculty_members.append(faculty)
                    
    def get_classrooms(self, room_in=None, random=False):
        output = self._classrooms
        if room_in:
            room_in = room_in.upper().strip()
            output = self._classroomType_rooms_dict.get(room_in)

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
                output += self._meetingTimesPattern_days_dict.get(p)

        return output[rnd.randrange(len(output))] if random else output
