from logger_settings.logger_settings import logger
from functools import wraps
import time

def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка. Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            t = start_sleep_time
            while True:
                try:
                    res = func(*args, **kwargs)
                    return res
                except Exception as e:
                    logger.warning(f'except in backoff : {e.args}')
                    t =  border_sleep_time if t >= border_sleep_time else start_sleep_time*factor
                    logger.debug(f'this new t in backoff : {t}')
                    time.sleep(t)
        return inner
    return func_wrapper


#тестовый декоратор
# def backoff(start_sleep_time: float = 0.1, factor: float = 2, border_sleep_time: float = 10):
#     def decorator(func):
#         @wraps(func)
#         def inner(*args, **kwargs):
#             logger.debug('start doing inner')
#             func(*args, **kwargs)
#             logger.debug('end doing inner')
#
#
#         return inner
#     return decorator

# @backoff()
# def say(name, surname, age):
#     print('hello world', name, surname, age)
# say('VV', 'FF', 400)

