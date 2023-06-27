# 从xls文件中读取数据
import openpyxl

xlsx_path = r"table\python_read.xlsx"

workbook = openpyxl.load_workbook(xlsx_path)
print(workbook.sheetnames)
