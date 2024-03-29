#!/usr/bin/python
# - * - encoding: UTF-8 - * -
import sys
import os
import time

import pickle
import traceback

import datetime
from bs4 import BeautifulSoup

sys.path.extend(['/data/my_tools_env/my_tools/'])

from utils import tools
from utils.fiddler import RawToPython, FiddlerRequestTimeOutException

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

NEW_HOT_COUNT = 0
NEW_NEW_COUNT = 0

NEW_NEW_SAVE_COUNT = 10
NEW_HOT_SAVE_COUNT = 10

def test_print(*args, **kwargs):
    print args, kwargs


def change_url(url):
    removes = ['&fromguid=', '&extra=', '&mobile']
    for each in removes:
        index = url.find(each)
        if index != -1:
            url = url[:index]
            break
    return url + '&mobile=no'


def get_web_hot_data(request_raw, exist_titles=None):
    global NEW_HOT_COUNT
    if exist_titles is None:
        with open(os.path.join(CUR_DIR, 'z8_exist_hot_titles.txt')) as f:
            exist_titles = pickle.load(f)
    try:
        web_data = request_raw.requests(timeout=10)
    except FiddlerRequestTimeOutException:
        time.sleep(30)
        return {}, exist_titles
    except Exception as e:
        tools.send_error_msg_by_email("[zk8]get_web_data: " + traceback.format_exc())
        time.sleep(30)
        return {}, exist_titles
    exist_titles_set = set(exist_titles) if exist_titles else set()
    new_titles = []
    result = {}
    is_get_new = False
    if web_data and web_data.status_code == 200:
        soups = BeautifulSoup(web_data.text, "lxml")
        soup_find = soups.find(id='alist')
        if not soup_find:
            return {}, exist_titles
        print "Hot_Find-%s|" % len(soup_find.find_all('li')),
        for tag in soup_find.find_all('li'):
            text = tag.text.strip().split()
            if text:
                name = ' || '.join(text)
                if name not in exist_titles_set:
                    url = "http://www.zuanke8.com/" + tag.a.attrs['href']
                    url = change_url(url)
                    result[name] = url
                    is_get_new = True
                    new_titles.append(name)
    exist_titles_limit = (new_titles + exist_titles)[:1000]
    if is_get_new:
        NEW_HOT_COUNT += len(result)
        if NEW_HOT_COUNT > NEW_HOT_SAVE_COUNT:
            print "Hot_Saved-%s/%s|" % (NEW_HOT_COUNT, NEW_HOT_SAVE_COUNT),
            NEW_HOT_COUNT = 0
            with open(os.path.join(CUR_DIR, 'z8_exist_hot_titles.txt'), 'wb+') as f:
                pickle.dump(exist_titles_limit, f)
        else:
            print "Hot_Count-%s/%s|" % (NEW_HOT_COUNT, NEW_HOT_SAVE_COUNT),
    return result, exist_titles_limit


def get_web_data(request_raw, break_names=None):
    global NEW_NEW_COUNT
    if break_names is None:
        with open(os.path.join(CUR_DIR, 'z8_exist_new_titles.txt')) as f:
            break_names = pickle.load(f)
    try:
        web_data = request_raw.requests(timeout=10)
    except FiddlerRequestTimeOutException:
        time.sleep(30)
        return {}, break_names
    except Exception as e:
        tools.send_error_msg_by_email("[zk8]get_web_data: " + traceback.format_exc())
        time.sleep(30)
        return {}, break_names
    result = {}
    is_get_new = False
    if web_data and web_data.status_code == 200:
        soups = BeautifulSoup(web_data.text, "lxml")
        new_break_names = []
        set_break_names = set(break_names or [])
        soup_find = soups.find(id='alist')
        if not soup_find:
            return {}, break_names
        print "New_Find_%s|" % len(soup_find.find_all('li')),
        for tag in soup_find.find_all('li'):
            text = tag.text.strip().split()
            if text:
                name = ' || '.join(text[:-1])
                if name in set_break_names:
                    break
                else:
                    new_break_names.append(name)
                    is_get_new = True
                url = "http://www.zuanke8.com/" + tag.a.attrs['href']
                url = change_url(url)
                result[name] = url
        new_break_names.extend(break_names)
    else:
        new_break_names = break_names
    break_names = new_break_names[:50]
    if is_get_new:
        NEW_NEW_COUNT += len(result)
        if NEW_NEW_COUNT > NEW_NEW_SAVE_COUNT:
            print "New_Saved-%s/%s|" % (NEW_NEW_COUNT, NEW_NEW_SAVE_COUNT),
            NEW_NEW_COUNT = 0
            with open(os.path.join(CUR_DIR, 'z8_exist_new_titles.txt'), 'wb+') as f:
                pickle.dump(break_names, f)
        else:
            print "New_Count-%s/%s|" % (NEW_NEW_COUNT, NEW_NEW_SAVE_COUNT),
    return result, break_names


CHANGE_MAPS = {u'〇': '0', u'零': '0', u'一': '1', u'二': '2', u'三': '3', u'四': '4',
               u'五': '5', u'六': '6', u'七': '7', u'八': '8', u'九': '9', u'十': '10',
               u'百': '100', u'千': '1000', u'万': '10000', u'０': '0', u'１': '1',
               u'２': '2', u'３': '3', u'４': '4', u'５': '5', u'６': '6', u'７': '7',
               u'８': '8', u'９': '9', u'壹': '1', u'贰': '2', u'叁': '3', u'肆': '4',
               u'伍': '5', u'陆': '6', u'柒': '7', u'捌': '8', u'玖': '9', u'拾': '10',
               u'佰': '100', u'仟': '1000', u'萬': '10000', u'亿': '100000000'}


def change_title(title):
    new_title = title.strip().replace(' ', '').replace('||', '').lower()
    for i in title:
        if i in CHANGE_MAPS:
            new_title = new_title.replace(i, CHANGE_MAPS[i])
    return new_title


def init():
    tools.send_push = test_print
    with open(os.path.join(CUR_DIR, 'z8_exist_new_titles.txt'), 'wb+') as f:
        pickle.dump([], f)
    with open(os.path.join(CUR_DIR, 'z8_exist_hot_titles.txt'), 'wb+') as f:
        pickle.dump([], f)


def custom_send_push(title, url):
    tools.send_push(
        u'[ZK8]' + title, url,
        's-70924c26-f3a5-4292-ad29-fb1b5877',
        'g-85ed11d8-f448-4e41-bc1c-0e600f94',
        'ZK8-New')


def custom_send_push_hot(title, url):
    tools.send_push(
        u'[ZK8][Hot]' + title, url,
        's-0d7dbf26-0156-4bc2-a7eb-bbb53bc5',
        'g-7465ca67-140a-4f78-8f38-5226f84b',
        'ZK8-Hot')


if __name__ == '__main__':
    # init()
    break_names = None
    exist_titles = None
    important_key_messages = {'wj', 'bug', 'fx', u'10000家', u'斐讯', u"有水", u"水了",
                              u"大水", u"洪水", u"水到", u'好价', u'漏洞', u'黄金', u'洞',
                              u'首发', 'ruan', u'软件', u'速来', u'快去', u'手慢无',
                              u'神券', u'神卷', u'无门槛', u'毛', u'速度', u'速领', u'速撸',
                              u'好用'}
    key_messages = {u'神', u'券', u'卷', u'抢', u'立减',
                    u'防身', u'性价比', u'便宜', u'秒杀',
                    u'秒到', u'可以了', u'有货', u'防身',
                    u'利器', u'又有', u'来了', u'又1', u'免费', u'0元', u'震惊',
                    u'1元', u'9.9', u'9块9', u'9元', u'超级返', u'线报', u'高返',
                    u'高反', u'有货', u'活动', u'白菜', u'免单', u'到手', u'大妈',
                    u'美滋滋', u'果', u'菓', u'整理', u'一抖'}
    exclude_key_messages = {u'赚神', u'求', u'有没有', u'吗', u'呢', u'么', u'收', u'返现',
                            u'推荐办', u'油锅', u'代下', u'带下', u'三网',
                            u'助力', u'点赞', u'秒审', u'代刷', u'售'}
    new_list_request_raw = RawToPython(os.path.join(CUR_DIR, 'z8_new_list_head.txt'))
    hot_list_request_raw = RawToPython(os.path.join(CUR_DIR, 'z8_hot_list_head.txt'))
    count = 1
    email_title = '[ZK8] Many Titles Need To Send By E-mail'
    email_msg_tmp = u"【{}】 - {}\r\n\r\n"
    while True:
        result, break_names = get_web_data(new_list_request_raw, break_names)
        for title, url in result.iteritems():
            if_title = change_title(title)
            for i_k in important_key_messages:
                if i_k in if_title:
                    custom_send_push('[.]' + title, url)
                    print "Send_Important_New|",
                    break
            else:
                for k in key_messages:
                    if k in if_title:
                        for ek in exclude_key_messages:
                            if ek in if_title:
                                break
                        else:
                            custom_send_push(title, url)
                            print "Send_New|",
                            time.sleep(1)
                        break
        print "Refresh|%s|" % datetime.datetime.now()
        time.sleep(8)

        count += 1
        if count == 10:
            result, exist_titles = get_web_hot_data(hot_list_request_raw, exist_titles)
            count = 1
            if len(result) > 5:
                email_msg = ""
                for title, url in result.iteritems():
                    email_msg += email_msg_tmp.format(title, url)
                tools.send_email(email_title, email_msg)
                print "Send_All_Hot-%s|" % len(result),
                continue
            for title, url in result.iteritems():
                custom_send_push_hot(title, url)
                print "Send_Hot|",
                time.sleep(1)
            time.sleep(8)
            print "Refresh_Hot|%s|" % datetime.datetime.now()
        sys.stdout.flush()
