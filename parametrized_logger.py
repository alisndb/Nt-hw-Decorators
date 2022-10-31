import datetime
import json

import requests


def parametrized_logger(logs_path):
    def logger(func):
        def logger_func(*args, **kwargs):
            result = func(*args, **kwargs)

            log = {
                'datetime': f'{datetime.datetime.now()}',
                'func': func.__name__,
                'pos_args': args,
                'key_args': kwargs,
                'result': result
            }

            with open(logs_path, 'w') as f:
                json.dump(log, f, ensure_ascii=False, indent=2)

            return result

        return logger_func

    return logger


# Применяем логгер к приложению (из старого д/з):
if __name__ == '__main__':
    @parametrized_logger(logs_path='logs_2.json')
    def get_questions(demo_arg):
        current_date = datetime.date.today()
        from_date = current_date - datetime.timedelta(days=1)
        to_date = current_date + datetime.timedelta(days=1)

        from_date_ts = int(datetime.datetime(*[int(i) for i in str(from_date).split('-')]).timestamp())
        to_date_ts = int(datetime.datetime(*[int(i) for i in str(to_date).split('-')]).timestamp())

        url = f'https://api.stackexchange.com/2.3/questions?fromdate={from_date_ts}'\
              f'&todate={to_date_ts}&order=desc&sort=activity&tagged=python&site=stackoverflow'
        resp = requests.get(url)

        if resp.status_code != 200:
            print('Ошибка!')

        titles = []
        for item in resp.json()['items']:
            titles.append(item['title'])

        return titles


    demo_arg = 'Made for logger demonstration!'

    get_questions(demo_arg)
