import sys
import os
import datetime
import syncfunctions
from models import Transcript
from riksdagen import RiksYearData

riks = RiksYearData(size=101)

# if syncfunctions.synced(riks):
#     print("synced")
#     sys.exit(0)
# else:
#     missing_ids = syncfunctions.missing(riks)
#     print(missing_ids)
#     # syncfunctions.db_insert(riks.get_missing_ids())
#     urls = set(riks.get_transcripts_urls(missing_ids))
#     syncfunctions.insert_db(urls)
#     print(Transcript.query.count())

if __name__ == "__main__":
    with open("sync-tracking.txt", "a") as f:
        if syncfunctions.synced(riks):

            time_now = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
            f.write(f"{time_now}: databases are synced\n")

        else:
            print("syncing")
            # syncfunctions.sync(riks)
            m = syncfunctions.missing(riks)
            missing_urls = riks.get_transcripts_urls(m)
            syncfunctions.insert_db(missing_urls)
            
            # print(syncfunctions.db_count())
