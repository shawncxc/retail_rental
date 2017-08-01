from redis_client import redis_client

size = 0
med = 0
avg = 0
data = []
redis_db = redis_client()
redis_db.connect()
heatmap_data = []
for key in redis_db.conn.scan_iter():
    temp = redis_db.get(key)
    rate = temp["rate"]
    if rate == 0 or rate > 1000 or rate < 10: continue
    size = size + 1
    avg = avg + rate
    data.append(rate)

data.sort()
high = data[size - 2] # remove the highest
low = data[1] # remove the lowest
avg = (avg - low - high) / size
med = data[size / 2]

print "total data size: {}".format(str(size))
print "high: {}".format(str(high))
print "low: {}".format(str(low))
print "avg: {}".format(str(avg))
print "med: {}".format(str(med))

print "==========================="
high_count = 0
low_count = 0
for key in redis_db.conn.scan_iter():
    temp = redis_db.get(key)
    rate = temp["rate"]
    if rate == 0: continue
    if rate > 1000:
    	print "high =>", key, rate
    	high_count = high_count + 1
    if rate < 10:
    	print "low =>", key, rate
    	low_count = low_count + 1

print "crazy high rate: {}".format(str(high_count))
print "crazy low rate: {}".format(str(low_count))