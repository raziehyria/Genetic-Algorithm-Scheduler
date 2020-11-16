import json

import pandas

from faculty import Faculty


class FacultyData:

    def __init__(self, file_path):
        self._faculty_objects_list = []

        excel_data_df = pandas.read_excel(file_path, sheet_name='Faculty Preference')
        json_str = excel_data_df.to_json(orient='records')  # use this to read rows not columns
        data = json.loads(json_str)

        for faculty_row in data:
            if faculty_row.get('Full Name') is not None:
                name = faculty_row.get('Full Name').strip()
                availability = faculty_row.get('Availability').strip()
                courses = [course.strip() for course in faculty_row.get('Courses').strip().split(',')]
                contact_hours = faculty_row.get('Total # of Contact hours')

                if type(contact_hours) == str and "to" in contact_hours:
                    contact_hours = int(contact_hours.split("to")[1].strip())
                self._faculty_objects_list.append(Faculty(name, availability, courses, contact_hours))

        # add faculty object for 'Staff' who'd teach courses that have no faculties
        self._faculty_objects_list.append(Faculty('Staff', 'No Restrictions', None, None))

    def get_faculty(self):
        return self._faculty_objects_list
