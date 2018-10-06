import src.models.expense.constants as ExpenseConstants
from src.common.database import Database
import uuid

class Expense(object):

    def __init__(self, date, category, item, remarks, amount, sn=None, _id=None):
        self.date = date
        self.category = category
        self.item = item
        self.remarks = remarks
        self.sn = sn
        self.amount = amount
        self._id = _id if _id else Expense.create_id()

    def json(self):
        return {
            'date': self.date,
            'item': self.item,
            'remarks': self.remarks,
            'sn': self.sn,
            '_id': self._id,
            'category': self.category,
            'amount': self.amount
        }

    def save_to_mongo(self):
        Database.update(ExpenseConstants.COLLECTION, {'_id': self._id}, self.json())

    @staticmethod
    def create_id():
        return uuid.uuid4().hex

    @classmethod
    def get_all_expense(cls):
        return [cls(**elem) for elem in Database.find(ExpenseConstants.COLLECTION, {})]




