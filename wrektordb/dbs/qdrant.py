import json

def dump(url, api_key, filename):
    """
    Dump all data from a Qdrant instance to a file.

    Usage:
        wrektordb qdrant dump --url <url> --api-key <api-key> --filename <filename>

    Arguments:
        url: The URL of the Qdrant instance to connect to.
        api-key: The API key to use to connect to the Qdrant instance.
        filename: The filename to dump the data to. Optional; will default to qdrant_dump_<timestamp>.json
    """
    from qdrant_client import QdrantClient

    try:
        client = QdrantClient(url=url, api_key=api_key)
        # list the collections
        collections = client.get_collections()
    except Exception as e:
        print(f"Could not connect to Qdrant instance: {e}")
        return

    print(f"    Dumping all documents to {filename}...")


    all_payloads = []
    for collection in collections.collections:
        print(f"        Dumping collection {collection.name}...")
        # scroll over an empty search to get everything
        for offset in range(0, 10, 100):
            resp = client.scroll(collection_name=collection.name, offset=offset, limit=100, with_payload=True, with_vectors=False)[0]

            payloads = [r.payload for r in resp]

            if len(payloads) == 0:
                break

            all_payloads.extend(payloads)

    with open(filename, "w") as f:
        json.dump(all_payloads, f)