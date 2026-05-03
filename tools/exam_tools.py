from datetime import datetime


def calculate_days_to_exam(exam_date):

    exam = datetime.strptime(exam_date, "%Y-%m-%d")
    today = datetime.today()

    days_left = (exam - today).days

    return days_left