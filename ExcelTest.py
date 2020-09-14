import xlrd

wb = xlrd.open_workbook("ClassList.xlsx")
sheet = wb.sheet_by_index(0)
sheet.cell_value(0,0)

row = 0
rows = sheet.nrows

valueList = []

while row < rows:
    valueList.append(sheet.row_values(row))
    row = row +1

print(valueList[116])