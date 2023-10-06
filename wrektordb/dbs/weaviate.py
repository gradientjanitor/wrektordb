import json

def dump(url, filename, api_key=None):
    """
    Dump all data from a Weaviate instance to a file.

    Usage:
        wrektordb weaviate dump --url <url> --api-key <api-key> --filename <filename>

        Arguments:
            url: The URL of the Weaviate instance to connect to.
            api-key: The API key to use to connect to the Weaviate instance. (Optional if no auth is required)
            filename: The filename to dump the data to. Optional; will default to weaviate_dump_<timestamp>.json
    """

    # Retrieve data
    import weaviate

    def get_batch_with_cursor(client, class_name, batch_size, cursor=None):
        query = (
            client.query.get(class_name)
            .with_additional(["id"])
            .with_limit(batch_size)
        )

        if cursor is not None:
            return query.with_after(cursor).do()
        else:
            return query.do()
    
    print(f"Connecting to Weaviate instance {url}...")
    try:
        client = weaviate.Client(url=url, auth_client_secret=api_key)
    except Exception as e:
        print(f"Could not connect to Weaviate instance: {e}")
        return

    all_uuids = []

    print(f"    Dumping all documents to {filename}...")

    batch_size = 20
    for a_class in client.schema.get()['classes']:
        class_name, class_properties = a_class['class'], a_class['properties']

        print(f"        Dumping class {class_name}...")

        cursor = None
        class_schema = client.schema.get(class_name)
        
        # Batch import all objects to the target instance
        while True:
            # From the SOURCE instance, get the next group of objects
            results = get_batch_with_cursor(client, class_name, batch_size, cursor)

            # put a pdb in here so we can inspect the results
            # import pdb; pdb.set_trace()

            for r in results["data"]["Get"][class_name]:
                all_uuids.append(r["_additional"]["id"])

            # If empty, we're finished
            if len(results["data"]["Get"][class_name]) == 0:
                break

            # Update the cursor to the id of the last retrieved object
            cursor = results["data"]["Get"][class_name][-1]["_additional"]["id"]
    
    all_results = []
    for uuid in all_uuids:
        obj = client.data_object.get(uuid)
        all_results.append(obj)

    with open(filename, "w") as f:
        f.write(json.dumps(all_results, indent=2))

