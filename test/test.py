import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../judger")

from judge import judge
import unittest
import re

class Test(unittest.TestCase):
    def setUp(self):
        self.pwd = os.getcwd()

    def tearDown(self):
        os.chdir(self.pwd)

    def test_all_pass(self):
        pwd = os.getcwd()

        report = judge('all_pass/judge.yaml')
        self.assertEqual(len(report), 5)
        # Traverse the value of report
        # Assert that all values are None
        for result in report.values():
            self.assertEqual(result, None, result)

        self.assertEqual(os.getcwd(), pwd)

    def test_with_fail(self):
        pwd = os.getcwd()

        report = judge('with_fail/judge.yaml')
        self.assertEqual(len(report), 5)
        # Traverse the value of report
        # Assert that all values are None except the "input_5"
        for testcase, result in report.items():
            if 'input_5' in testcase:
                self.assertNotEqual(result, None, result)
            else:
                self.assertEqual(result, None, result)

        self.assertEqual(os.getcwd(), pwd)

    def test_compile_error(self):
        pwd = os.getcwd()

        report = judge('compile_error/judge.yaml')
        self.assertEqual(len(report), 1)
        self.assertTrue('Compile Error' in report)

        self.assertEqual(os.getcwd(), pwd)

    def test_missing_input(self):
        from testcase import InputMiss
        with self.assertRaises(InputMiss) as raised:
            judge('missing_input/judge.yaml')
        expect = re.compile("Input file for .*missing_input/testcases/output_1.txt is missing")
        message = f'{raised.exception}'
        self.assertIsNotNone(expect.match(message), message)

    def test_missing_expect(self):
        from testcase import ExpectMiss
        with self.assertRaises(ExpectMiss) as raised:
            judge('missing_expect/judge.yaml')
        expect = re.compile("Expect file for .*missing_expect/testcases/input_1.txt is missing")
        message = f'{raised.exception}'
        self.assertIsNotNone(expect.match(message), message)

if __name__ == '__main__':
    unittest.main()