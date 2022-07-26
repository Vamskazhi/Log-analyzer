import unittest
from pathlib import Path

from steps import get_last_file, get_data_from_log, get_common_params


def get_files_list(path):
    return [i for i in Path(path).iterdir()]


class TestLoggerMethods(unittest.TestCase):

    def test_last_archive(self):
        self.assertEqual(
            'nginx-access-ui.log-20170930.gz',
            get_last_file(get_files_list('data_tests/log')).name,
            'Not expected name'
        )

    def test_last_file(self):
        self.assertEqual(
            'nginx-access-ui.log-20171031',
            get_last_file(get_files_list('data_tests/log1')).name,
            'Not expected name'
        )


class TestUnzip(unittest.TestCase):

    def test_unzip(self):
        file_path = get_data_from_log('data_tests/log')
        # print(file_path)
        get_common_params(file_path)
    # def test_unzip1(self):
    #     file_path = get_last_file(get_files_list('data_tests/log1'))
    #     read_log_file(file_name=file_path)
    #     # self.assertIsNotNone(next(read_log_file(file_name=file_path)))
