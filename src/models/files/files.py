import uuid
import datetime
from src.common.database import Database
import src.models.files.constants as Filesconstants


class Files(object):

    def __init__(self, name, _id=None, grid_id=None, upload_time=None):
        self.name = name
        self._id = _id if _id else Files.set_id()
        self.grid_id = grid_id
        self.upload_time = upload_time if upload_time else datetime.datetime.now()

    @staticmethod
    def set_id():
        return uuid.uuid4().hex

    def json(self):
        return {
            'name': self.name,
            'grid_id': self.grid_id,
            '_id': self._id,
            'upload_time': self.upload_time
        }

    def save_to_mongo(self):
        Database.update(Filesconstants.COLLECTION, {'_id': self._id}, self.json())

    @staticmethod
    def save_to_gridfs(file, filename):
        return Database.send_to_gridfs(filename, file)

    @staticmethod
    def create_and_save_gridfs(file):
        file_obj = Files(file.filename)
        grid_id = Files.save_to_gridfs(file, file.filename)
        if grid_id:
            file_obj.grid_id = grid_id
            file_obj.save_to_mongo()

    @classmethod
    def find_by_id(cls, _id):
        return cls(**Database.find_one(Filesconstants.COLLECTION, {'_id':_id}))

    @classmethod
    def get_all_files(cls):
        return [cls(**elem) for elem in Database.find(Filesconstants.COLLECTION, {})]


