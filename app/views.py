#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__ = ' 4 10, 2016 '
__author__ = 'mkfsn'


import re
from flask import render_template
from flask import jsonify
from flask import request
from sqlalchemy.sql import func
from sqlalchemy.sql import label


from app import app, db
from app.models import Course
from app.models import Time
from app import babel
from config import LANGUAGES


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/autocomplete/course', methods=['GET'])
def autocomplete_course():
    query = request.args.get('query').strip().rstrip()
    return jsonify(result=Course.distinct(query))


@app.route('/chart', methods=['GET'])
def chart():
    import json
    data = db.session.query(Course.ClassAffiliation,
                            label('Count', func.count(Course.ClassCode))) \
                     .group_by(Course.ClassAffiliation).all()
    return render_template('chart.html', data=json.dumps(data))


def parse_query(query):
    dayofweek = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    keywords = {
        'title': '((?:[^\s\'"]+)|(?:[\'"].+?[\'"]))',
        'day': "(\d+)",
        'period': "(\d+)",
        'interval': ('('
                     '(?:' + '|'.join(['(?:%s)' % i for i in dayofweek]) + ')'
                     '\d'
                     '(?:(?:..\d)|(?:(?:,\d)*))'
                     ')'),
        'instructor': '((?:[^\s\'"]+)|(?:[\'"].+?[\'"]))'
    }
    app.logger.info(keywords)

    filtered = {k: [] for k in keywords.keys()}
    specified = {k: [] for k in keywords.keys()}
    for keyword, expression in keywords.items():
        pattern = r'(-?)%s:%s' % (keyword, expression)
        for matched in re.findall(pattern, query, flags=re.IGNORECASE):
            if matched[0] == '-':
                filtered[keyword].append(matched[1])
            else:
                specified[keyword].append(matched[1])
            query = re.sub(pattern, '', query)

    return query.strip().rstrip(), filtered, specified


@app.route('/course', methods=['GET'])
def course():
    query = request.args.get('query')
    query, filtered, specified = parse_query(query)
    app.logger.info("Query: [%s]" % query)
    app.logger.info("Filtered: [%s]" % filtered)
    app.logger.info("Specified: [%s]" % specified)
    if query == "" and \
            sum([len(i) for i in filtered]) == 0 and \
            sum([len(i) for i in specified] == 0):
        return jsonify(courses=[])

    conditions = (
        (Course.ClassCode == query) |
        Course.Name.contains(query) |
        Course.Name_English.contains(query) |
        Course.Instructor.contains(query)
    )

    # TODO: filter title, interval
    for s in filtered['interval']:
        app.logger.info(s)

    for s in specified['instructor']:
        _name = re.sub(r'^"|"$', '', s)
        conditions &= (Course.Instructor.ilike(u'%{0}%'.format(_name)))

    for s in filtered['instructor']:
        _name = re.sub(r'^"|"$', '', s)
        conditions &= ~(Course.Instructor.ilike(u'%{0}%'.format(_name)))

    for s in specified['day']:
        conditions &= (Course.ClassTime.any(Time.Day == int(s)))

    for s in filtered['day']:
        conditions &= ~(Course.ClassTime.any(Time.Day == int(s)))

    for s in specified['period']:
        conditions &= (Course.ClassTime.any(Time.Period == int(s)))

    for s in filtered['period']:
        conditions &= ~(Course.ClassTime.any(Time.Period == int(s)))
 
    courses = Course.query.join(Time).filter(conditions).all()
    return jsonify(courses=[c.to_dict() for c in courses])


@app.route("/autocomplete/courses/beta", methods=['GET'])
def autocomplete_course_beta():
    query = request.args.get('query')
    app.logger.debug(query)
    conditions = (
        Course.Name.contains(query) |
        Course.Name_English.contains(query)
    )
    conditions &= ~Course.Instructor.contains('watanabe')
    courses = Course.query.filter(conditions).all()
    return jsonify(courses=[c.to_dict() for c in courses])


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
