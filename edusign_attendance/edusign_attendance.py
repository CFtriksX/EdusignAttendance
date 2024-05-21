from edusign_attendance.Edusign import Edusign
from edusign_attendance.excel_wirtter import create_excel, add_worksheet
import os
from dotenv import load_dotenv
import json

async def get_student_ids_name(edusign, group_id):
    try:
        student_ids = (await edusign.get_group(group_id))['students']
    except:
        return False
    student_names = []
    for student_id in student_ids:
        student_names.append((await edusign.get_student(student_id))['email'])
    return student_ids, student_names

async def get_student_summary(edusign, student_ids, start_date, end_date):
    summarys = []
    for student_id in student_ids:
        summarys.append(await edusign.get_presence_summary(student_id, start_date, end_date))
    return summarys

async def get_school_id_attendance(edusign, workbook, start_date, end_date):
    group_id_list = json.loads(os.getenv("GROUPE_ID_LIST"))
    promo_list = json.loads(os.getenv("PROMO_LIST"))

    for index, group_id in enumerate(group_id_list):
        student_info = await get_student_ids_name(edusign, group_id)
        if student_info != False:
            summarys = await get_student_summary(edusign, student_info[0], start_date, end_date)
            add_worksheet(workbook, promo_list[index], student_info[1], summarys)

async def edusign_attendance(start_date, end_date):
    load_dotenv()
    token_list = json.loads(os.getenv("EDUSING_TOKEN"))
    workbook = create_excel(f"{start_date}_to_{end_date}.xlsx")
    for token in token_list:
        edusign = Edusign(token)
        await get_school_id_attendance(edusign, workbook, start_date, end_date)
    workbook.close()