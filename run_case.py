import unittest
from base_config import PATH
import time
import os
import  HTMLTestRunner


case_path = PATH+'/testcase'
result_path = PATH+'/result'


def Creatsuite():  # 创建单元测试容器
    testunit = unittest.TestSuite()

    test_case_file = unittest.defaultTestLoader.discover(case_path, pattern='test_*.py', top_level_dir=None)

    for test_suite in test_case_file:
        for casename in test_suite:
            testunit.addTest(casename)
        print(testunit)
    return testunit

test_case = Creatsuite()


# 获取系统当前时间
now = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
day = time.strftime('%Y-%m-%d', time.localtime(time.time()))

# 定义报告存放路径，支持相对路径

temp_result = result_path + '/' + day
if os.path.exists(temp_result):
    filename = temp_result + '/' + now + '_result.html'
    with open(filename, 'wb') as f:
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='测试报告', description='用例详情')
        runner.run(test_case)
else:
    os.mkdir(temp_result)
    filename = temp_result + '/' + now + '_result.html'
    with open(filename, 'wb') as f:
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='测试报告', description='用例详情')
        runner.run(test_case)

