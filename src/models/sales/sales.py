
import uuid
from src.common.database import Database
import src.models.sales.constants as SalesConstants


class Sales(object):

    def __init__(self, subtotal, ship_cost, tax, ship_method, line_item, line_item_price, pay_method, refund_amount,
                 finance_stat, order_num, sku, _id=None):
        self.subtotal = subtotal
        self.ship_cost = ship_cost
        self.tax = tax
        self.ship_method = ship_method
        self.line_item = line_item
        self.line_item_price = line_item_price
        self.pay_method = pay_method
        self.refund_amount = refund_amount
        self.finance_stat = finance_stat
        self.order_num = order_num
        self.sku = sku
        self.awb = None
        self._id = _id if _id else self.set_id_if_none(order_num)
        print('Order Num is: {}'.format(order_num))
        # self._id = _id if _id else self.set_id()

    @staticmethod
    def set_id():
        return uuid.uuid4().hex

    def json(self):
        return {
            'subtotal': self.subtotal,
            'ship_cost': self.ship_cost,
            'tax': self.tax,
            'ship_method': self.ship_method,
            'line_item': self.line_item,
            'line_item_price': self.line_item_price,
            'pay_method': self.pay_method,
            'finance_stat': self.refund_amount,
            'order_num': self.order_num,
            'sku': self.sku,
            '_id': self._id,
            'awb': self.awb
        }

    def save_to_mongo(self):
        Database.update(SalesConstants.COLLECTION, {'_id': self._id}, self.json())

    @staticmethod
    def get_sales_by_num(order_num):
        return Database.find_one(SalesConstants.COLLECTION, {'order_num': order_num})

    @staticmethod
    def set_id_if_none(order_num):
        sale = Sales.get_sales_by_num(order_num)
        if sale:
            print('Sale is {}'.format(sale))
            return sale['_id']
        else:
            return Sales.set_id()







