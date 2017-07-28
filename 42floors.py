# https://42floors.com/office-space/us/ca/san-francisco/{page}?max=&min=&type=Lease&uses=17

import os
import re
import json
import requests
from fake_useragent import UserAgent
from redis_client import redis_client

def main():
    redis_db = redis_client()
    redis_db.connect()

    print "searching for all the retail rentals in SF from 42floors"

    ua = UserAgent()

    data = []

    session = requests.Session()
    req = session.get(
        "https://42floors.com/office-space/us/ca/san-francisco/1?max=&min=&type=Lease&uses=17",
        headers={"Content-Type": "application/json", "User-agent": str(ua.chrome)}
    )
    text = req.text
    divs = re.findall('<div class="uniformRow uniformRow-listing "(.+?)>', text)
    for div in divs:
        link = re.findall('data-href="(.+?)"', div)[0]
        lat = re.findall('data-latitude="(.+?)"', div)[0]
        lng = re.findall('data-longitude="(.+?)"', div)[0]
        print link, lat, lng
    
    # script_dir = os.path.dirname(__file__)
    # file_path = os.path.join(script_dir, './stocktwits.json')
    # with open(file_path, 'w+') as file:
    # 	json.dump(json_data['messages'], file)

 #    print "Found {} records of retail rentals".format(len(ids))

# data_email_pattern = re.compile(r'data-email="([^"]+)"')
# match = data_email_pattern.search(response.body)
# if match:
#     print(match.group(1))

# next level
# https://42floors.com/us/ca/san-francisco/835-kearny-st?listings=118040

if __name__ == "__main__":
    main()