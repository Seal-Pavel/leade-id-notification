from datetime import time
from config import config


class Pavel:
    def __init__(self):
        self.name = config.USEDESK_PAVEL_NAME
        self.email = config.USEDESK_PAVEL_EMAIL
        self.password = config.USEDESK_PAVEL_PASSWORD
        self.full_schedule = {
            5: [
                {
                    'start': time(9),
                    'end': time(23, 59)
                }
            ],
            6: [
                {
                    'start': time(9),
                    'end': time(23, 59)
                }
            ]
        }
        self.work_days = list(self.full_schedule.keys())

    def __str__(self):
        return f'{self.name}'


class Denis:
    def __init__(self):
        self.name = config.USEDESK_DENIS_NAME
        self.email = config.USEDESK_DENIS_EMAIL
        self.password = config.USEDESK_DENIS_PASSWORD
        self.full_schedule = {
            0: [
                {
                    'start': time(10),
                    'end': time(13)
                },
                {
                    'start': time(18),
                    'end': time(23, 59)
                }
            ],
            1: [
                {
                    'start': time(0),
                    'end': time(2)
                },
                {
                    'start': time(10),
                    'end': time(13)
                },
                {
                    'start': time(18),
                    'end': time(23, 59)
                }
            ],
            2: [
                {
                    'start': time(0),
                    'end': time(2)
                },
                {
                    'start': time(10),
                    'end': time(13)
                },
                {
                    'start': time(18),
                    'end': time(23, 59)
                }
            ],
            3: [
                {
                    'start': time(0),
                    'end': time(2)
                },
                {
                    'start': time(10),
                    'end': time(13)
                },
                {
                    'start': time(18),
                    'end': time(23, 59)
                }
            ],
            4: [
                {
                    'start': time(0),
                    'end': time(2)
                },
                {
                    'start': time(10),
                    'end': time(13)
                },
                {
                    'start': time(18),
                    'end': time(23, 59)
                }
            ],
            5: [
                {
                    'start': time(0),
                    'end': time(9)
                }
            ]
        }
        self.work_days = list(self.full_schedule.keys())

    def __str__(self):
        return f'{self.name}'


class Nika:
    def __init__(self):
        self.name = config.USEDESK_NIKA_NAME
        self.email = config.USEDESK_NIKA_EMAIL
        self.password = config.USEDESK_NIKA_PASSWORD
        self.full_schedule = {
            0: [
                {
                    'start': time(10),
                    'end': time(18)
                }
            ],
            1: [
                {
                    'start': time(10),
                    'end': time(18)
                }
            ],
            2: [
                {
                    'start': time(10),
                    'end': time(18)
                }
            ],
            3: [
                {
                    'start': time(10),
                    'end': time(18)
                }
            ],
            4: [
                {
                    'start': time(10),
                    'end': time(18)
                }
            ]

        }
        self.work_days = list(self.full_schedule.keys())

    def __str__(self):
        return f'{self.name}'


class Vova:
    def __init__(self):
        self.name = config.USEDESK_VOVA_NAME
        self.email = config.USEDESK_VOVA_EMAIL
        self.password = config.USEDESK_VOVA_PASSWORD
        self.full_schedule = {
            0: [
                {
                    'start': time(0),
                    'end': time(10)
                }
            ],
            1: [
                {
                    'start': time(2),
                    'end': time(10)
                }
            ],
            2: [
                {
                    'start': time(2),
                    'end': time(10)
                }
            ],
            3: [
                {
                    'start': time(2),
                    'end': time(10)
                }
            ],
            4: [
                {
                    'start': time(2),
                    'end': time(10)
                }
            ],
            6: [
                {
                    'start': time(0),
                    'end': time(9)
                }
            ]
        }
        self.work_days = list(self.full_schedule.keys())

    def __str__(self):
        return f'{self.name}'
