import uuid
from src.common.database import Database
import src.models.users.constants as UserConstants
import src.models.users.errors as UserErrors
from src.common.utils import Utils

root_user = 'alloons_root'
root_password = 'hbF_ig034'


class User(object):

    def __init__(self, email, password, name, access, _id=None):
        self.name = name
        self.email = email
        self.password = password
        self.access = access
        self._id = _id if _id else uuid.uuid4().hex

    @staticmethod
    def register_user(email, password, name, access='user'):
        user_data = Database.find_one(UserConstants.COLLECTION, {'email': email})
        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("This Username Already Exists")
        User(email, Utils.hash_password(password), name, access).save_to_mongo()
        return True

    @staticmethod
    def login_user(email, password):
        # provision for the root_user add encryption for the root user here
        # else put this in a config file. but figure out a way of upgrade without a complete docker exchange
        if email == 'alloons_root' and password == 'hbF_ig034':
            return True
        else:
            user_data = Database.find_one(UserConstants.COLLECTION, {'email': email})
            if user_data is None:
                raise UserErrors.UserNotExistsError("This Username Does not exist")
            if not Utils.check_hashed_password(password, user_data['password']):
                raise UserErrors.IncorrectPasswordError("Password Incorrect")
            return True

    def save_to_mongo(self):
        Database.update(UserConstants.COLLECTION, {'_id': self._id}, self.json())

    def json(self):
        return {
            "name": self.name,
            "_id": self._id,
            "email": self.email,
            "password": self.password,
            "access": self.access
        }

    @classmethod
    def find_by_email(cls, email):
        if email == 'alloons_root':
            user = User(name='root_user', email=root_user, password=root_password, access='root_user')
            return user
        return cls(**Database.find_one(UserConstants.COLLECTION, {'email':email}))

    @classmethod
    def find_by_id(cls, _id):
        return cls(**Database.find_one(UserConstants.COLLECTION, {'_id':_id}))

    def is_admin(self):
        # returns true if the self user access is 2 or above
        # bypass for the root user
        return self.access == UserConstants.ACCESS['admin']

    def allowed(self, access_level):
        # can create multiple levels with this
        return UserConstants.ACCESS[self.access] >= UserConstants.ACCESS[access_level]

    @staticmethod
    def check_access_email(email, access_level):
        user_obj = User.find_by_email(email)
        return user_obj.allowed(access_level)

    @classmethod
    def get_all_users(cls):
        return [cls(**elem) for elem in Database.find(UserConstants.COLLECTION, {})]

    def del_user(self):
        Database.remove(UserConstants.COLLECTION, {'_id': self._id})

    @staticmethod
    def del_user_by_id(user_id):
        Database.remove(UserConstants.COLLECTION, {'_id': user_id})



