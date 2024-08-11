import DBcm

db_details = "CoachDB.sqlite3"

from queries import *

def select_swimmers_event_(swimmer, age, session):
    with DBcm.UseDatabase(db_details) as db:
        db.execute(SQL_SWIMMERS_EVENTS_BY_SESSION, (swimmer, age, session,))
        return db .fetchall()
    