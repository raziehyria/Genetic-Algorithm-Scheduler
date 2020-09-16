import xlrd
import pprint

wb = xlrd.open_workbook("ClassList.xlsx")
sheet = wb.sheet_by_index(0)
sheet.cell_value(0,0)


rows = sheet.nrows

courseDetailsList = []

for row in range(rows):
    courseDetailsList.append(sheet.row_values(row))

pprint.pprint(courseDetailsList)

sheet2 = wb.sheet_by_index(1)
sheet.cell_value(0,0)


totalRowsSheet2 = sheet2.nrows

roomDetailsList = []
for rowSheet2 in range(totalRowsSheet2):
    roomDetailsList.append(sheet2.row_values(rowSheet2))


pprint.pprint(roomDetailsList)