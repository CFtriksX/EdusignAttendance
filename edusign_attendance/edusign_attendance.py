from edusign_attendance.Edusign import EdusignToken
from edusign_attendance.excel_wirtter import create_excel, add_worksheet

async def log_in():
    edusign = EdusignToken()
    if not await edusign.login():
        return False
    return edusign

def create_student_sheet(student, sessions):
    for session in sessions:
        student_status = next(filter(lambda x: x['studentId'] == student[0], session))
        if student_status['state'] == True:
            if student_status.get('delay', False):
                student.append("Late")
            student.append("OK")
        elif student_status['signatureEmail'] == None:
            student.append("NOK")
        else:
            if student_status.get('delay', False):
                student.append("SIGN Late")
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

async def edusign_attendance(start_date, end_date):
    key_list = ['LYN202', 'LYN193', 'LYN201', 'LYN169', 'LYN194', 'LYN209', 'LYN210']
    promo_list = ['MSC1', 'MSC2', 'Pre-msc', 'WAC 2022', 'WAC 2023', 'WAC 2024', 'Coding']
    edusign = await log_in()
    if not edusign:
        print("Can not log in!\nPlease verify that you have specify the correct credentials in the .env file.")
        exit(84)
    workbook = create_excel(f"{start_date}_to_{end_date}.xlsx")
    for index, element in enumerate(key_list):
        result = await get_promo_attendance(edusign, start_date, end_date, element)
        if result != False:
            add_worksheet(workbook, promo_list[index], result[0], result[1])
    workbook.close()

