# https://www.journaldev.com/33335/python-excel-to-json-conversion#converting-excel-sheet-to-json-string-using-pandas-module
# issues: some classes are not listed, ex: CMPSC 221 does not exist in excel, so it does not register it as a coreq/prereq/conflct
# regex pattern breaks in some situations, works with current inputs though

import pandas
import json
import re
from course import Course
import re

class CourseData():
    def __init__(self):
        self.courses = []
        self._all_courses = set()
        self._subject_level_dict = {}

        excel_data_df = pandas.read_excel('Course list and attributes.xlsx', sheet_name='S&E Courses')
        json_str = excel_data_df.to_json(orient='records')  # use this to read rows not columns
        data = json.loads(json_str)

        for row in data:
            self._all_courses.add("{}{}".format(row.get('Subject').strip().upper(), str(row.get('Num')).strip()))

        for course_row in data:
            pre_reqs = self.resolve_course_list(course_row.get('Pre-Req'))
            co_reqs = self.resolve_course_list(course_row.get('Co-Req'))
            potential_conflicts = self.resolve_course_list(course_row.get('Potential conflicts'))

            subject = course_row.get('Subject').strip()
            num = str(course_row.get('Num')).strip()
            description = course_row.get('Descr')
            meeting_pattern = course_row.get('Meeting pattern')
            capacity = course_row.get('Enr Cpcty')
            mutex = self.resolve_course_list(course_row.get('Mutually exclusive with'))
            room_in = course_row.get('Room in')
            if room_in is None:
                room_in = ""

            self.courses.append(Course(subject, num, description, meeting_pattern, capacity, pre_reqs, co_reqs,
                                       potential_conflicts, mutex, room_in))



        # for course in data:
        #
        #     #print(course)
        #     courseAttr = []
        #     # I could not find a way to make it work without this,
        #     # using dictionary keys from the json str directly resulted in errors i could not figure out how fix
        #     for attr in course.values():
        #         courseAttr.append(str(attr).strip()) # make everything a string just for consistency and to remove whitespaces
        #         # print(attr)
        #     # print(courseAttr)
        #
        #     """courseObj = Course(course["Subject"], str(course["Num"]), course["Descr"], course["Meeting pattern"], course["Enr Cpcty"],
        #                        course["Pre-Req"], course["Co-Req"], course["Potential conflicts"], course["Mutually exclusive with"], course["Room in"])"""
        #     courseObj = Course(courseAttr[0], str(courseAttr[1]), courseAttr[2], courseAttr[3], courseAttr[4],
        #                        courseAttr[5], courseAttr[6], courseAttr[7], courseAttr[8], courseAttr[9])
        #     self.courses.append(courseObj)
        #
        # # Using Regex to parse complex strings from file into lists for coreq, prereq etc.
        # for course in self.courses:
        #     coreqs = []
        #     prereqs = []
        #     conflicts = []
        #     # print(course)
        #     for anotherCourse in self.courses:
        #         if course == anotherCourse:
        #             pass
        #         else:
        #             # ex: "(.*BIOL[^a-z]*(?![a-z])[^a-z]*(?<!\d)110(?!\d).*)"
        #             # if subject and name are in the string in that order I can assume its included,
        #             # uses a negative look ahead and negative lookbehind to make sure it does not match with any numbers that are
        #             # not part of the course number
        #
        #             pattern = r"(.*" + anotherCourse.get_subject() + "[^a-z]*(?![a-z])[^a-z]*(?<!\d)" + anotherCourse.get_number() + "(?!\d).*)"
        #
        #             # ex: "(.*PHYS ?4xx.*)|(.*4xx (?=PHYS).*)"
        #             # catches strings that use different notation using something like "subject" \dxx to represent an entire level of courses
        #             altPattern = r"(.*" + anotherCourse.get_subject() + " ?.*(?<!\d)" + anotherCourse.get_number()[
        #                 0] + "xx(?!\d).*)|(.*(?<!\d)" + \
        #                          anotherCourse.get_number()[0] + "xx (?=" + anotherCourse.get_subject() + ").*)"
        #             # print(pattern)
        #             # print(altPattern)
        #             if re.search(pattern, course.get_corequisites(), re.IGNORECASE):
        #                 coreqs.append(anotherCourse.get_name())
        #             if re.search(pattern, course.get_prerequisites(), re.IGNORECASE):
        #                 prereqs.append(anotherCourse.get_name())
        #             if re.search(pattern, course.get_potentialConflicts(), re.IGNORECASE):
        #                 conflicts.append(anotherCourse.get_name())
        #             if re.search(altPattern, course.get_potentialConflicts(), re.IGNORECASE):
        #                 for i in self.courses:
        #                     if i.get_name() in conflicts:
        #                         pass
        #                     elif i == anotherCourse:
        #                         pass
        #                     elif i.get_subject() == anotherCourse.get_subject() and i.get_number()[0] == \
        #                             anotherCourse.get_number()[0]:
        #                         conflicts.append(i.get_name())
        #     course.set_corequisites(coreqs)
        #     course.set_prerequisites(prereqs)
        #     course.set_potentialConflicts(conflicts)

    def resolve_course_list(self, input_str):
        """
        This method parses the input string and returns the list of courses
        :param input_str:
        :return:
        """

        # if input_str is missing or 'None' or empty, simply return empty list
        if input_str is None or input_str == "None" or len(input_str) == 0: return []

        # converting the whole string into upper case for ease of processing
        input_str = input_str.upper().strip()

        if 'OR' not in input_str and 'AND' not in input_str and ',' not in input_str:
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
            if course in self._all_courses:
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
                        for course in self._all_courses:
                            if prefix in course:
                                all_XX_courses.append(course)
                        self._subject_level_dict[target_course] = all_XX_courses

                    sub_course_no_list += (self._subject_level_dict.get(target_course))

        possible_courses = sub_course_no_list

        return possible_courses









courseData = CourseData()
print('DONE')

"""for i, course in enumerate(courseData.courses):
    # print(course)
    print(i+2, course.get_name(), "coreqs:" , course.get_corequisites() , "prereqs:" , course.get_prerequisites() , "conflicts:" , course.get_potentialConflicts())"""
