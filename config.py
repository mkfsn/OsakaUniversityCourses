#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__ = ' 4 14, 2016 '
__author__ = 'mkfsn'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'osaka-u.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
# SQLALCHEMY_ECHO = True

LANGUAGES = {
    'en': 'English',
    'zh': '繁體中文',
    'ja': '日本語'
}
