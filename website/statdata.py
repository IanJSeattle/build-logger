#!/usr/bin/python3

from collections import defaultdict
import datetime
import sqlite3 as sql
import json

def connect_db(filename):
    db = sql.connect(filename)
    return db

def get_total_hours(db):
    cursor = db.cursor()
    cursor.execute('select sum(hours) from events')
    return cursor.fetchone()[0]

def get_hours_by_month(db):
    cursor = db.cursor()
    cursor.execute('select date, hours from events')
    rawdata = cursor.fetchall()
    monthdata = defaultdict(float)
    for item in rawdata:
        date = '-'.join(item[0].split('-')[0:2])
        hours = item[1]
        monthdata[date] += hours
    return monthdata

def get_last_x_days(db, limit):
    """ retrieve hour data for the last limit days """
    fmt = "%Y-%m-%d %H:%M:%S"
    now = datetime.datetime.now().timestamp()
    seconds = limit * 24 * 60 * 60
    x_days_ago = datetime.datetime.fromtimestamp(now - seconds).strftime(fmt)
    cursor = db.cursor()
    query = f'select date, hours from events where date > "{x_days_ago}"'
    cursor.execute(query)
    rawdata = cursor.fetchall()
    return rawdata

def get_hours_by_day(db, limit):
    """ get hours by day for the last limit days """
    rawdata = get_last_x_days(db, limit)
    daydata = defaultdict(float)
    for item in rawdata:
        date = item[0].split(' ')[0]
        hours = item[1]
        daydata[date] += hours
    today = datetime.datetime.today()
    all_days = [(today - datetime.timedelta(days=x)).strftime("%Y-%m-%d")
                for x in range(limit)]
    for day in all_days:
        if not daydata[day]:
            daydata[day] = 0.0
    return daydata

def get_avg_daily(db, limit):
    """ get average daily hours for the last limit days """
    rawdata = get_last_x_days(db, limit)
    total_hours = 0
    for item in rawdata:
        total_hours += item[1]
    return total_hours / limit

def get_avg_overall(db):
    """ calculate the average hours-per-day over the course of the whole
    project, includig empty days """
    cursor = db.cursor()
    cursor.execute('select date from events order by date asc limit 1')
    first_date_str = cursor.fetchone()[0]
    date, time = first_date_str.split(' ')
    datelist = [int(item) for item in date.split('-')]
    timelist = [int(item) for item in time.split(':')]
    first_date = datetime.datetime(*datelist, *timelist)
    days = (datetime.datetime.now() - first_date).days
    total_hours = get_total_hours(db)
    return total_hours / days

def get_hours_by_category(db):
    cursor = db.cursor()
    cursor.execute('select category, hours from events')
    rawdata = cursor.fetchall()
    categories = defaultdict(float)
    for item in rawdata:
        cat = item[0]
        hours = item[1]
        categories[cat] += hours
    return categories

def get_hours_by_subcategory(db):
    cursor = db.cursor()
    cursor.execute('select category, subcategory, hours from events')
    rawdata = cursor.fetchall()
    subcats = defaultdict(lambda: defaultdict(float))
    for item in rawdata:
        cat = item[0]
        subcat = item[1]
        hours = item[2]
        subcats[cat][subcat] += hours
    return subcats
        
def main():
    filename = "charger-buildlog.sqlite"
    db = connect_db(filename)
    data = {}
    data['total_hours'] = get_total_hours(db)
    data['hours_by_month'] = get_hours_by_month(db)
    data['hours_last_30'] = get_hours_by_day(db, 30)
    data['avg_last_month'] = get_avg_daily(db, 30)
    data['avg_overall'] = get_avg_overall(db)
    data['hours_by_category'] = get_hours_by_category(db)
    data['hours_by_subcategory'] = get_hours_by_subcategory(db)

    print('Content-type: application/json\n\n')
    print(json.dumps(data))

if __name__ == '__main__':
    main()
