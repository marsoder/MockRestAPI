#!/usr/bin/python


""" script that syncs riksdag database with app database.
    Scheduled by cron to run once each week. Stderr and stderr is redirected to a log file. 
"""

import sys
import os
import datetime

from . import syncfunctions
from .riksdagen import RiksClient
from RiksApp.models import Transcript

riks = RiksClient(size=100000)

current_count = syncfunctions.db_count

if __name__ == "__main__":
    print(syncfunctions.db_count())
    print(riks.count)

    time_now = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")

    if syncfunctions.synced(riks):
        print(f"{time_now}: Databases are synced")

    else:
        syncfunctions.sync(riks)
        c = current_count()
        print(f"{time_now}: Sync is successful!", f"current count is: {c}")


