import sys
import re
import asyncio
from edusign_attendance.edusign_attendance import edusign_attendance

def print_help():
    print("Bad arguments !!")
    print("The program create an Excel of attendance between two dates for every promotions you specify in the .env file.")
    print("You can see how to fill the .env file with the .env_exemple file.")
    print("Here how to launch the app:")
    print("With python >= 3.10 run python run.py YY-MM-DD YY-MM-DD")
    print("The first date is the start and the seccond the end.")
    print("Example:\n   $ python main.py 22-12-01 22-12-05")
    print("It will create this file '22-12-01_to_22-12-05.xlsx'")
    exit(84)

def verify_argument(start_date, end_date):
    if not re.search("^\d\d-\d\d-\d\d$", start_date):
        print_help()

    if not re.search("^\d\d-\d\d-\d\d$", end_date):
        print_help()

if __name__ == '__main__':
    match len(sys.argv):
        case 3:
            verify_argument(sys.argv[1], sys.argv[2])
            asyncio.run(edusign_attendance(sys.argv[1], sys.argv[2]))
        case _:
            print_help()