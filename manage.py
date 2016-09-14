#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__ = ' 5 21, 2016 '
__author__ = 'mkfsn'

from app import app, db
from app.models import Course
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='localhost', port='5001'))


if __name__ == '__main__':
    manager.run()
