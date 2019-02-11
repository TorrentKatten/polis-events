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

