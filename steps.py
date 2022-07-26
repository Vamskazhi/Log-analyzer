import mimetypes
import re
from collections import namedtuple
import gzip
import logging
from mimetypes import guess_type
from pathlib import Path
from datetime import datetime
from typing import Any, Generator


def get_last_file(files: list, format_date: str = '%Y%m%d') -> Path:
    """"""
    pattern = re.compile(r'\d{8}')
    latest_file = None
    max_date = datetime.strptime(f'{pattern.findall(files[0].name)[0]}', format_date)
    for i in files:
        _date = datetime.strptime(f'{pattern.findall(i.name)[0]}', format_date)
        if _date >= max_date:
            max_date = _date
            latest_file = i
    return latest_file


def read_in_chunks(file_name: Path, chunk_size=1024):
    """"""
    with gzip.open(file_name, 'rb') as file_object:
        while True:
            data = file_object.readline().decode('utf-8')
            if not data:
                break
            yield data


def get_data_from_log(log_dir: str = './log') -> dict:
    """"""
    path_log_dir = Path(log_dir)
    last_file = get_last_file([i for i in path_log_dir.iterdir()])
    result = {}
    pattern = re.compile(r'\s/.*/.*/?\sHTTP/1.\d')
    for line in read_in_chunks(last_file):
        res = pattern.search(line)
        if res:
            url = res.group().strip().split(' ')[0]
            time_request = float(line[-6:])
            result[url] = added_time(time_request, result.get(url))
    return result


def get_common_params(urls: dict) -> dict:
    """"""
    Report = namedtuple('Report', 'url count_request time_sum time_avg time_max time_med')
    lens = []
    for url, times in urls.items():
        lens.append(len(times))
        t = Report(url, len(times), sum(times), sum(times)/len(times), max(times), median_value(times))
        print(t)
    print(lens)


def median_value(value: list) -> float:
    """"""
    value.sort()
    return value[len(value)//2]


def added_time(time_req: float, exist_list: list):
    """"""
    if not exist_list:
        exist_list = []
    exist_list.append(time_req)
    return exist_list


def find_log_file(log_dir: str = './log'):
    """"""
    path_log_dir = Path(log_dir)
    assert path_log_dir.is_dir() is True, f'{log_dir} is not directory'
    # TODO replace on the exception later
    log_files = [i for i in path_log_dir.iterdir()]
    assert len(log_files) > 0, f'{log_dir} is empty'
    # TODO replace on the exception later
    return get_last_file(log_files)


def read_log(path):
    """"""
    with open(find_log_file(path), 'r') as f:
        generator = (i for i in f.read())
    return generator


def sorting_url():
    """
    Ckol'ko n kakih url, vremia, mb imeet smysl podniat' db
    :return:
    """