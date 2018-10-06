import pymongo
import gridfs


class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    # use the below for docker with mongodb in the host
    # URI = "mongodb://172.17.0.1:27017"
    # use the below only on mac
    # URI = "mongodb://host.docker.internal:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client["alloons"]

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)

    @staticmethod
    def find_one(collection, query):
        # this will return a dictionary of the search result
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def send_to_gridfs(filename, data):
        grid_fs = gridfs.GridFS(Database.DATABASE)
        with grid_fs.new_file(filename=filename) as fp:
            fp.write(data)
            file_id = fp._id
            print(file_id)

        if grid_fs.find_one(file_id) is not None:
            return file_id

    @staticmethod
    def get_gridfs_file(filename):
        grid_fs = gridfs.GridFS(Database.DATABASE)
        return grid_fs.find_one({'filename': filename})

    @staticmethod
    def del_gridfs_file(file_id):
        grid_fs = gridfs.GridFS(Database.DATABASE)
        grid_fs.delete(file_id)
        if not grid_fs.find_one(file_id):
            return True






