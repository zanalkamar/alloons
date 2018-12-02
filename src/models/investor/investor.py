
import uuid
from src.common.database import Database
import src.models.investor.constants as InvestorConstants
from src.models.users.users import User


class Investor(object):

    def __init__(self, name, join_date=None, contacts=None, sku_dict=None, _id=None):
        self.name = name
        self.contacts = contacts if contacts else {'mobile': None, 'email': None}
        self.sku_dict = sku_dict if sku_dict else {}
        self.join_date = join_date
        self._id = _id if _id else uuid.uuid4().hex

    def json(self):
        return {
            'name': self.name,
            'contacts': self.contacts,
            'sku_dict': self.sku_dict,
            '_id': self._id,
            'join_date': self.join_date
        }

    def save_to_mongo(self):
        Database.update(InvestorConstants.COLLECTION, {'_id': self._id}, self.json())

    @classmethod
    def get_investor_by_id(cls, _id):
        return cls(**Database.find_one(InvestorConstants.COLLECTION, {'_id': _id}))

    @staticmethod
    def del_investor_by_id(_id):
        investor = Investor.get_investor_by_id(_id)
        investor.del_investor()

    def del_investor(self):
        Database.remove(InvestorConstants.COLLECTION, {'_id': self._id})

    @staticmethod
    def check_user_access(email, access_level):
        if email:
            return User.check_access_email(email, access_level)

    @classmethod
    def get_all(cls):
        return [cls(**elem) for elem in Database.find(InvestorConstants.COLLECTION, {})]


