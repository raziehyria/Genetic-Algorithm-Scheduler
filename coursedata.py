# https://www.journaldev.com/33335/python-excel-to-json-conversion#converting-excel-sheet-to-json-string-using-pandas-module
# issues: some classes are not listed, ex: CMPSC 221 does not exist in excel, so it does not register it as a coreq/prereq/conflct
# regex pattern breaks in some situations, works with current inputs though

import pandas
import json
import re
from course import Course

class CourseData():
    def __init__(self):
        self.courses = []

        excel_data_df = pandas.read_excel('Course list and attributes.xlsx', sheet_name='S&E Courses')
        json_str = excel_data_df.to_json(orient='records')  # use this to read rows not columns
        data = json.loads(json_str)
        # print(data)
        # print(len(data))

        for course in data:

            #print(course)
            courseAttr = []
            # I could not find a way to make it work without this,
            # using dictionary keys from the json str directly resulted in errors i could not figure out how fix
            for attr in course.values():
                courseAttr.append(str(attr).strip()) # make everything a string just for consistency and to remove whitespaces
                # print(attr)
            # print(courseAttr)

            """courseObj = Course(course["Subject"], str(course["Num"]), course["Descr"], course["Meeting pattern"], course["Enr Cpcty"],
                               course["Pre-Req"], course["Co-Req"], course["Potential conflicts"], course["Mutually exclusive with"], course["Room in"])"""
            courseObj = Course(courseAttr[0], str(courseAttr[1]), courseAttr[2], courseAttr[3], courseAttr[4],
                               courseAttr[5], courseAttr[6], courseAttr[7], courseAttr[8], courseAttr[9])
            self.courses.append(courseObj)

        # Using Regex to parse complex strings from file into lists for coreq, prereq etc.
        for course in self.courses:
            coreqs = []
            prereqs = []
            conflicts = []
            # print(course)
            for anotherCourse in self.courses:
                if course == anotherCourse:
                    pass
                else:
                    # ex: "(.*BIOL[^a-z]*(?![a-z])[^a-z]*(?<!\d)110(?!\d).*)"
                    # if subject and name are in the string in that order I can assume its included,
                    # uses a negative look ahead and negative lookbehind to make sure it does not match with any numbers that are
                    # not part of the course number

                    pattern = r"(.*" + anotherCourse.get_subject() + "[^a-z]*(?![a-z])[^a-z]*(?<!\d)" + anotherCourse.get_number() + "(?!\d).*)"

                    # ex: "(.*PHYS ?4xx.*)|(.*4xx (?=PHYS).*)"
                    # catches strings that use different notation using something like "subject" \dxx to represent an entire level of courses
                    altPattern = r"(.*" + anotherCourse.get_subject() + " ?.*(?<!\d)" + anotherCourse.get_number()[
                        0] + "xx(?!\d).*)|(.*(?<!\d)" + \
                                 anotherCourse.get_number()[0] + "xx (?=" + anotherCourse.get_subject() + ").*)"
                    # print(pattern)
                    # print(altPattern)
                    if re.search(pattern, course.get_corequisites(), re.IGNORECASE):
                        coreqs.append(anotherCourse.get_name())
                    if re.search(pattern, course.get_prerequisites(), re.IGNORECASE):
                        prereqs.append(anotherCourse.get_name())
                    if re.search(pattern, course.get_potentialConflicts(), re.IGNORECASE):
                        conflicts.append(anotherCourse.get_name())
                    if re.search(altPattern, course.get_potentialConflicts(), re.IGNORECASE):
                        for i in self.courses:
                            if i.get_name() in conflicts:
                                pass
                            elif i == anotherCourse:
                                pass
                            elif i.get_subject() == anotherCourse.get_subject() and i.get_number()[0] == \
                                    anotherCourse.get_number()[0]:
                                conflicts.append(i.get_name())
            course.set_corequisites(coreqs)
            course.set_prerequisites(prereqs)
            course.set_potentialConflicts(conflicts)


courseData = CourseData()

"""for i, course in enumerate(courseData.courses):
    # print(course)
    print(i+2, course.get_name(), "coreqs:" , course.get_corequisites() , "prereqs:" , course.get_prerequisites() , "conflicts:" , course.get_potentialConflicts())"""
