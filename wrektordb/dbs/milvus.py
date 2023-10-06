import json
import numpy as np
from pymilvus import (
    connections,
    utility,
    Collection,
)

class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyArrayEncoder, self).default(obj)

def dump(hostname=None, port=None, user=None, password=None, db_name=None, token=None, filename=None):
    """
    Dump all data from a Milvus instance to a file.

    Usage:
        wrektordb milvus dump --hostname <hostname> --port <port> --user <user> --password <password> --db-name <db-name> --token <token> --filename <filename>

    Arguments:
        hostname: The hostname of the Milvus instance to connect to.
        port: The port of the Milvus instance to connect to.
        user: The user to use to connect to the Milvus instance.
        password: The password to use to connect to the Milvus instance.
        db_name: The database name to use to connect to the Milvus instance.
        token: The token to use to connect to the Milvus instance.
        filename: The filename to dump the data to. Optional; will default to milvus_dump_<timestamp>.json
    """

    print(f"Connecting to Milvus instance. Configuration:")
    print(f"    hostname: {hostname}")
    print(f"    port: {port}")
    print(f"    user: {user}")
    print(f"    password: {password}")
    print(f"    db_name: {db_name}")
    print(f"    token: {token}")

    try:
        connections.connect("default", host=hostname, port=port, user=user, password=password, db_name=db_name, token=token)
    except Exception as e:
        print(f"Could not connect to Milvus instance: {e}")
        return

    print(f"    Dumping all documents to {filename}...")

    results = []

    print("    Listing collections...")
    for collection_name in utility.list_collections():
        print(f"        Dumping collection {collection_name}...")
        collection = Collection(collection_name)      # Get an existing collection.
        collection.load()

        output_fields = [c.name for c in collection.schema.fields]

        # return 5 results per page
        limit = 1000

        # create a query iterator
        query_iterator = collection.query_iterator(expr="", output_fields=output_fields, batch_size=limit)

        while True:
            # turn to the next page
            res = query_iterator.next()

            if len(res) == 0:
                # close the iterator
                query_iterator.close()
                break

            results.extend(res)
    
    # write results to a file
    with open(filename, "w") as f:
        f.write(json.dumps(results, cls=NumpyArrayEncoder))