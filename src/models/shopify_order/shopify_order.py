
import uuid
import src.models.shopify_order.constants as ShopifyConstants
from src.common.database import Database
import collections
from src.models.users.users import User


class Shopifyorder(object):

    def __init__(self, name, email, financial_status, paid_at, fulfillment_status, fulfilled_at, accepts_marketing,
                 currency, subtotal, shipping, taxes, total, discount_code, discount_amount, shipping_method,
                 created_at, lineitem_quantity, lineitem_name, lineitem_price, lineitem_compare_at_price, lineitem_sku,
                 lineitem_requires_shipping, lineitem_taxable, lineitem_fulfillment_status, shipping_company, notes, note_attributes, cancelled_at, payment_method,
                 payment_reference, refunded_amount, vendor, id, tags, lineitem_discount, miss_fill=None, _id=None, shipping_cost=None):
        self.name = name
        self.email = email
        self.financial_status = financial_status
        self.paid_at = paid_at
        self.fulfillment_status = fulfillment_status
        self.fulfilled_at = fulfilled_at
        self.accepts_marketing = accepts_marketing
        self.currency = currency
        self.subtotal = Shopifyorder.format_if_not_none('float', subtotal)
        self.shipping = shipping
        self.taxes = taxes
        self.total = Shopifyorder.format_if_not_none('float', total)
        self.discount_code = discount_code
        self.discount_amount = Shopifyorder.format_if_not_none('float', discount_amount)
        self.shipping_method = shipping_method
        self.created_at = created_at
        self.lineitem_quantity = Shopifyorder.format_if_not_none('int', lineitem_quantity)
        self.lineitem_name = lineitem_name
        self.lineitem_price = Shopifyorder.format_if_not_none('float', lineitem_price)
        self.lineitem_compare_at_price = lineitem_compare_at_price
        self.lineitem_sku = lineitem_sku
        self.lineitem_requires_shipping = lineitem_requires_shipping
        self.lineitem_taxable = lineitem_taxable
        self.lineitem_fulfillment_status = lineitem_fulfillment_status
        self.shipping_company = shipping_company
        self.notes = notes
        self.note_attributes = note_attributes
        self.cancelled_at = cancelled_at
        self.payment_method = payment_method
        self.payment_reference = payment_reference
        self.refunded_amount = Shopifyorder.format_if_not_none('float', refunded_amount)
        self.vendor = vendor
        self.id = id
        self.tags = tags
        self.lineitem_discount = lineitem_discount
        # self.shipping_company = shipping_company
        self.miss_fill = miss_fill  # help to fill the missing information
        self._id = Shopifyorder.get_id(name, lineitem_name)
        self.shipping_cost = shipping_cost

    def json(self):
        return {
            'name': self.name,
            'email': self.email,
            'financial_status': self.financial_status,
            'paid_at': self.paid_at,
            'fulfillment_status': self.fulfillment_status,
            'fulfilled_at': self.fulfilled_at,
            'accepts_marketing': self.accepts_marketing,
            'currency': self.currency,
            'subtotal': self.subtotal,
            'shipping': self.shipping,
            'taxes': self.taxes,
            'total': self.total,
            'discount_code': self.discount_code,
            'discount_amount': self.discount_amount,
            'shipping_method': self.shipping_method,
            'created_at': self.created_at,
            'lineitem_quantity': self.lineitem_quantity,
            'lineitem_name': self.lineitem_name,
            'lineitem_price': self.lineitem_price,
            'lineitem_compare_at_price': self.lineitem_compare_at_price,
            'lineitem_sku': self.lineitem_sku,
            'lineitem_requires_shipping': self.lineitem_requires_shipping,
            'lineitem_taxable': self.lineitem_taxable,
            'lineitem_fulfillment_status': self.lineitem_fulfillment_status,
            'shipping_company': self.shipping_company,
            'notes': self.notes,
            'note_attributes': self.note_attributes,
            'cancelled_at': self.cancelled_at,
            'payment_method': self.payment_method,
            'payment_reference': self.payment_reference,
            'refunded_amount': self.refunded_amount,
            'vendor': self.vendor,
            'id': self.id,
            'tags': self.tags,
            'lineitem_discount': self.lineitem_discount,
            '_id': self._id,
            'miss_fill': self.miss_fill,
            'shipping_cost': self.shipping_cost
        }

    def save_to_mongo(self):
        Database.update(ShopifyConstants.COLLECTION, {'_id': self._id}, self.json())

    @staticmethod
    def format_if_not_none(int_type, value):
        if value:
            if int_type == 'float':
                return float(value)
            elif int_type == 'int':
                return int(value)
        else:
            return 0

    @staticmethod
    def get_id(name, lineitem_name):
        in_db = Database.find_one(ShopifyConstants.COLLECTION, {'name': name, 'lineitem_name': lineitem_name})
        if in_db:
            # print(f'name is: {name}\titem is {lineitem_name}')
            return in_db['_id']
        else:
            return uuid.uuid4().hex

    @classmethod
    def fill_missing_info(cls):
        all_shopify = Shopifyorder.get_all_shopify()
        order_ids = [x.name for x in all_shopify]
        repeats = [item for item, count in collections.Counter(order_ids).items() if count > 1]
        # print(f'Found repeats in {repeats}')
        for name in repeats:
            same_order = Shopifyorder.get_list_by_name(name)
            # for order in same_order:
            #     print(order.subtotal)
            Shopifyorder.fill_missing_in_order(same_order)

    @classmethod
    def get_all_shopify(cls):
        return [cls(**elem) for elem in Database.find(ShopifyConstants.COLLECTION, {})]

    @classmethod
    def get_by_name(cls, name):
        # print(name)
        try:
            return cls(**Database.find_one(ShopifyConstants.COLLECTION, {'name': name}))
        except TypeError:
            print('Found Type error on {}'.format(name))

    @classmethod
    def get_list_by_name(cls, name):
        return [cls(**elem) for elem in Database.find(ShopifyConstants.COLLECTION, {'name': name})]

    @classmethod
    def fill_missing_in_order(cls, order_list):
        first_order = order_list.pop(0)
        # financial_status = first_order.financial_status
        # print(f'financial status is {financial_status}')
        for order in order_list:
            # print(order.financial_status)
            order.financial_status = first_order.financial_status
            order.paid_at = first_order.paid_at
            order.fulfillment_status = first_order.fulfillment_status
            order.shipping_method = first_order.shipping_method
            order.payment_method = first_order.payment_method
            order.refunded_amount = first_order.refunded_amount
            order.id = first_order.id
            order.miss_fill = True  # this wont work now.
            order.save_to_mongo()

    @staticmethod
    def del_shopify_order_by_id(_id):
        shopify_order = Shopifyorder.get_by_id(_id)
        shopify_order.del_shopify_order()

    def del_shopify_order(self):
        Database.remove(ShopifyConstants.COLLECTION, {'_id': self._id})

    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one(ShopifyConstants.COLLECTION, {'_id': _id}))

    @staticmethod
    def check_user_access(email, access_level):
        if email:
            return User.check_access_email(email, access_level)

    @classmethod
    def get_by_sku_list(cls, sku_list):
        tot_list = []
        for sku in sku_list:
            order_list = Shopifyorder.get_by_sku(sku)
            tot_list += order_list
        return tot_list

    @classmethod
    def get_by_sku(cls, sku):
        return [cls(**elem) for elem in Database.find(ShopifyConstants.COLLECTION, {'lineitem_sku': sku})]















