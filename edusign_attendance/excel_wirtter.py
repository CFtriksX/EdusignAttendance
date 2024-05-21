import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell

def create_excel(name):
    return xlsxwriter.Workbook(name)
    
def add_worksheet(workbook, promo_name, student_names, summarys):
    worksheet = workbook.add_worksheet(promo_name)
    top_format = workbook.add_format({'pattern': 1, 'left': 1, 'bottom': 2, 'bg_color': '#87CEEB'})
    cell_format = workbook.add_format({'pattern': 1, 'left': 1, 'top': 2, 'bottom': 2})
    worksheet.write(0, 0, "Mail", top_format)
    worksheet.write(0, 1, "Heures present", top_format)
    worksheet.write(0, 2, "Heures Absence", top_format)
    worksheet.write(0, 3, "Heures Absence Justifie", top_format)

    for index, student_name in enumerate(student_names):
        if len(summarys[index]) == 0:
            continue
        worksheet.write(index + 1, 0, student_name, cell_format)
        worksheet.write(index + 1, 1, summarys[index]['present'], cell_format)
        worksheet.write(index + 1, 2, summarys[index]['missing'], cell_format)
        worksheet.write(index + 1, 3, summarys[index]['justified'], cell_format)

    worksheet.conditional_format(1, 1, len(student_names), 1, {'type': '3_color_scale', 'min_color': '#f8696b', 'max_color': '#63be7b'})
    worksheet.conditional_format(1, 2, len(student_names), 2, {'type': '3_color_scale', 'min_color': '#63be7b', 'max_color': '#f8696b'})
    worksheet.autofilter(0, 0, len(student_names), 3)
    worksheet.set_column(0, 0, 32)
    for i in range(1, 4):
        worksheet.set_column(i, i, 20)


