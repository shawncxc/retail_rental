from redis_client import redis_client

redis_db = redis_client()
redis_db.connect()

for key in redis_db.conn.scan_iter():
	print key