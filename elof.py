import json
import requests as r
from collections import namedtuple

class PolisEvent:
    """En händelse från Polisens API."""


def larmslag_sammanfattning():
    purl = "https://polisen.se/api/events"
    svar = r.get(purl)
    foo = json.loads(svar.content, object_hook=lambda d: namedtuple('Event', d.keys())(*d.values()))

    bar = {}

    for i in foo:
        if i.type not in bar:
            bar[i.type] = 1
        else:
            bar[i.type] += 1

    for i,j in sorted(bar.items()):
        print(i,": ",j,"stycken")





# test med att konvertera tid
"""
datum = "2019-02-09 20:44:22 +01:00"
if ":" == datum[-3:-2]:
    datum = datum[:-3] + datum[-2:]   # Korrigera för att python har problem att konvertera alla ISO 8601 datumsträngar (https://stackoverflow.com/a/45300534).
d = datetime.strptime(datum,"%Y-%m-%d %H:%M:%S %z")
"""