#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__ = ' 4 14, 2016 '
__author__ = 'mkfsn'


from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babel import Babel


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
babel = Babel(app)


from app import views, models


LOGFILE = 'tmp/OsakaUniversityCourses.log'
LOGFORMAT = '%(asctime)s %(levelname)s: %(message)s [%(pathname)s:%(lineno)d]'


if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(LOGFILE, 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter(LOGFORMAT))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('OsakaUniversityCourses startup')
