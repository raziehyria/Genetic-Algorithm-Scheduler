"""
This class contains faculty members data
"""


class Faculty:

    def __init__(self, name, availability, courses, contact_hours):
        self.name = name
        self.availability = availability
        self.courses = courses
        self.contact_hours = contact_hours

    def get_name(self):
        return self.name

    def get_availability(self):
        return self.availability

    def get_courses(self):
        return self.courses

    def get_contact_hours(self):
        return self.contact_hours

    def __str__(self):
        return self.get_name()
