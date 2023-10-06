from elasticsearch import Elasticsearch
import json

def dump(url, api_key, filename):
  """
    Dump all data from an Elasticsearch instance to a file.

    Usage:
        wrektordb elastic dump --url <url> --api-key <api-key> --filename <filename>

    Arguments:
        url: The URL of the Elasticsearch instance to connect to.
        api-key: The API key to use to connect to the Elasticsearch instance.
        filename: The filename to dump the data to. Optional; will default to elastic_dump_<timestamp>.json
  """
  print(f"Connecting to Elasticsearch instance {url}...")

  try:
    client = Elasticsearch(url, api_key=api_key)
  except Exception as e:
    print(f"Could not connect to Elasticsearch instance: {e}")
    return

  # Get information about all indices
  indices_info = client.indices.get(index='_all')
  print(indices_info)

  # Execute a search query
  search_body = {
    "query": {
        "match_all": {}
    }
  }

  results = client.search(index='_all', body=search_body, scroll='5m')

  scroll_id = results["_scroll_id"]

  # Iterate over the results
  with open(filename, "w") as f:
    for result in client.scroll(scroll_id=scroll_id, scroll='5m'):
        json.dump(result, f)