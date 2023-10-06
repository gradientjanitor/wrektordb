import json
import random

import redis
from redisearch import Client, Query, TextField, NumericField, IndexDefinition


def dump(host, port, filename, password=None, ssl=None, ):
    """
    Dump all data from a Redis instance to a file.

    Usage:
        wrektordb redis dump --hostname <hostname> --port <port> --filename <filename>

    Arguments:
        hostname: The hostname of the Redis instance to connect to.
        port: The port of the Redis instance to connect to.
        filename: The filename to dump the data to. Optional; will default to redis_dump_<timestamp>.json
    """

    print(f"Connecting to Redis instance {host}:{port}...")
    try:
        r = redis.Redis(host=host, port=port, password=password, ssl=ssl)
    except Exception as e:
        print(f"Could not connect to Redis instance: {e}")
        return
        
    all_data = []
    for key in r.keys():
        key_type = r.type(key).decode()
        decoded_key = key.decode()
        if key_type == "string":
            key_value = r.get(key).decode() if r.get(key) else None
        if key_type == "hash":
            key_value = {k.decode(): v.decode() for k, v in r.hgetall(key).items()}
        elif key_type == "list":
            key_value = [v.decode() for v in r.lrange(key, 0, -1)]
        elif key_type == "set":
            key_value = [v.decode() for v in list(r.smembers(key))]
        elif key_type == "zset":
            key_value = [v.decode() for v in r.zrange(key, 0, -1)]

        all_data.append({"key": decoded_key, "type": key_type, "value": key_value})
    
    with open(filename, "w") as f:
        f.write(json.dumps(all_data))