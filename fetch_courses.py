#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__ = ' 4 09, 2016 '
__author__ = 'mkfsn'


from pyquery import PyQuery as pq
import requests
import ConfigParser
import time
import json
import re
from app import db
from app.models import Course, Time


config = ConfigParser.ConfigParser()
config.read('defaults.cfg')
db.create_all()
db.session.commit()


def extract_day_period(content):
    day_of_week = {
        'jp': ['月', '火', '水', '木', '金', '土', '日'],
        'en': ['monday', 'tuesday', 'wednesday', 'thursday',
               'friday', 'saturday', 'sunday']
    }
    pattern = {
        'jp': '|'.join(['(%s)' % c for c in day_of_week['jp']]),
        'en': '|'.join(['(%s)' % c for c in day_of_week['en']])
    }
    match = {
        'jp': re.search(pattern['jp'], content),
        'en': re.search(pattern['en'], content, flags=re.IGNORECASE)
    }
    if match['jp'] is not None:
        m = match['jp'].group(0)
        content = re.sub('(%s)|(%s)' % (m, '限'), '', content)
        day = 1 + day_of_week['jp'].index(m)
        return [(day, int(i)) for i in re.findall("\d+", content)]
    elif match['en'] is not None:
        m = match['en'].group(0).lower()
        content = re.sub('(%s)|(%s)' % (m, 'Period'), '', content,
                         flags=re.IGNORECASE)
        day = 1 + day_of_week['en'].index(m)
        return [(day, int(i)) for i in re.findall("\d+", content)]
    else:
        return [(-1, -1)]


def decode_day_period(jp, en):
    if jp.find('　') != -1 and en.find('　') != -1:
        # 水 2限　木 2限 | Wednesday, Period 2　Thursday, Period 2
        jp_list, en_list = [jp.split('　'), en.split('　')]
        if len(jp_list) == len(en_list):
            day_period = []
            for i, v in enumerate(jp_list):
                day_period += decode_day_period(jp_list[i], en_list[i])
            return day_period

    elif (len(jp) == 8 and len(en) >= 16 and len(en) <= 19) or \
         (jp.count(',') > 0 and en.count(',') > 1):
        # 水 5限 | Wednesday, Period 5
        # 水 5限,6限 | Wednesday, Period 5,Period 6
        t = [extract_day_period(jp), extract_day_period(en)]
        if t[0] == t[1]:
            return t[0]

    elif len(jp) == 3 and len(en) == 5:
        return [(0, 0)]

    return [(-1, -1)]


def fetch(link, headers={}, payload={}, category='', code=''):
    r = requests.post(link, headers=headers, data=payload)
    rows = pq(r.text).find("table.search > tr")
    courses_info = [(i, j) for i, j in zip(rows[2:-1:2], rows[3:-1:2])]
    courses = []
    for info in courses_info:
        a, td = [pq(info[0]).find('a'), pq(info[1]).find('table tr td:eq(1)')]
        data = {
            'Name':             pq(a[0]).text(),
            'InfoURL':          pq(a[0]).attr('onclick')[17:-2],
            'ClassCode':        pq(td[0]).text(),
            'ClassAffiliation': pq(td[1]).text(),
            'Instructor':       pq(td[2]).text(),
            'DayAndPeriod':     pq(td[3]).text(),
            'Year':             int(payload['nendo']),
            'Category':         category,
            'AffiliationCode':  code
        }
        if len(a) > 1:
            data['Name_English'] = pq(a[1]).text()
            data['InfoURL_English'] = pq(a[1]).attr('onclick')[17:-2]
        else:
            data['Name_English'] = ''
            data['InfoURL_English'] = ''
        courses.append(Course(data))
    return courses


def dump_syllabus(headers, payload, department_list, db):

    link = 'https://koan.osaka-u.ac.jp/syllabus_ex/campus'
    headers['Referer'] = 'https://koan.osaka-u.ac.jp/syllabus_ex/campus'
    payload['func'] = 'function.syllabus.ex.refer.sogo.search'

    for category, affiliation in department_list.items():
        for a in affiliation:

            # Show status of fetching
            print a['Name']

            payload['category'] = category
            payload['s_j_s_cd'] = a['Code']
            courses = fetch(link, headers=headers, payload=payload,
                            category=a['Name'], code=a['Code'])
            for c in courses:
                if db.session.query(Course) \
                             .filter_by(ClassCode=c.ClassCode, Year=c.Year) \
                             .first():
                    continue
                db.session.add(c)
                db.session.flush()
                jp, en = c.DayAndPeriod.encode('utf-8').split('／')
                day_and_period = decode_day_period(jp, en)
                for day, period in day_and_period:
                    t = Time({'Cid': c.Id, 'Day': day, 'Period': period})
                    c.ClassTime.append(t)
                    db.session.add(t)
            db.session.commit()

            # Don't fetch too fast
            time.sleep(2)


if __name__ == '__main__':
    headers = {
        i: config.get('headers', i) for i in config.options('headers')
    }
    payload = {
        i: config.get('payload', i) for i in config.options('payload')
    }

    with open('CourseCategory.json') as data_file:
        department_list = json.load(data_file)

    dump_syllabus(headers, payload, department_list, db)
