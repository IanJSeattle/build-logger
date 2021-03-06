#!/usr/bin/env python3
# vi: set wm=0 ai sw=4 ts=4 et:

"""
"""

import mysql.connector as dbcon
import datetime
import click

ORDER = ['date', 'activity', 'hours', 'primary_worker', 'additional_workers',
         'category', 'subcategory', 'cost', 'purchased', 'photo_url']

DBINFO = {'user': 'reaper', 'password': 'hello*', 'database': 'charger_buildlog'}


@click.command()
@click.option('--cost', '-c', 
              default = False,
              is_flag = True,
              help = 'Show only entries with a cost associated')
def main(cost):
    """
    """
    db = setup_db()
    data = get_data(db)
    print_data(data, cost)
    cleanup_db(db)


def print_data(data, cost_flag):
    total_hours = 0
    cat_hours = {}
    for item in data:
        hours = item[2]
        cat = item[5]
        cost = item[7]
        if cost_flag and cost == 0:
                continue
        total_hours += hours
        if cat in cat_hours:
            cat_hours[cat] += hours
        else:
            cat_hours[cat] = hours
        if cost_flag:
            print('{} [{} hrs]: ${} {}'.format(item[0].date(), 
                                               hours, 
                                               cost, 
                                               item[1]))
        else:
            print('{} [{} hrs]: {}'.format(item[0].date(), hours, item[1]))
        print()
    for cat in cat_hours:
        print('{} hours: {}'.format(cat, cat_hours[cat]))
    print('------')
    print('Total hours: {}'.format(total_hours))


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
    query = 'select * from events'
    cursor.execute(query)
    for item in cursor:
        items.append(item)
    return items

if __name__ == '__main__':
    main()
