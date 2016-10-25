#!/bin/python3
import sqlite3 as sq

def generate_html(s):
    i=s.path.find('?')
    id=s.path[i+1+len('id='):]

    with sq.connect(s.dbs) as conn:
        c=conn.cursor()
        c.execute('DELETE FROM alldata WHERE id={}'.format(id))
        conn.commit()
    
    return ['/index.html']
