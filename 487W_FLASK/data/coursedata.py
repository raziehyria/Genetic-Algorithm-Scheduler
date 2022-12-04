# https://www.journaldev.com/33335/python-excel-to-json-conversion#converting-excel-sheet-to-json-string-using-pandas-module
# issues: some classes are not listed, ex: CMPSC 221 does not exist in excel, so it does not register it as a coreq/prereq/conflct
# regex pattern breaks in some situations, works with current inputs though

import json
import re

import pandas

from course import Course


class CourseData():
    """
    This class handles the Course related data
    """
    def __init__(self, file_path):
        self._courses_objects_list = []
        self._courses_names_set = set()
        self._subject_level_dict = {}

        excel_data_df = pandas.read_excel(file_path, sheet_name='Courses')
        json_str = excel_data_df.to_json(orient='records')  # use this to read rows not columns
        data = json.loads(json_str)

        for row in data:
            self._courses_names_set.add("{}{}".format(row.get('Subject').strip().upper(), str(row.get('Num')).strip()))

        for course_row in data:

            subject = course_row.get('Subject').strip()
            num = str(course_row.get('Num')).strip()
            description = course_row.get('Descr')
            numContactHrs = course_row.get('# of Contact hours')
            meeting_pattern = course_row.get('Meeting pattern')
            capacity = course_row.get('Enr Cpcty')
            mutex = self._resolve_course_list(course_row.get('Mutually exclusive with'))
            room_in = course_row.get('Room in')
            num_of_sections = course_row.get('# of sections')
            concurrency_max = self._resolve_concurrencty_number(course_row.get("Concurrent OK?"), num_of_sections)

            pre_reqs = self._resolve_course_list(course_row.get('Pre-Req'))
            co_reqs = self._resolve_course_list(course_row.get('Co-Req'))
            potential_conflicts = self._resolve_course_list(course_row.get('Potential conflicts'))

            # remove self-reference from pre-reqs, co-reqs and potential_conflicts
            parent_course = subject + num
            if parent_course in pre_reqs: pre_reqs.remove(parent_course)
            if parent_course in co_reqs: co_reqs.remove(parent_course)
            if parent_course in potential_conflicts: potential_conflicts.remove(parent_course)

            if room_in is None: room_in = ""
            if int(num_of_sections) > 1:
                for section_no in range(1, int(num_of_sections) + 1):
                    prefix = '_00' if section_no < 10 else '_0'
                    self._courses_objects_list.append(Course(subject, num + prefix + str(section_no),
                                                             description, numContactHrs,
                                                             meeting_pattern, capacity, pre_reqs, co_reqs,
                                                             potential_conflicts, mutex, room_in,
                                                             num_of_sections, concurrency_max))

            else:
                self._courses_objects_list.append(Course(subject, num, description, numContactHrs, meeting_pattern, capacity, pre_reqs, co_reqs,
                                                     potential_conflicts, mutex, room_in, num_of_sections, concurrency_max))

    def _resolve_course_list(self, input_str):
        """
        This method parses the input string and returns the list of courses
        :param input_str:
        :return:
        """

        # if input_str is missing or 'None' or empty, simply return empty list
        if input_str is None or input_str == "None" or len(input_str) == 0: return []

        # converting the whole string into upper case for ease of processing
        input_str = input_str.upper().strip()

        # Match only single course, e.g., CMPSC132, CMPSC487W, MATH4, Ignore IST2XX
        # Single course can be 3-5 characters, followed by 1 - 3 numbers and then an optional letter
        if re.match(r"^[A-Z]{3,5}\d{1,3}[A-Z]?$", input_str):
            return [input_str]

        pattern = "[ORAND,\W]*(\w+)[ORAND,\W]*"
        possible_courses = re.findall(pattern, input_str)
        sub_course_no_list = []
        subject = ""

        # prepend Subject if missing
        # BIOL223, 224 => BIOL224
        for item in possible_courses:
            if re.match('^(\D+)', item): # \D = non-digit
                subject = re.findall('(\D+)', item)[0]
            else:
                item = subject + item
            sub_course_no_list.append(item)

        possible_courses = sub_course_no_list
        sub_course_no_list = []
        for i, course in enumerate(possible_courses):
            if course in self._courses_names_set:
                sub_course_no_list.append(course)
            else:
                if 'XX' not in course: # a course simply not in the list
                    continue
                else: # handle 4XX type courses
                    # no subject mentioned, e.g., 4XX BIOL
                    target_course = course
                    if not re.match("^\D+", course):
                        target_course = possible_courses[i + 1] + course

                    # E.g., finds all the 400-level courses: BIOL4XX
                    if target_course not in self._subject_level_dict.keys():
                        all_XX_courses = []
                        prefix = re.findall('^(\w+)XX', target_course)[0]
                        for course in self._courses_names_set:
                            if prefix in course and course != target_course:
                                all_XX_courses.append(course)
                        self._subject_level_dict[target_course] = all_XX_courses

                    sub_course_no_list += (self._subject_level_dict.get(target_course))

        possible_courses = sub_course_no_list

        return possible_courses

    def _resolve_concurrencty_number(self, input_str, sections):
        concurrency_max = 0
        if input_str:
            input_str = input_str.lower()

        if input_str is None or input_str == 'no':
            return concurrency_max
        elif input_str == 'yes':
            return int(sections)
        elif 'no more than' in input_str: return int(input_str.split('no more than')[1])
        elif 'concurrent' in input_str: return int(input_str.split('concurrent')[0])
        else: return concurrency_max


    def get_courses_objects_list(self):
        return self._courses_objects_list

    def get_courses_names_set(self):
        return self._courses_names_set