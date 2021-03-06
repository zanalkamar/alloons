import src.models.expense.constants as ExpenseConstants
from src.common.database import Database
import uuid
from src.models.users.users import User
from src.models.time.date_time import DateTime


class Expense(object):

    def __init__(self, date, category, item, remarks, amount, sn=None, _id=None):
        self.date = date
        self.category = category
        self.item = item
        self.remarks = remarks
        self.sn = sn if sn else Expense.set_sno()
        self.amount = float(amount)
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

    @staticmethod
    def set_sno():
        """
        to set the Sno:, checks the last s no and returns the next
        :return:
        """
        all_expense = Expense.get_all_expense()
        if all_expense:
            s_list = [s.sn for s in all_expense]
            s_no = max(s_list) + 1
        else:
            # this is for the first entry
            s_no = 1000
        return s_no

    @classmethod
    def get_exp_by_id(cls, _id):
        return cls(**Database.find_one(ExpenseConstants.COLLECTION, {'_id': _id}))

    @staticmethod
    def del_expense_by_id(_id):
        expense = Expense.get_exp_by_id(_id)
        expense.del_expense()

    def del_expense(self):
        Database.remove(ExpenseConstants.COLLECTION, {'_id': self._id})

    @staticmethod
    def check_user_access(email, access_level):
        if email:
            return User.check_access_email(email, access_level)

    @classmethod
    def get_exp_in_interval(cls, start, end):
        query = {'date': {'$gte': start, '$lt': end}}
        return [cls(**elem) for elem in Database.find(ExpenseConstants.COLLECTION, query)]

    @staticmethod
    def get_exp_predefined(duration):
        if duration == 'this_week':
            start, end = DateTime.this_week()
        elif duration == 'this_month':
            start, end = DateTime.this_month()
        elif duration == 'last_month':
            start, end = DateTime.last_month()
        elif duration == 'this_year':
            start, end = DateTime.this_year()
        return Expense.get_exp_in_interval(start, end)

    @staticmethod
    def get_sum_for_interval(duration):
        exp_list = Expense.get_exp_predefined(duration)
        return sum([x.amount for x in exp_list])

    @staticmethod
    def get_sum_dict():
        this_month = Expense.get_sum_for_interval('this_month')
        last_month = Expense.get_sum_for_interval('last_month')
        this_year = Expense.get_sum_for_interval('this_year')
        return {'this_month': this_month, 'last_month': last_month, 'this_year': this_year}










