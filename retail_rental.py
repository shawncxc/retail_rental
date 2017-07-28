# http://www.cityfeet.com/cont/mapsearch

import os
import time
import requests
from fake_useragent import UserAgent
import json
from redis_client import redis_client

def isSanFrancisco(response):
    if "Location" in response:
        if "PropertyAddress" in response["Location"]:
            if "City" in response["Location"]["PropertyAddress"]:
                return response["Location"]["PropertyAddress"]["City"] == "San Francisco"
    return False

def getAddress(response):
    if "Location" in response:
        return response["Location"]["PropertyAddress"]["Address"]

def hasRate(response):
    if "Offer" in response:
        if "YearlyRentMinPerSf" in response["Offer"]:
            return True
    return False

def main():
    redis_db = redis_client()
    redis_db.connect()

    print "searching for all the retail rentals in SF"

    ua = UserAgent()

    session = requests.Session()
    req = session.post(
        "http://www.cityfeet.com/cont/api/search/listing-markers?height=379&width=1008",
        json={
            "location": {
                "name": "San Francisco, CA",
                "lat": 37.77304864698841,
                "lng": -122.41884563815209
            },
            "lt": 1,
            "partnerId": None,
            "pt": 4,
            "spatialBoundary": {
                "rect": [37.674633, -122.842429, 37.880325, -122.15029]
            },
            "term": "San Francisco, CA"
        },
        headers={"Content-Type": "application/json", "User-agent": str(ua.chrome)}
    )
    res = json.loads(req.text)["Data"]

    ids = []
    for ids_obj in res:
        ids = ids + ids_obj["Id"].split(",")

    print ids
    print "Found {} records of retail rentals".format(len(ids))

    for id in ids:
        req = session.get(
            "http://www.cityfeet.com/cont/api/listings/{}".format(id),
            headers={
                "X-Requested-With": "XMLHttpRequest",
                "User-agent": str(ua.chrome),
                "Cookie": "ASP.NET_SessionId=yx20ngzb0iiayby222iqd1zs; __RequestVerificationToken_L2NvbnQ1=LG0vg6Pft7K_JfdxMgJUjB5ZOVB1v5gFDUrzOrf6xDSNKkzhEc29S8bDrMxZVtMjQ_FwmAzM8ZW_t4_KOcONp7hz13w1; __gads=ID=381ce439b3775cb8:T=1500843877:S=ALNI_MZlNI0ceFgtFFjnsekWtSih2ZlH9Q; .CF=0ABAB907D25937458DA9A4410396F7A604286F6393032C9309D079698C7B880BEA49EF188C75C870E9BA098C14992FC4F8FC27D56282219BB9FE26C73CA0DC597F162327F560F18AC6ED7C1A18BE4FB69D6A209C6C451C76482EFCFE72042D7BC18034E2DC244582F8E7000BE7FC2CB536750CDC; _gat=1; optimizelySegments=%7B%7D; optimizelyBuckets=%7B%7D; optimizelyPendingLogEvents=%5B%5D; optimizelyEndUserId=oeu1500843837093r0.7755104035737768; _ga=GA1.2.1412147200.1500843837; _gid=GA1.2.1596952242.1501203239"
            }
        )
        res = json.loads(req.text)

        if isSanFrancisco(res):
            redis_id = "retail_rental_{}".format(id)
            rate = 0
            if hasRate(res):
                rate = res["Offer"]["YearlyRentMinPerSf"]
            address = res["Location"]["PropertyAddress"]["Address"]
            geo = res["Location"]["PropertyAddress"]["GeoLocation"]
            record = {
                "rate": rate,
                "address": address,
                "geo": geo
            }
            print record

            redis_db.set(redis_id, record)


if __name__ == "__main__":
    main()