import fire
import json
import numpy as np
from importlib import import_module
import time
import os
import sys
import inspect

LOGO = """
\x1B[38;5;232m    :::       ::: ::::::::   :::::::::: :::    ::: ::::::::::: ::::::::  ::::::::   :::::::::  :::::::: 
\x1B[38;5;236m   :+:       :+: :+:    :+: :+:        :+:   :+:      :+:    :+:    :+: :+:    :+: :+:    :+: :+:    :+: 
\x1B[38;5;238m  +:+       +:+ +:+    +:+ +:+        +:+  +:+       +:+    +:+    +:+ +:+    +:+ +:+    +:+ +:+    +:+  
\x1B[38;5;240m +#+  +:+  +#+ +#++:++#:  +#++:++#   +#++:++        +#+    +#+    +:+ +#++:++#:  +#+    +:+ +#++:++#+    
\x1B[38;5;242m+#+ +#+#+ +#+ +#+    +#+ +#+        +#+  +#+       +#+    +#+    +#+ +#+    +#+ +#+    +#+ +#+    +#+    
\x1B[38;5;244m#+#+# #+#+#  #+#    #+# #+#        #+#   #+#      #+#    #+#    #+# #+#    #+# #+#    #+# #+#    #+#     
\x1B[38;5;246m###   ###   ###    ### ########## ###    ###     ###     ########  ###    ### #########  #########       \x1B[0m
"""

def print_supported_actions(db_type):
    print(f"Supported actions for {db_type}:")

    # Try to dynamically import the db_type module
    try:
        db_module = import_module(f'dbs.{db_type}')
    except ModuleNotFoundError:
        print(f"Database type '{db_type}' not found!")
        return
    
    # if __actions__ is defined, print the actions
    function_list = sorted([name for name, obj in inspect.getmembers(db_module) if inspect.isfunction(obj)])

    for func in function_list:
        print(f"    {func}")
        
def main(db_type, action=None, **kwargs):
    # Try to dynamically import the db_type module
    try:
        db_module = import_module(f'dbs.{db_type}')
    except ModuleNotFoundError:
        print(f"Database type '{db_type}' not found!")
        return
    
    # if no action specified, print the functions defined in db_type
    if action is None:
        print_supported_actions(db_type)
        return
    
    # check if any kwargs are specified.  if not, or if the only kwarg is "help", print the function's docstring
    try:
        func = getattr(db_module, action)
    except AttributeError:
        print_supported_actions(db_type)
        return

    if len(kwargs) == 0 or (len(kwargs) == 1 and "help" in kwargs):
        print(func.__doc__)
        return

    # create filename based on db_type and timestamp if filename in kwargs isn't specified
    if "filename" not in kwargs:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        kwargs.update({"filename": f"{db_type}_{action}_{timestamp}.json"})

    # check whether the filename exists.  if so, confirm with the user.
    filename = kwargs["filename"]
    if os.path.exists(filename):
        print(f"File {filename} already exists.  Overwrite? (y/n)", end=" ")
        response = input()
        if response.lower() != "y":
            print("Aborting...")
            return

    # Check if the action exists in the module
    if not hasattr(db_module, action):
        print(f"Action '{action}' not found in {db_type}!")
        return

    # Call the function
    func = getattr(db_module, action)
    result = func(**kwargs)

    print()
    print("Done. Have a nice day >:)")

def print_supported_dbs():
    print("Supported databases:")

    supported_dbs = []
    for db in os.listdir(os.path.join(os.path.dirname(__file__), "dbs")):
        if db.endswith(".py"):
            supported_dbs.append(f"{db[:-3]}")
    
    for db in sorted(supported_dbs):
        print(f"    {db}")

if __name__ == "__main__":
    # if no args specified, print supported dbs and usage
    if len(sys.argv) == 1:
        print(LOGO)
        print("Usage: \033[92mwrektordb\033[0m \033[91m<db_type> <args>\033[0m")
        print()
        print("Example: wrektordb weaviate dump --hostname localhost --port 8080 --filename weaviate_dump.json")
        print()
        print_supported_dbs()

        exit(0)

    fire.Fire(main)