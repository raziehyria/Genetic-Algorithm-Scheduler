import pprint

import excel2json
import xlrd

# should we use JSON instead?
# https://www.journaldev.com/33335/python-excel-to-json-conversion


excel2json.convert_from_file('ClassList.xlsx')

# MeetingTime = []
# read the JSON file
# for each item in JSON obj:
#    meetingtime = MeetingTime(item.get('MX), item.get('BLD'), ..)
#    MeetingTime.append(meetingtime)

wb = xlrd.open_workbook("ClassList.xlsx")
current_sheet = wb.sheet_by_index(0)
current_sheet.cell_value(0, 0)


courseDetailsList = []
roomDetailsList = []

for row in range(current_sheet.nrows):
    courseDetailsList.append(current_sheet.row_values(row))

pprint.pprint(courseDetailsList)

current_sheet = wb.sheet_by_index(1)
current_sheet.cell_value(0, 0)

for rowSheet2 in range(current_sheet.nrows):
    roomDetailsList.append(current_sheet.row_values(rowSheet2))


pprint.pprint(roomDetailsList)