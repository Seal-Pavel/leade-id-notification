import pytz

from datetime import datetime

from mypackages.leader_id.employee_schedule import (Pavel,
                                                    Nika,
                                                    Denis,)

TZ_MC = pytz.timezone('Europe/Moscow')


class Employees:
    def get_current_employees(self, day_of_week=None, time_of_day=None) -> list:
        now = datetime.now(TZ_MC)
        day = day_of_week if day_of_week is not None else now.weekday()
        time = time_of_day if time_of_day is not None else now.time()

        employees = []
        for employee in [Pavel(), Nika(), Denis(), Vova()]:
            if day in employee.work_days:
                for work in employee.full_schedule[day]:
                    if work['start'] < time < work['end']:
                        employees.append(employee)
        return employees
