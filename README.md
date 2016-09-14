# OsakaUniversityCourses

OsakaUniversityCourses is a web application for searching courses in a wiser way.

# Dependency

+ python-pip

# Installation

Install required packages.

```
pip -r requirement.txt
```

# Preparation

Fetch the latest information of courses

```
$ ./fetch_courses.py
```

# Start web application

Starting web server

```
$ ./manage.py runserver
```

+ Then open web browser to access

```
https://localhost:5001/
```

# How to use

Type any keywords in input field on the top of page. There are some reserved keyowords:

    * day
    * period
    * interval

Here are some examples:

    * `"Computer" -day:1`: Courses that name has "Computer" and not in Monday.
    * `"Computer" -period:5`: Courses that name has "Computer" and not in period 5
    * `Computer day:2`: Courses that name has "Computer" and in Tuesday.

# Screenshots

![](https://www.mkx.tw/static/image/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202016-09-14%2011.56.34.png)
