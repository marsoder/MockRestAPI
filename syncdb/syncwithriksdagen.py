#!/usr/bin/python
import sys
import os
import datetime
sys.path.insert(0, "..")
import syncfunctions
from models import Transcript
from riksdagen import RiksClient
riks = RiksClient(size=100000)

current_count = syncfunctions.db_count

if __name__ == "__main__":

    time_now = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")

    if syncfunctions.synced(riks):
        print(f"{time_now}: Databases are synced")

    else:
        syncfunctions.sync(riks)
        c = current_count()
        print(f"{time_now}: Sync is successful!", f"current count is: {c}")


