import random as rnd
import sys
from datetime import datetime

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
        self._faculty_assigned_hours_dict = {}
        self._faculty_availability_meetingtime_overlap_dict = {}

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
            if faculty.get_name() is 'Staff':
                continue
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

    def get_faculties(self, target_class=None, random=False):
        output = self._faculties
        if target_class:
            course = target_class.get_course()
            course_name = course.get_name().split('_')[0]  # using just the course name without section number for input
            if (self._courses_faculties_dict.get(course_name)) is None:  # no faculty listed for that class
                return self._faculties[-1]  # get the 'Staff' faculty
            else:
                eligible_faculties = self._courses_faculties_dict.get(course_name)
                eligible_faculties = self._remove_faculties_hours_maxed_out(eligible_faculties)
                available_faculties = self._filter_based_on_availability(target_class, eligible_faculties)

                if len(available_faculties) == 0:
                    candidate_faculty = self._faculties[-1]  # get the 'Staff' faculty
                else:
                    candidate_faculty = available_faculties[rnd.randrange(len(available_faculties))]

        return candidate_faculty if random else output

    def _filter_based_on_availability(self, target_class, faculty_members):
        available_faculties = []
        for faculty in faculty_members:
            faculty_availability = faculty.get_availability().upper()
            if 'NO' in faculty_availability:
                available_faculties.append(faculty)
            else:
                course_days = target_class.get_meetingTime().get_days()
                course_times = target_class.get_meetingTime().get_time()

                # if already checked this combination, lets re-use the prior finding
                key = "{} {} {}".format(faculty_availability, course_days, course_times).upper()
                if key in self._faculty_availability_meetingtime_overlap_dict:
                    if self._faculty_availability_meetingtime_overlap_dict[key]:
                        available_faculties.append(faculty)

                    continue  # to next faculty

                faculty_available_days = faculty_availability.split(":", 1)[0]
                faculty_available_times = faculty_availability.split(":", 1)[1]

                # if faculty is available only if both days and meeting times match class days and times
                if self.check_days_overlap(faculty_available_days, course_days) \
                        and self.check_meeting_time_overlap(faculty_available_times, course_times):
                    available_faculties.append(faculty)
                    # let's memoize seen overlap checks
                    self._faculty_availability_meetingtime_overlap_dict[key] = True
                else:
                    self._faculty_availability_meetingtime_overlap_dict[key] = False

        return available_faculties

    def _remove_faculties_hours_maxed_out(self, eligible_faculties):
        updated_list = []
        for faculty in eligible_faculties:
            # if faculty absent (i.e., not assigned any hours yet) or assigned less than contact hours
            if faculty not in self._faculty_assigned_hours_dict or \
                    self._faculty_assigned_hours_dict.get(faculty) < faculty.get_contact_hours():
                updated_list.append(faculty)

        return updated_list

    def check_days_overlap(self, available_days, required_days):
        is_overlapping = False
        available_days = available_days.upper()
        required_days = required_days.upper()
        # available_days = 'MWF or TR', 'MWF'
        if "OR" in available_days:  # e.g., 'MWF or TR'
            multiple_days_slots = [day.strip() for day in available_days.split("OR")]
            for each_days_slot in multiple_days_slots:
                if required_days in each_days_slot:
                    is_overlapping = True
                    break
        elif required_days in available_days:
            is_overlapping = True

        return is_overlapping

    def check_meeting_time_overlap(self, available_time, required_time):
        # available_time looks like: "10am - 5pm" or "9:30am - 4:30pm"
        # now becomes "10am" and "5pm", "9:30am" and "4:30pm"
        available_start_time, available_end_time = available_time.split("-")[0].strip(), available_time.split("-")[
            1].strip()
        # ex: 8:00 a and 8:50 a
        required_start_time, required_end_time = required_time.split("-")[0].strip(), required_time.split("-")[
            1].strip()
        # turning them to datetime object for easy comparisons

        available_start = self.get_datetime_object(available_start_time)
        available_end = self.get_datetime_object(available_end_time)
        required_start = self.get_datetime_object(required_start_time)
        required_end = self.get_datetime_object(required_end_time)

        if available_start <= required_start <= required_end <= available_end:
            return True
        else:
            return False

    def get_datetime_object(self, time_string):
        """checks type of input and returns a datetime object for time comparisons"""
        # ref https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
        time_string = time_string.lower()
        # add 'm' for am and pm if missing
        if 'm' not in time_string:
            time_string.replace('a', 'am')
            time_string.replace('p', 'pm')

        # replace space with empty string
        time_string = time_string.replace(' ', "")
        if ':' in time_string:
            return datetime.strptime(time_string, "%I:%M%p")
        else:
            return datetime.strptime(time_string, "%I%p")

    def update_faculty_assigned_hours_dict(self, faculty, contact_hours):
        self._faculty_assigned_hours_dict.setdefault(faculty, 0)
        self._faculty_assigned_hours_dict[faculty] += contact_hours

    def reset_faculty_assigned_hours_dict(self):
        self._faculty_assigned_hours_dict = {}
