import os
import re
import json
import requests
from fake_useragent import UserAgent
from redis_client import redis_client

def get_records(start_page=1, end_page=10, redis_db=None):
    ua = UserAgent()
    session = requests.Session()
    for page in range(start_page, end_page + 1):
        print "==============={}==============".format(str(page))
        req = session.get(
            "https://42floors.com/office-space/us/ca/san-francisco/{}?max=&min=&type=Lease&uses=17".format(str(page)),
            headers={"Content-Type": "application/json", "User-agent": str(ua.chrome)}
        )
        text = req.text
        divs = re.findall('<div class="uniformRow uniformRow-listing "(.+?)>', text)
        old_divs = re.findall('<div class="uniformRow uniformRow-listing  archived"(.+?)>', text)
        divs = divs + old_divs
        for div in divs:
            link = re.findall('data-href="(.+?)"', div)[0]
            address = re.findall('/us/ca/san-francisco/(.+?)\\?listing', link)[0]
            redis_id = re.findall('listings=(.*)', link)[0]
            link = "https://42floors.com{}".format(link)
            lat = re.findall('data-latitude="(.+?)"', div)[0]
            lng = re.findall('data-longitude="(.+?)"', div)[0]
            req = session.get(
                link,
                headers={"Content-Type": "application/json", "User-agent": str(ua.chrome)}
            )
            text = req.text
            size = re.findall('<div class="size col-md-3">\n                (.+?) sqft', text)
            rate = re.findall('<meta itemprop="price" content="(.+?) USD', text)
            unit = re.findall('<div class="secondary">(.+?)</div>\n', text)
            
            if len(size) > 1 or len(size) == 0:
                continue
            else:
                size = float(size[0].replace(",", ""))
            
            if len(rate) == 1:
                rate = float(rate[0].replace(",", ""))
            elif len(rate) == 0:
                rate = 0.0
            else: continue

            if len(unit) >= 1:
                unit = unit[0]
            else:
                unit = "unknown"

            if unit == "/mo":
                rate = rate * 12 / size

            print link, address, redis_id
            # print size, rate, unit
            # print float(lat), float(lng)

            redis_db.set(redis_id, {
                "rate": rate,
                "address": address,
                "geo": {
                    "lat": float(lat),
                    "lng": float(lng)
                }
            })

def main():
    redis_db = redis_client()
    redis_db.connect()

    print "searching for all the retail rentals in SF from 42floors"
    get_records(1, 8, redis_db)

if __name__ == "__main__":
    main()