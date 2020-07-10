import sys
import os
import datetime
import syncfunctions
from models import Transcript
from riksdagen import RiksClient
riks = RiksClient(size=11000)

current_count = syncfunctions.db_count
print(current_count())

if __name__ == "__main__":
    with open("sync-tracking.txt", "a") as f:
        if syncfunctions.synced(riks):
            print("is synced")
            time_now = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
            f.write(f"{time_now}: databases are synced\n")

        else:
            print("syncing")
            syncfunctions.sync(riks)
            c = current_count()
            print(f"Success!", f"current count is: {c}")
            
