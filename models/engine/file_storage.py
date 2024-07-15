#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import os


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""

        if cls:
            if cls is not str:
                cls = cls.__name__
            temp = {}
            for key, val in FileStorage.__objects.items():
                if key.split('.')[0] == cls:
                    temp[key] = val
            return temp
        return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f, indent=2)

    def reload(self):
        """Loads storage dictionary from file"""

        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                }

        if os.path.exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, 'r') as f:
                try:
                    temp = json.load(f)
                    for key, val in temp.items():
                        cls_name = val['__class__']
                        if cls_name in classes:
                            self.all()[key] = \
                                classes[cls_name](**val)
                except json.JSONDecodeError:
                    raise ValueError
                except FileNotFoundError:
                    pass

    def delete(self, obj=None):
        """Deletes an object (obj) from FileStorage.__objects"""

        if obj and obj in FileStorage.__objects.values():
            key_to_delete = None

            for key, value in FileStorage.__objects.items():
                if value == obj:
                    key_to_delete = key

            if key_to_delete:
                del FileStorage.__objects[key_to_delete]
                self.save()

    def close(self):
        """Close method"""
        self.reload()
