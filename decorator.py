from time import sleep, time
from base_config import PATH
import os


def time_decorator(function):  # 时间花费修饰器，用于计算一个函数所用的时间
    def wrapper(*args, **kwargs):
        start_time = time()
        function(*args, **kwargs)
        with open(os.path.join(PATH, 'result', 'result_temp.txt'), 'a', encoding='utf-8') as f:
            f.write(str(int(time() - start_time)) + 's')
            f.write('\n')
            print('time=' + str((time() - start_time)) + 's')
        print('--------------------------')
    return wrapper
