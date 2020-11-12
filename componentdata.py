import random as rnd
import sys

from data.classroomdata import ClassroomData
from data.coursedata import CourseData
from data.facultydata import FacultyData
from data.meetingtimedata import MeetingTimeData
from datetime import datetime


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

    def get_faculties(self, course=None, meeting_time=None, faculty_with_no_restrictions_dict=None, random=False):
        output = self._faculties
        if course:
            course_name = course.get_name().split('_')[0]   # using just the course name without section number for input
            if (self._courses_faculties_dict.get(course_name)) == None:  # no faculty listed for that class
                return "Staff", faculty_with_no_restrictions_dict
            else:
                possible_faculties = list(self._courses_faculties_dict.get(course_name))
            while True:
                # impossible for anyone to fill this meeting time so we randomly pick one unlucky faculty member
                if not possible_faculties:
                    total_possible_faculties = self._courses_faculties_dict[course_name]
                    candidate_faculty = total_possible_faculties[rnd.randrange(len(total_possible_faculties))]
                    break

                candidate_faculty = possible_faculties[rnd.randrange(len(possible_faculties))]
                possible_faculties.remove(candidate_faculty)    # remove faculty from pool of faculties

                # ex: given MWF "12:20-1:10 p", check if fits faculty availability, "MWF: 10am - 5pm".
                faculty_availability = candidate_faculty.get_availability()
                available_day = faculty_availability.split(":")[0].strip()  # split at ":" and check if the days match
                if "NO" in available_day.upper() or available_day is None:  # faculty has no restrictions
                    if candidate_faculty not in faculty_with_no_restrictions_dict:
                        faculty_with_no_restrictions_dict[candidate_faculty] = 0
                    if faculty_with_no_restrictions_dict[candidate_faculty]+course.get_numContactHrs() > candidate_faculty.get_contact_hours():
                        continue
                    else:
                        faculty_with_no_restrictions_dict[candidate_faculty] += course.get_numContactHrs()
                        break
                if not self.check_matching_days(available_day, meeting_time.get_days()):
                    continue
                # the split removes the days from the faculty time, because input is MWF: 10am - 5pm or MWF: 9:30am - 4:30pm
                # only split at first ":" ex: MWF: 10:00am - 5pm
                if self.check_meeting_time_overlap(faculty_availability.split(":", 1)[1], meeting_time.get_time()):
                    break

        return candidate_faculty, faculty_with_no_restrictions_dict if random else output

    def check_matching_days(self, available_day, required_days):
        if "or" in available_day:   # not just a single day
            available_days = [day.strip() for day in available_day.split("or")]
            for available_day in available_days:
                if required_days == available_day:
                    return True
        elif available_day == required_days:
            return True
        else:
            return False

    def check_meeting_time_overlap(self, available_time, required_time):
        # available_time looks like: "10am - 5pm" or "9:30am - 4:30pm"
        # now becomes "10am" and "5pm", "9:30am" and "4:30pm"
        available_time_string_start, available_time_string_end = available_time.split("-")[0].strip(), \
                                                   available_time.split("-")[1].strip()
        required_time_string = required_time.split("-")  # ex: 8:00 a - 8:50 a
        # ex: 8:00 a and 8:50 a
        required_time_string_start, required_time_string_end = required_time_string[0].strip(), \
                                                                 required_time_string[1].strip()
        # turning them to datetime object for easy comparisons
        available_time_start = self.get_datetime_object(available_time_string_start)
        available_time_end = self.get_datetime_object(available_time_string_end)
        required_time_start = self.get_datetime_object(required_time_string_start)
        required_time_end = self.get_datetime_object(required_time_string_end)

        # available start has to be less than or equal required start
        # available end has to be greater than or equal to required end
        if available_time_start <= required_time_start and available_time_end >= required_time_end:
            return True
        else:
            return False

    def get_datetime_object(self, time_string):
        """checks type of input and returns a datetime object for time comparisons"""
        # ref https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
        if "am" in time_string or "pm" in time_string:  # only faculty time have am and pm suffix so they are expected in the form "5pm", "9:30am"
            if ":" in time_string:
                if " " in time_string:
                    return datetime.strptime(time_string, "%I:%M %p")
                else:
                    return datetime.strptime(time_string, "%I:%M%p")
            else: #doesn't have a ':' in it so it must be written as 3pm, 5pm, 9am etc
                if " " in time_string:  # some have a space like 5 pm
                    return datetime.strptime(time_string, "%I %p")
                else:
                    return datetime.strptime(time_string, "%I%p")
        else:   # all the required meeting times have this format so it has the p or a ending which needs to be pm or am
            return datetime.strptime(time_string + "m", "%I:%M %p")

