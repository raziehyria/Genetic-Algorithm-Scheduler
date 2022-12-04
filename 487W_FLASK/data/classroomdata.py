import pandas
import json

from classroom import Classroom


class ClassroomData:
    """
    This class handles creating objects representing classrooms
    """

    def __init__(self,file_path):
        # using Pandas as it does not create JSON files fron excel instead does it in-memory
        # source: https://www.journaldev.com/33335/python-excel-to-json-conversion
        excel_data_df = pandas.read_excel(file_path, sheet_name='Classroom Capacities')
        json_str = excel_data_df.to_json(orient='records')
        classroom_rows = json.loads(json_str)
        self._classrooms_objects_list = []

        for each_class in classroom_rows:
            self._classrooms_objects_list.append(Classroom(each_class.get('BLDG'), each_class.get("RM"), each_class.get("MX"),
                                                           each_class.get("TYPE")))

    def get_classroom_objects_list(self):
        return self._classrooms_objects_list