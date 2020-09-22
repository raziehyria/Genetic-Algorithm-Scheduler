import json

import pandas

from classroom import Classroom
from course import Course
from department import Department
from instructor import Instructor
from meetingtime import MeetingTime
from room import Room


class Data:
    ROOMS = [['R2', 25], ['R2', 45], ['R3', 35]]
    MEETING_TIMES = [
        ["MT1", 'MWF 9 - 10'],
        ['MT2', 'MWF 10 - 11'],
        ['MT3', 'TTH 9 - 10:30'],
        ['MT4', 'TTH 10:30 - 12:00']
    ]

    INSTRUCTORS = [
        ['I1', "Dr. Vinayak Elangovan"],
        ['I2', 'Dr. Ishtiaque Hussain'],
        ['I3', 'Dr. Gokhan Ozden'],
        ['I4', 'Dr. Yi Yang']
    ]

    def __init__(self):
        self._rooms = []  # TODO: remove
        self._classrooms = []
        self._meetingTimes = []
        self._instructors = []

        # using Pandas as it does not create JSON files fron excel instead does it in-memory
        # source: https://www.journaldev.com/33335/python-excel-to-json-conversion
        excel_data_df = pandas.read_excel('ClassList.xlsx', sheet_name='Classroom Capacities')
        json_str = excel_data_df.to_json(orient='records')
        classroom_rows = json.loads(json_str)

        for each_class in classroom_rows:
            self._classrooms.append(Classroom(each_class.get('BLDG'), each_class.get("RM"), each_class.get("MX"),
                                              each_class.get("TYPE")))

        for room in self.ROOMS:
            self._rooms.append(Room(room[0], room[1]))
        for meetingTime in self.MEETING_TIMES:
            self._meetingTimes.append(MeetingTime(meetingTime[0], meetingTime[1]))
        for instructor in self.INSTRUCTORS:
            self._instructors.append(Instructor(instructor[0], instructor[1]))

        course1 = Course('C1', 'CMPSC 131', [self._instructors[0], self._instructors[1]], 25)
        course2 = Course('C2', 'CMPSC 132', [self._instructors[0], self._instructors[1]], 25)
        course3 = Course('C3', 'CMPENG 144', [self._instructors[2], self._instructors[3]], 35)
        course4 = Course('C4', 'CMPSC 360', [self._instructors[1], self._instructors[2]], 30)
        course5 = Course('C5', 'MATH 144', [self._instructors[2], self._instructors[3]], 25)
        course6 = Course('C6', 'MATH 121', [self._instructors[2]], 25)
        course7 = Course('C7', 'PHY 112', [self._instructors[3]], 35)
        course8 = Course('C8', 'PHY 144', [self._instructors[2], self._instructors[3]], 30)

        self._courses = [course1, course2, course3, course4, course5, course6, course7, course8]

        dept1 = Department("CMPSC", [course1, course2, course3, course4])
        dept2 = Department('MATH', [course5, course6])
        dept3 = Department('PHY', [course7, course8])

        self._depts = [dept1, dept2, dept3]

        self._numberOfClasses = 0
        for dept in self._depts:
            self._numberOfClasses += len(dept.get_courses())

    def get_rooms(self):
        return self._rooms

    def get_instructors(self):
        return self._instructors

    def get_courses(self):
        return self._courses

    def get_depts(self):
        return self._depts

    def get_meetingTimes(self):
        return self._meetingTimes

    def get_numberOfClasses(self):
        return self._numberOfClasses
