from edusign_attendance.Edusign import EdusignToken
from edusign_attendance.excel_wirtter import create_excel, add_worksheet
import os
from dotenv import load_dotenv
import json

async def log_in(school_id):
    edusign = EdusignToken()
    if not await edusign.login(school_id):
        return False
    return edusign

def create_student_sheet(student, sessions):
    for session in sessions:
        student_status = next(filter(lambda x: x['studentId'] == student[0], session))
        if student_status['state'] == True:
            if student_status.get('delay', False):
                student.append("Late")
            else:
                student.append("OK")
        elif student_status['signatureEmail'] == None:
            student.append("NOK")
        else:
            if student_status.get('delay', False):
                student.append("SIGN Late")
            else:
                student.append("SIGN")
    return student

def get_name_from_id(students, id):
    student = next(filter(lambda x: x['ID'] == id, students))
    return student['EMAIL']

def create_matrix(sessions, students, promo):
    table = []
    for student in students:
        table.append(create_student_sheet([student['ID']], sessions))
        table[-1][0] = get_name_from_id(students, student['ID'])
    return table

def get_dates(sessions):
    date_list = ["Login"]
    for session in sessions:
        date = session["begin"][8:12]
        if date[-1] == '0':
            date_list.append(date[:2] + " - Matin")
        else:
            date_list.append(date[:2] + " - Apres-midi")
    return date_list

async def get_promo_attendance(edusign, start_date, end_date, promo):
    sessions = await edusign.get_sessions(start_date, end_date, promo)
    if len(sessions) == 0:
        return False
    sessions = sessions[::-1]
    date_list = get_dates(sessions)
    all_sessions = []
    students = await edusign.get_students(sessions[0]['edusign_id'])
    for session in sessions:
        all_sessions.append(await edusign.get_session(session['edusign_id']))
    return create_matrix(all_sessions, students, promo), date_list

async def get_school_id_attendance(edusign, workbook, start_date, end_date):
    key_list = json.loads(os.getenv("KEY_LIST"))
    promo_list = json.loads(os.getenv("PROMO_LIST"))

    for index, element in enumerate(key_list):
        result = await get_promo_attendance(edusign, start_date, end_date, element)
        if result != False:
            add_worksheet(workbook, promo_list[index], result[0], result[1])

async def edusign_attendance(start_date, end_date):
    load_dotenv()
    workbook = create_excel(f"{start_date}_to_{end_date}.xlsx")
    edusign = EdusignToken()
    school_ids = await edusign.login()
    for school_id, token in list(school_ids.items()):
        edusign.set_school_id(school_id)
        edusign.set_token(token)
        await get_school_id_attendance(edusign, workbook, start_date, end_date)
    workbook.close()