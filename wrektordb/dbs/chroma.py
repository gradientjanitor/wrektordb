import json
from tqdm import tqdm

def dump(hostname, port, filename):
    """
    Dump all data from a ChromaDB instance to a file.

    Usage:
        wrektordb chroma dump --hostname <hostname> --port <port> --filename <filename>

    Arguments:
        hostname: The hostname of the ChromaDB instance to connect to.
        port: The port of the ChromaDB instance to connect to.
        filename: The filename to dump the data to. Optional; will default to chroma_dump_<timestamp>.json
    """

    import chromadb

    print(f"Connecting to ChromaDB instance {hostname}:{port}...")

    try:
        # connect to the client.
        client = chromadb.HttpClient(host=hostname, port=port)

        # list all collections from client. we can't be sure we're connected until
        # we do this.
        collections = client.list_collections()
    except Exception as e:
        print(f"Could not connect to ChromaDB instance: {e}")
        return

    if len(collections) == 0:
        print("    No collections found.  Aborting...")
        return

    print(f"    Found {len(collections)} collections")
    print(f"    Dumping all documents to {filename}...")
    

    with open(filename, "w") as f:    
        all_docs = []

        for collection in collections:
            # get number of docs in the collection
            count = collection.count()

            # iterate over a batch of docs
            offset = 0
            limit = 100

            all_docs = []

            for offset in range(0, count, limit):
                print(f"        Dumping collection {collection.name}...")
                docs = collection.get(limit=limit, offset=offset)["documents"]

                if len(docs) < limit:
                    break
                
                all_docs.extend(docs)
            
        json.dump(all_docs, f, indent=2)

        