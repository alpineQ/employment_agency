""" Конфигурация веб приложения """


# pylint: disable=too-few-public-methods
class Config:
    """ Класс конфигурации веб приложения """
    SERVER = 'sql_server'
    DATABASE = 'EmploymentAgencyDB'
    PASSWORD = 'QwErTy123!'
    USERNAME = 'SA'

    TABLE_INFO = {'positions': {'name': 'Должности',
                                'db': 'dbo.Positions',
                                'url': 'http://localhost/positions'},
                  'employers': {'name': 'Работодатели',
                                'db': 'dbo.Employers',
                                'url': 'http://localhost/employers'},
                  'applicants': {'name': 'Соискатели',
                                 'db': 'dbo.Applicants',
                                 'url': 'http://localhost/applicants'},
                  'education': {'name': 'Образование',
                                'db': 'dbo.Education',
                                'url': 'http://localhost/education'},
                  'agents': {'name': 'Агенты',
                             'db': 'dbo.Agents',
                             'url': 'http://localhost/agents'},
                  'vacancies': {'name': 'Вакансии',
                                'db': 'dbo.Vacancies',
                                'url': 'http://localhost/vacancies'},
                  'deals': {'name': 'Сделки',
                            'db': 'dbo.Deals',
                            'url': 'http://localhost/deals'}}
