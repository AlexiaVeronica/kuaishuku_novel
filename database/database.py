import json
import os
from rich import print


def check_key_type(key, type_list: list):
    raise_count = 0
    for type_ in type_list:
        if not isinstance(key, type_):
            raise_count += 1
    if raise_count == len(type_list):
        raise TypeError('Key must be a {}:'.format(type_list), type(key))


class Database:
    def __init__(self, path, database_name):
        self.path = path
        self.database_name = database_name
        self.database = {}
        self.data = {}
        self.init_database()

    def init_database(self):
        if ".json" not in self.path:
            self.path += ".json"
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r', encoding='utf-8') as f:
                    self.database = json.load(f)
                    self.data = self.database.get(self.database_name)
                    if not self.data:
                        self.database[self.database_name] = {}
                        self.data = {}
                        self.save()
            except json.decoder.JSONDecodeError:
                self.database = {self.database_name: {}}
                self.data = self.database[self.database_name]
                self.save()
        else:
            self.database = {self.database_name: {}}
            self.data = self.database[self.database_name]
            self.save()

    def save(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.database, f, ensure_ascii=False, indent=4)  #

    def insert(self, key, value):
        if isinstance(value, int):
            value = str(value)
        if self.data.get(key):
            raise KeyError('Key already exists:', key)
        self.data[key] = value

    def insert_many(self, data):
        check_key_type(data, [list])
        for key, value in data:
            self.insert(key, value=value)

    def delete(self, key):
        check_key_type(key, [str])
        del self.data[key]
        self.save()

    def delete_many(self, data):
        check_key_type(data, [list])
        for key in data:
            self.delete(key)

    def update_one(self, key_name, key, value):
        check_key_type(key, [str])
        self.data[key_name][key] = value

    def update_many(self, key, new_data):
        if self.get(key=key):
            self.data[key] = new_data

    def get(self, key):
        if key.find('.') != -1:
            key_split = key.split('.')
            return_data = self.data.get(key_split[0])
            if return_data:
                for i in key_split[1:]:
                    try:
                        return_data = return_data[i]
                        if isinstance(return_data, str):
                            return_data = json.loads(return_data)
                    except KeyError as e:
                        print(e)
            return return_data
        return_data = self.data.get(key)
        if return_data is not None:
            return return_data

    def find_like(self, key_like):
        check_key_type(key_like, [str, int])
        return {key: value for key, value in self.data.items() if key_like in key}

    def find_all(self):
        return self.data
