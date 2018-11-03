from src.common.database import Database
import src.models.order.constants as OrderConstants
import uuid
from src.models.users.users import User


class Order(object):

    def __init__(self, ord_date, name, descr, vendor, gst, ship, total, rcv_date, oid=None, _id=None, items=[]):
        self.ord_date = ord_date
        self.name = name
        self.descr = descr
        self.vendor = vendor
        self.gst = float(gst)
        self.ship = float(ship)
        self.total = float(total)
        self.rcv_date = rcv_date
        self.oid = oid if oid else Order.set_oid()
        self._id = _id if _id else Order.create_id()
        self.items = items

    def json(self):
        return {
            'ord_date': self.ord_date,
            'name': self.name,
            'descr': self.descr,
            'vendor': self.vendor,
            'gst': self.gst,
            'ship': self.ship,
            'total': self.total,
            'rcv_date': self.rcv_date,
            'oid': self.oid,
            '_id': self._id,
            'items': self.items
        }

    def save_to_mongo(self):
        Database.update(OrderConstants.COLLECTION, {'_id': self._id}, self.json())

    @classmethod
    def get_all_order(cls):
        return [cls(**elem) for elem in Database.find(OrderConstants.COLLECTION, {})]

    @staticmethod
    def create_id():
        return uuid.uuid4().hex

    @staticmethod
    def set_oid():
        """
        to set the OID:, checks the last OID no and returns the next
        :return:
        """
        all_order = Order.get_all_order()
        if all_order:
            o_list = [s.oid for s in all_order]
            oid = max(o_list) + 1
        else:
            # this is for the first entry
            oid = 2000
        return oid

    @staticmethod
    def check_user_access(email, access_level):
        if email:
            return User.check_access_email(email, access_level)

    @classmethod
    def get_ord_by_id(cls, _id):
        return cls(**Database.find_one(OrderConstants.COLLECTION, {'_id': _id}))

    @staticmethod
    def del_ord_by_id(_id):
        order = Order.get_ord_by_id(_id)
        order.del_order()

    def del_order(self):
        Database.remove(OrderConstants.COLLECTION, {'_id': self._id})

    @staticmethod
    def get_item_for_order(_id, item_id):
        order_obj = Order.get_ord_by_id(_id)
        for item in order_obj.items:
            if item['item_id'] == item_id:
                return item

    # @staticmethod
    # def get_item_index_by_item_id(order, item_id):
    #     for index, item in enumerate(order.items):
    #         if item['item_id'] == item_id:
    #             return index

    @staticmethod
    def update_item(_id, item_id, item_dict):
        order = Order.get_ord_by_id(_id)
        index = [order.items.index(x) for x in order.items if x['item_id'] == item_id][0]
        order.items[index] = item_dict
        order.save_to_mongo()



