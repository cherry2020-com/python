#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import json
import os
import pickle
import time
from functools import wraps

from small_tools.hospital_schedule import FILE_PATH, APP_ACCESS_TOKEN, HAS_CARD, DEPARTMENT, HOSPITAL, DOCTOR, \
    SLOW_TIMEOUT, DATE, TIME, FAST_TIMEOUT, IS_DEBUG_TIME, IS_DEBUG_SUBMIT
from utils.fiddler_session import RawToPython


imp_templ = u'\033[1;33;44m{}\033[0m'


def save_file(func):
    @wraps(func)  # 保持原函数名不变
    def wrapper(*args, **kwargs):
        print '--> start: ', func.__name__
        base_path = './fuchan_tmp'
        if not os.path.exists(base_path):
            os.mkdir(base_path)
        path = os.path.join(base_path, DATE)
        if not os.path.exists(path):
            os.mkdir(path)
        path = os.path.join(path, func.__name__)
        if os.path.exists(path):
            with open(path) as f:
                res = pickle.load(f)
        else:
            res = func(*args, **kwargs)
            with open(path, 'wb+') as f:
                pickle.dump(res, f)
        return res
    return wrapper


def replace_app_access_token():
    if 'UGlpFAlTvmwL9XWK4x2GLpjqxC8m2yyljYfCCVYaF4w' == APP_ACCESS_TOKEN:
        print '--> replace_app_access_token: same token'
        return
    for _path, _, _files in os.walk(FILE_PATH):
        for _file in _files:
            head = os.path.join(_path, _file)
            print '--> replace app_access_token:', head
            with open(head) as f:
                head_data = f.read()
            head_data = head_data.replace('UGlpFAlTvmwL9XWK4x2GLpjqxC8m2yyljYfCCVYaF4w', APP_ACCESS_TOKEN)
            with open(head, 'wb+') as f:
                f.write(head_data)


def check_card_no(is_one=True):
    head = os.path.join(FILE_PATH, 'getCurrentCardNo.txt')
    req = RawToPython(head)
    req.set_param(req_param={"app_access_token": APP_ACCESS_TOKEN})
    while True:
        try:
            req_json = req.requests(timeout=SLOW_TIMEOUT).json()
            print req_json
        except Exception as e:
            print '--> request error', e
        if is_one:
            break
        time.sleep(5)


@save_file
def get_department_id(from_file=False):
    if from_file:
        _file = os.path.join(FILE_PATH, 'departmentList.json')
        with open(_file) as f:
            data = f.read()
    else:
        head = os.path.join(FILE_PATH, 'departmentList.txt')
        data = RawToPython(head).requests(timeout=SLOW_TIMEOUT).text
    _json = json.loads(data)
    department_id = None
    for hos in _json['result']['departmentList']:
        if hos['yq'] != HOSPITAL:
            continue
        for dep in hos['xkflList']:
            for dep2 in dep['deptList']:
                if dep2['deptName'] == DEPARTMENT:
                    department_id = dep2['deptCode']
    assert department_id
    print '--> get_department_id: ', DEPARTMENT, department_id
    return department_id


@save_file
def get_docker_id(department_id):
    head = os.path.join(FILE_PATH, 'doctorList.txt')
    req = RawToPython(head)
    body_data = json.loads(req.body_data['data'])
    body_data['hasCard'] = "1" if HAS_CARD else "0"
    body_data['deptCode'] = department_id or DEPARTMENT
    req.set_param(req_param={"data": json.dumps(body_data)})
    req_data = req.requests(timeout=SLOW_TIMEOUT)
    docker_id = None
    for doctor in req_data.json()['result']['doctorList']:
        if doctor['doctorName'] == DOCTOR:
            docker_id = doctor['doctorId']
            _str = u'!!> get_docker_id: {}, {}, {}'.format(doctor['doctorName'], doctor['doctorId'], doctor['doctorProfession'])
            print imp_templ.format(_str)
        else:
            print u'--> get_docker_id:', doctor['doctorName'], doctor['doctorId'], doctor['doctorProfession']
    assert docker_id
    return docker_id


@save_file
def check_docker_date(department_id, doctor_id):
    head = os.path.join(FILE_PATH, 'doctorDateList.txt')
    req = RawToPython(head)
    body_data = json.loads(req.body_data['data'])
    body_data['hasCard'] = "1" if HAS_CARD else "0"
    body_data['deptCode'] = department_id or DEPARTMENT
    body_data['doctorId'] = doctor_id or DOCTOR
    req.set_param(req_param={"data": json.dumps(body_data)})
    req_data = req.requests(timeout=SLOW_TIMEOUT)
    is_allow = False
    for each in req_data.json()['result']['doctorDateList']:
        if each['date'] == DATE:
            _str = u'!!> get_docker_date_list: {}, {}'.format(DOCTOR, each['date'])
            print imp_templ.format(_str)
            is_allow = True
        else:
            print u'--> get_docker_date_list:', DOCTOR, each['date']
    return is_allow


@save_file
def check_docker_datetime(department_id, doctor_id):
    head = os.path.join(FILE_PATH, 'doctorDateTimeList.txt')
    req = RawToPython(head)
    body_data = json.loads(req.body_data['data'])
    body_data['hasCard'] = "1" if HAS_CARD else "0"
    body_data['deptCode'] = department_id or DEPARTMENT
    body_data['doctorId'] = doctor_id or DOCTOR
    body_data['date'] = DATE
    req.set_param(req_param={"data": json.dumps(body_data)})
    req_data = req.requests(timeout=SLOW_TIMEOUT)
    all_datetime = []
    for each in req_data.json()['result']['doctorDateTimeList']:
        if IS_DEBUG_TIME:
            each['status'] = 1
        if int(each['status']) == 1:
            print '-->check_docker_datetime: {}'.format(each['time'])
            all_datetime.append(each)
    return all_datetime


def get_good_time(all_datetime):
    if not all_datetime:
        return None, []
    all_datetime_map = {x['dateTime']: x for x in all_datetime}
    config_str_time = "{} {}:00".format(DATE, TIME)
    config_time = datetime.datetime.strptime(config_str_time, '%Y-%m-%d %H:%M:%S')
    if config_str_time in all_datetime_map:
        good_time = all_datetime_map[config_str_time]
        del all_datetime_map[config_str_time]
        return good_time, all_datetime_map.values()
    for n in range(240):
        s_time = config_time - datetime.timedelta(seconds=60*5*(1+n))
        e_time = config_time + datetime.timedelta(seconds=60*5*(1+n))
        for _time in all_datetime_map.keys():
            c_time = datetime.datetime.strptime(_time, '%Y-%m-%d %H:%M:%S')
            if s_time <= c_time <= e_time:
                print '--> get_good_time: {}'.format(c_time)
                good_time = all_datetime_map[_time]
                del all_datetime_map[_time]
                return good_time, all_datetime_map.values()
    good_time = all_datetime[0]
    return good_time, all_datetime[1:]


def submit(department_id, doctor_id, good_time):
    if good_time is None:
        print u'--> 没有可预约的时间, 终止请求'
        return 'none'
    if IS_DEBUG_SUBMIT:
        head = os.path.join(FILE_PATH, 'fake_submit.txt')
    else:
        head = os.path.join(FILE_PATH, 'submit.txt')
    req = RawToPython(head)
    body_data = json.loads(req.body_data['data'])
    body_data['hasCard'] = "1" if HAS_CARD else "0"
    body_data['deptCode'] = department_id or DEPARTMENT
    body_data['doctorId'] = doctor_id or DOCTOR
    body_data['date'] = DATE
    body_data['time'] = good_time['time']
    body_data['roomId'] = good_time['roomId']
    body_data['timeIndexNo'] = good_time['timeIndexNo']
    body_data['deptName'] = DEPARTMENT
    body_data['doctorName'] = DOCTOR
    req.set_param(req_param={"data": json.dumps(body_data)})
    try:
        req_data = req.requests(timeout=FAST_TIMEOUT)
        req_json = req_data.json()
        status_code = int(req_json['status'])
        if status_code == 200:
            print imp_templ.format(u'--> 成功抢到，请检查预')
            return 'success'
        elif status_code == 500:
            msg = req_json.get('responseMessage', '')
            if u'不能重复预约' in msg:
                print imp_templ.format(u'--> 成功抢到，请检查预')
                return 'success'
            print u'--> 未能抢到: ', req_json.get('responseMessage')
            return 'fail'
        print '--> submit: what?: ', req_json
        return 'what?'
    except Exception as e:
        print u'--> 抢注报错: ', e
        return 'error'


if __name__ == '__main__':
    replace_app_access_token()
    check_card_no(is_one=True)
    department_id = get_department_id()
    docker_id = get_docker_id(department_id)
    while True:
        is_allow = check_docker_date(department_id, docker_id)
        if is_allow:
            break
        time.sleep(1)
    all_datetime = check_docker_datetime(department_id, docker_id)
    good_time, all_datetime = get_good_time(all_datetime)
    while True:
        _type = submit(department_id, docker_id, good_time)
        if _type == 'success':
            break
        elif _type == 'fail':
            good_time, all_datetime = get_good_time(all_datetime)
        elif _type == 'none':
            break
        # elif _type == 'error':
        #     pass
        # elif _type == 'what?':
        #     pass
    check_card_no(is_one=False)
