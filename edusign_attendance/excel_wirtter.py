import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell

def create_excel(name):
    return xlsxwriter.Workbook(name)
    
def add_worksheet(workbook, promo_name, students_matrix, date_list):
    worksheet = workbook.add_worksheet(promo_name)
    top_format = workbook.add_format({'pattern': 1, 'left': 1, 'bottom': 2, 'bg_color': '#87CEEB'})
    cell_format = workbook.add_format({'pattern': 1, 'left': 1, 'top': 2, 'bottom': 2})
    col_count = len(date_list)
    for index, date in enumerate(date_list):
        worksheet.write(0, index, date, top_format)
    worksheet.write(0, col_count, "Count NOK", top_format)
    worksheet.write(0, col_count + 1, "Message Absence", top_format)

    row = 1
    for line in students_matrix:
        for col, element in enumerate(line):
            worksheet.write(row, col, element, cell_format)

        start_cell = xl_rowcol_to_cell(row, 1)
        end_cell = xl_rowcol_to_cell(row, col_count - 1)
        worksheet.write(
            row,
            col_count,
            f'=COUNTIF({start_cell}:{end_cell},"NOK")+COUNTIF({start_cell}:{end_cell},"SIGN")+COUNTIF({start_cell}:{end_cell},"SIGN Late")',
            cell_format
        )
        row += 1

    for index in range(0, row - 1):
        text = ""
        for col in range(1, col_count):
            match students_matrix[index][col]:
                case "OK":
                    continue
                case "NOK":
                    text += f"- Absent le {date_list[col]}\n"
                case "SIGN":
                    text += f"- Present mais n'as pas signe le {date_list[col]}\n"
                case "SIGN Late":
                    text += f"- En retard mais present mais n'as pas signe le {date_list[col]}\n"
                case _:
                    continue
        worksheet.write(index + 1, col_count + 1, text)

    worksheet.conditional_format(0, 0, row, col_count, {
        'type':     'cell',
        'criteria': 'equal to',
        'value':    '"OK"',
        'format':   workbook.add_format({'bg_color': '#90EE90'})
    })
    worksheet.conditional_format(0, 0, row, col_count, {
        'type':     'cell',
        'criteria': 'equal to',
        'value':    '"Late"',
        'format':   workbook.add_format({'bg_color': '#FFFF66'})
    })
    worksheet.conditional_format(0, 0, row, col_count, {
        'type':     'cell',
        'criteria': 'equal to',
        'value':    '"NOK"',
        'format':   workbook.add_format({'bg_color': '#FF726F'})
    })
    worksheet.conditional_format(0, 0, row, col_count, {
        'type':     'text',
        'criteria': 'containing',
        'value':    'SIGN',
        'format':   workbook.add_format({'bg_color': '#FFB52E'})
    })
    worksheet.conditional_format(1, col_count, row, col_count, {'type': '3_color_scale', 'min_color': '#63be7b', 'max_color': '#f8696b'})
    worksheet.autofilter(0, 0, row, col_count + 1)
    worksheet.set_column(0, 0, 32)
    for i in range(1, col_count + 1):
        worksheet.set_column(i, i, 12)


