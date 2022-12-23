from abc import ABC, abstractmethod
import aiohttp
import os

class Edusign(ABC):
    @abstractmethod
    async def login(self):
        ...

    @abstractmethod
    async def get_sessions(self, start_date, end_date, promo):
        ...
    
    async def get_session(self, session_id):
        ...

    @abstractmethod
    async def get_students(self, session_id):
        ...

    @abstractmethod
    async def send_mails(self, student_ids, session_id):
        ...

class EdusignToken(Edusign):
    def __init__(self):
        self.token = ''
        self.school_id = ''


    async def login(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{os.getenv("EDUSIGN_URL")}/professor/account/getByCredentials',
                json={'EMAIL': os.getenv("EDUSIGN_EMAIL"), 'PASSWORD': os.getenv("EDUSIGN_PASSWORD"), 'connexionMode': True}
            ) as resp:
                objs = await resp.json()
                if not objs.get('result'):
                    raise KeyError('No result found')
                objs = objs.get('result')
                school_ids = {}
                if not objs:
                    raise KeyError('No result found')
                self.token = objs[0]['TOKEN']
                for obj in objs:
                    if not obj.get('TOKEN'):
                        raise KeyError('No token found')
                    if not obj.get('SCHOOL_ID'):
                        raise KeyError('No school id')
                    school_ids.update({_id: obj['TOKEN'] for _id in obj['SCHOOL_ID']})
                self.school_id = school_ids[list(school_ids.keys())[0]]
                return school_ids
        return []

    def set_token(self, token):
        self.token = token

    def set_school_id(self, school_id):
        self.school_id = school_id


    async def get_sessions(self, start_date, end_date, promo):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{os.getenv("EDUSIGN_URL")}/professor/courses/getCourses/getLastProfessorCourses/{self.school_id}?start={start_date}&end={end_date}',
                headers={'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
            ) as resp:
                result = await resp.json()
                if not result.get('result'):
                    raise KeyError('No result found')
                return [{'edusign_id': res['COURSE_ID'], 'begin': res['START'], 'end': res['END']} for res in result['result']['result'] if promo in res['NAME']]

    async def get_session(self, session_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{os.getenv("EDUSIGN_URL")}/professor/courses/{self.school_id}/{session_id}',
                headers={'Authorization': f'Bearer {self.token}'}
            ) as resp:
                result = await resp.json()
                if not result.get('result') and result.get('status') != 'success':
                    raise KeyError('No result found')
                return result['result']['STUDENTS']

    async def get_students(self, session_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{os.getenv("EDUSIGN_URL")}/professor/courses/{self.school_id}/{session_id}',
                headers={'Authorization': f'Bearer {self.token}'}
            ) as resp:
                result = await resp.json()
                if not result.get('result'):
                    raise KeyError('No result found')
                student_ids = [c['studentId'] for c in result['result']['STUDENTS']]
                async with session.post(
                    f'{os.getenv("EDUSIGN_URL")}/professor/students/getManyAttendanceList/{self.school_id}/',
                    json={'studentIds': student_ids},
                    headers={'Authorization': f'Bearer {self.token}'}
                ) as response:
                    result = await response.json()
                    return result['result']

    async def send_mails(self, student_ids, session_id):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{os.getenv("EDUSIGN_URL")}/professor/courses/massSendSignEmail/{self.school_id}/{session_id}',
                json={'studentsId': student_ids},
                headers={'Authorization': f'Bearer {self.token}'}
            ) as resp:
                return await resp.json()
