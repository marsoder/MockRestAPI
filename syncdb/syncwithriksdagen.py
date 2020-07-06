import sys
import os
import syncfunctions

from riksdagen import RiksYearData

riks = RiksYearData(size=101)

if syncfunctions.synced(riks):
    print("synced")
    sys.exit(0)
else:
    missing_ids = syncfunctions.missing(riks)
    print(missing_ids)
    # syncfunctions.db_insert(riks.get_missing_ids())
    for x in riks.get_transcripts_urls(missing_ids):
        print(x)
    pass
