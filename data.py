from pandas import pandas
import json
from classroom import Classroom
from coursedata import CourseData
from meetingtimedata import MeetingTimeData


class Data:

    def __init__(self):
        self._classrooms = []

        # using Pandas as it does not create JSON files fron excel instead does it in-memory
        # source: https://www.journaldev.com/33335/python-excel-to-json-conversion
        excel_data_df = pandas.read_excel('ClassList.xlsx', sheet_name='Classroom Capacities')
        json_str = excel_data_df.to_json(orient='records')
        classroom_rows = json.loads(json_str)

        for each_class in classroom_rows:
            self._classrooms.append(Classroom(each_class.get('BLDG'), each_class.get("RM"), each_class.get("MX"),
                                              each_class.get("TYPE")))

        # getting all course info from excel file and storing it
        coursedata = CourseData()
        self._courses = coursedata.get_courses()

        # getting all room info info from excel file and storing it
        meetingTimeData = MeetingTimeData()
        self._meetingTimes = meetingTimeData.get_meetingTimes()

        self._numberOfClasses = len(self._courses)

    def get_classrooms(self):
        return self._classrooms

    def get_courses(self):
        return self._courses

    def get_meetingTimes(self):
        return self._meetingTimes

    def get_numberOfClasses(self):
        return self._numberOfClasses
