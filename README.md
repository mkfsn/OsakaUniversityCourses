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

And then open web browser to access

```
https://localhost:5001/
```

# How to use

Type any keyword in input field on the top of page.

There are some reserved keyowords:

* day
* period
* interval
* instructor

Here are some examples:

* Courses that name contains "Computer" but not in Monday and Friday.

    `"Computer" -day:1 -day:5`

* Courses that name contains "Computer" and is in period 5

    `"Computer" period:5`

* Courses that name contains "Computer" and is in Monday period 2 to 5.

    `Computer interval:mon2..5`

* Courses that name contains "Computer" but not in Friday period 1, 3 and 5.

    `Computer -interval:fri1,3 -interval:fri5`

* Courses that name contains "Computer" and the name of instructor contains "SUGIHARA".

    `Computer instructor:SUGIHARA`


# Screenshots

![](https://www.mkx.tw/static/image/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202016-09-14%2011.56.34.png)
