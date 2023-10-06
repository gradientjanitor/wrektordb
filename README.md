# Wrektordb: a cli tool for exploring vector dbs

# Why
There's a lot of vector db's out there, all of whom have their own schemas, APIs, ways to iterate over the data, etc. This tool aims to provide a common interface for exploring these dbs.

# Getting Started
The simplest way to get started is to run the tool in a docker container. First, build the dockerfile:
```
docker build -t wrektordb .
```

Then run the dockerfile:
```
docker run -it wrektordb
```

You'll be greeted with a friendly message showing you usage of the tool:
```
    :::       ::: ::::::::   :::::::::: :::    ::: ::::::::::: ::::::::  ::::::::   :::::::::  :::::::: 
   :+:       :+: :+:    :+: :+:        :+:   :+:      :+:    :+:    :+: :+:    :+: :+:    :+: :+:    :+: 
  +:+       +:+ +:+    +:+ +:+        +:+  +:+       +:+    +:+    +:+ +:+    +:+ +:+    +:+ +:+    +:+  
 +#+  +:+  +#+ +#++:++#:  +#++:++#   +#++:++        +#+    +#+    +:+ +#++:++#:  +#+    +:+ +#++:++#+    
+#+ +#+#+ +#+ +#+    +#+ +#+        +#+  +#+       +#+    +#+    +#+ +#+    +#+ +#+    +#+ +#+    +#+    
#+#+# #+#+#  #+#    #+# #+#        #+#   #+#      #+#    #+#    #+# #+#    #+# #+#    #+# #+#    #+#     
###   ###   ###    ### ########## ###    ###     ###     ########  ###    ### #########  #########       

Usage: wrektordb <db_type> <args>

Example: wrektordb weaviate dump --hostname localhost --port 8080 --filename weaviate_dump.json

Supported databases:
    chroma
    elastic
    milvus
    pinecone
    qdrant
    redis
    weaviate
```

All database implementations currently have a "dump" method that will iterate over the contents of the vectordb, and dump the contents to a file. The file will be saved in the current directory, and will be named after the database type and marked with a timestamp. For example, if you run the following command:
```
docker run -v $(pwd):/app -it wrektordb chroma dump --hostname localhost --port 8080
```
it will dump the contents of the ChromaDB instance to a file called `chroma_dump_yyyymmdd-hhmmss.json` in your current directory.

All commands are designed to be as friendly as possible, printing out function docstrings when an insufficient number of arguments are provided, and attempts are made to print out a helpful error message when an invalid arguments is provided.

# Example Usage
Say you come across a ChromaDB instance and want to explore it. You can run the following command:

```
docker run -v $(pwd):/app -it wrektordb chroma dump --hostname localhost --port 8080 --filename chroma_dump.json
```

This will dump the document contents of the ChromaDB instance to a file called `chroma_dump.json` in your current directory.

# Supported Databases & Adding Functionality
Currently, the following databases are supported:
- ChromaDB
- ElasticSearch
- Milvus
- Pinecone
- Qdrant
- Redis
- Weaviate

Adding functionality for a new vector database is as simple as dropping a new .py file in wrecktordb/dbs and implementing a function to dump the contents of the db to a file. Canonically, each .py file in the dbs/ directory implements a "dump" function. However, if you'd like to implement a reconnaissance function that prints out information about the database (eg., number of collections, number of records, etc), or any additional functionality, it can easily be called with:
```
wrektordb <new_db> <new_functionality>
```

# Disclaimer
This tool is for educational purposes only. Please do not use this tool to do anything illegal. I am not responsible for any misuse of this tool.