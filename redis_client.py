import json
import redis

class redis_client():

    conn = None
    host = "localhost"
    port = 6379

    def __init__(self, host=None, port=None):
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port

    def connect(self):
        try:
            conn = redis.StrictRedis(
                host=self.host,
                port=self.port,
            )
            print conn
            conn.ping()
            print "Redis DB Connected at host: {},  port: {}".format(self.host, self.port)
            self.conn = conn
        except Exception as ex:
            print "Error: ", ex
            exit("Failed to connect, terminating.")

    def set(self, key, value):
        if self.conn is None:
            return

        # check value data type
        if isinstance(value, dict):
            value = json.dumps(value)

        try:
            self.conn.set(key, value)
            return key
        except Exception as ex:
            print "Error: ", ex
            exit("Failed to insert, terminating.")

    def get(self, key):
        if self.conn is None:
            return

        try:
            return json.loads(self.conn.get(key))
        except Exception as ex:
            print "Error: ", ex
            exit("Failed to find, terminating.")