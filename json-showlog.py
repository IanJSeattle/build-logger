#!/usr/bin/env python3
# vi: set wm=0 ai sw=4 ts=4 et:

"""
"""

import mysql.connector as dbcon
import datetime
import json
import csv

ORDER = ['date', 'activity', 'hours', 'primary_worker', 'additional_workers',
         'category', 'subcategory', 'cost', 'purchased', 'photo_url']

DBINFO = {'user': 'reaper', 'password': 'hello*', 'database':
          'charger_buildlog', 'host': 'localhost'}



def main():
    """
    """
    db = setup_db()
    save_categories(db)
    data = get_data(db)
    save_data(data)
    cleanup_db(db)


def save_data(data):
    clean_data = []
    stat_data = []
    for item in data:
        clean_item = []
        for value in item:
            newvalue = value
            if type(value) not in [str, int, float]:
                newvalue = str(value)
            clean_item.append(newvalue)
        clean_data.append(clean_item)
        stat_item = clean_item[:]
        stat_item[1] = ''
        stat_data.append(stat_item)
    with open('data.json', 'w') as fstream:
        json.dump(clean_data, fstream)
    with open('stats.json', 'w') as fstream:
        json.dump(stat_data, fstream)


def setup_db():
    """
    set up and return a link to the db
    """
    db = dbcon.connect(**DBINFO)
    return db


def cleanup_db(db):
    db.close()


def get_data(db):
    """
    connect to the DB and download all the goo
    """
    cursor = db.cursor()
    items = []
    query = 'select * from events order by date'
    cursor.execute(query)
    for item in cursor:
        items.append(item)
    return items

def save_categories(db):
    """
    connect to the DB, get the category info, and save it as csv
    """
    header = ['name', 'subcategory_of']
    cursor = db.cursor()
    query = 'select * from subcategories'
    cursor.execute(query)
    items = [item for item in cursor]
    with open('subcategories.csv', 'w') as subcat:
        writer = csv.writer(subcat)
        writer.writerow(header)
        writer.writerows(items)

if __name__ == '__main__':
    main()
