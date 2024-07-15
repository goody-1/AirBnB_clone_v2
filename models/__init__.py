#!/usr/bin/python3
"""
This module initializes the storage system for the AirBnB clone project.

It checks the value of the environment variable 'HBNB_TYPE_STORAGE' to determine
the type of storage to use. If the value is set to 'db', it imports and uses the
DBStorage class from models.engine.db_storage module. Otherwise, it imports and
uses the FileStorage class from models.engine.file_storage module.

The storage object is then created and reloaded to load all the data from the
storage system.
"""
import os

storage_type = os.environ.get("HBNB_TYPE_STORAGE")

if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
