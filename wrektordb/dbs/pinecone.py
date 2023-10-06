import json
import numpy as np
import pinecone

# all possible envs for pinecone.
# grabbed from https://docs.pinecone.io/docs/projects as of 2023-09/06
PINECONE_ENVS = ["us-west1-gcp-free",
                "gcp-starter",
                "asia-southeast1-gcp-free",
                "us-west4-gcp-free",
                "us-west1-gcp",
                "us-central1-gcp",
                "us-west4-gcp",
                "us-east4-gcp",
                "northamerica-northeast1-gcp",
                "asia-northeast1-gcp",
                "asia-southeast1-gcp",
                "us-east1-gcp",
                "eu-west1-gcp",
                "eu-west4-gcp",
                "us-east-1-aws",
                "eastus-azure"]

def try_connect(api_key):
    """
    Try to connect to a Pinecone instance.  Returns the environment if successful, None otherwise.
    """

    # if the env is none, we have to keep trying until we get a successful connection.
    print(f"    Searching for env associated with api key...")
    successful_connection = False
    for env in PINECONE_ENVS:
        print(f"    [-] Trying env {env}...")
        try:
            pinecone.init(api_key=api_key, environment=env)

            # check indices.  if it works, we know we have the right env
            indices = pinecone.list_indexes()

            successful_connection = True

            break
        except:
            continue

    if not successful_connection:
        print(f"Could not connect to Pinecone instance.")
        return None
    else:
        return env

def dump(api_key, filename, env=None, random_queries=10):
    """
    Dump all data from a Pinecone Cloud instance to a file.

    Usage:
        wrektordb pinecone dump --api_key <api_key> --env <env> --filename <filename>

    Arguments:
        api_key: The API key to use to connect to the Pinecone Cloud instance.
        filename: The filename to dump the data to. Optional; will default to pinecone_dump_<timestamp>.json
        env: The environment to connect to.  Optional; if none specified, will try all environments until one works.
    """

    # if the env is none, we have to keep trying until we get a successful connection.
    print(f"Connecting to Pinecone instance...")
    successful_connection = False
    if env is None:
        env = try_connect(api_key)
        if env is None:
            return
    else:
        try:
            pinecone.init(api_key=api_key, environment=env)
        except Exception as e:
            print(f"Could not connect to pinecone instance: {e}")
            return

    # we have a successful connection.  dump all data from pinecone
    print(f"    [-] Connected to Pinecone at env {env}.  Dumping all data...")

    results = []

    print(f"    Dumping all documents to {filename}...")

    print("    Listing indices...")
    results = dict()
    for index_name in pinecone.list_indexes():
        print(f"        Dumping index {index_name}...")

        index = pinecone.Index(index_name)
        stats = index.describe_index_stats()
        dimension = stats.dimension

        # create a bunch of random query vectors
        for i in range(random_queries):
            query_vector = np.random.randn(dimension).tolist()
            query_result = index.query(vector=query_vector, top_k=1000)

            # parse query result
            for match in query_result['matches']:
                id = match['id']
                score = match['score']
                if id not in results:
                    results[id] = dict()
                results[id][index_name] = score

    # pretty-print this
    with open(filename, "w") as f:
        f.write(json.dumps(results, indent=2))
    
