# Edusing Attendance

Tools to complete Edusign on the lack of summary of class attendance.


# Installation
## Requirements
- `hatch` is the [project manager](https://github.com/pypa/hatch) used for the EdusignAttendance project.

## Configuration

You must create a .env file based on the .env_exemple file

- `EDUSING_TOKEN` : An array of all your school token.
- `PROMO_LIST` : An array of all your edusign class key
- `GROUPE_ID_LIST` : An array of all your edusign class ids
- `PROMO_LIST` : An array of all your class name. It's used only in the excel file so you can name them as you prefer.

## Run

- `hatch run python main.py YYYY-MM-DD YYYY-MM-DD` the first date is the start and the second the end

This will generate an xlsx file named `YYYY-MM-DD_to_YYYY-MM-DD.xlsx` that contain a page for every class you set in the .env file.

Each page has a list of all students with their mail, the number of hours present, the number of hours missing and the number of missing hours justified.