#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__ = ' 4 14, 2016 '
__author__ = 'mkfsn'


from app import db


class Course(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    InfoURL = db.Column(db.String)
    Name_English = db.Column(db.String)
    InfoURL_English = db.Column(db.String)
    ClassCode = db.Column(db.String, unique=True)
    ClassAffiliation = db.Column(db.String)
    Instructor = db.Column(db.String)
    DayAndPeriod = db.Column(db.String)
    Year = db.Column(db.Integer)
    Category = db.Column(db.String)
    AffiliationCode = db.Column(db.String)
    ClassTime = db.relationship('Time', backref='Course', lazy='dynamic')

    __tablename__ = 'Course'
    __table_args__ = (db.UniqueConstraint('ClassCode',
                                          'Year',
                                          name='YearlyCourse'),
                      dict(sqlite_autoincrement=True))

    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __eq__(self, other):
        return self.ClassCode == other.ClassCode and self.Year == other.Year

    def to_dict(self):
        return {
            'Name': self.Name,
            'InfoURL': self.InfoURL,
            'Name_English': self.Name_English,
            'InfoURL_English': self.InfoURL_English,
            'ClassCode': self.ClassCode,
            'ClassAffiliation': self.ClassAffiliation,
            'Instructor': self.Instructor,
            'DayAndPeriod': self.DayAndPeriod,
            'Year': self.Year,
            'Category': self.Category,
            'AffiliationCode': self.AffiliationCode
        }

    @classmethod
    def _get_distinct(self, attr, text):
        query = db.session.query(self.__getattribute__(self, attr)) \
                  .distinct(self.__getattribute__(self, attr)) \
                  .filter(self.__getattribute__(self, attr).contains(text)) \
                  .all()
        return [c.__getattribute__(attr) for c in query]

    @classmethod
    def distinct(self, text):
        if len(text) > 2:
            code = self._get_distinct("ClassCode", text)
        else:
            code = []
        name = self._get_distinct("Name", text)
        name_english = self._get_distinct("Name_English", text)
        instructor = self._get_distinct("Instructor", text)
        return code + name + name_english + instructor


class Time(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Cid = db.Column(db.Integer, db.ForeignKey('Course.Id'))
    Day = db.Column(db.Integer)
    Period = db.Column(db.Integer)

    __tablename__ = 'Time'
    __table_args__ = (dict(sqlite_autoincrement=True),)

    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])
