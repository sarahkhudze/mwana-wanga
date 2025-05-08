from datetime import datetime, timedelta


class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.lmp_date = None
        self.due_date = None
        self.current_week = None

    def set_pregnancy_data(self, lmp_date):
        self.lmp_date = lmp_date
        self.due_date = lmp_date + timedelta(days=280)
        self.current_week = (datetime.today() - lmp_date).days // 7