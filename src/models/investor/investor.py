
import uuid
from src.common.database import Database
import src.models.investor.constants as InvestorConstants
from src.models.users.users import User
from src.models.shopify_order.shopify_order import Shopifyorder
import src.models.shopify_order.constants as ShopifyConstants


class Investor(object):

    def __init__(self, name, join_date=None, contacts=None, sku_list=None, _id=None):
        self.name = name
        self.contacts = contacts if contacts else {'mobile': None, 'email': None}
        self.sku_list = sku_list if sku_list else []
        self.join_date = join_date
        self._id = _id if _id else uuid.uuid4().hex

    def json(self):
        return {
            'name': self.name,
            'contacts': self.contacts,
            'sku_list': self.sku_list,
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

    def get_shopify(self):
        total_dict = {'shoppify_total': 0, 'shipping_cost': 0, 'pay_u': 0, 'shopify_commision': 0, 'tot_pack_cost': 0}
        pay_cnt = 0
        for sku in self.sku_list:
            sku_shopify_list = Shopifyorder.get_by_sku(sku)


            if sku_shopify_list:
                for entry in sku_shopify_list:
                    if entry.shipping_method == 'Standard shipping':
                        pay_cnt += 1
                        total_dict['pay_u'] += (entry.total * ShopifyConstants.payu_commision * 0.01)
                        total_dict['shopify_commision'] += (entry.total * ShopifyConstants.shoppify_commision * 0.01)
                        print('Pay_U: {}\tsale value: {}'.format(total_dict['pay_u'], entry.total))

                    if entry.total == 0:
                        print(entry.name)

                    if entry.total:
                        total_dict['shoppify_total'] += entry.total

                    if entry.shipping_cost:
                        total_dict['tot_pack_cost'] += ShopifyConstants.packing_cost
                        total_dict['shipping_cost'] += entry.shipping_cost



        skus_total = total_dict['shoppify_total'] - total_dict['shipping_cost'] - total_dict['pay_u'] - \
                     total_dict['shopify_commision'] - total_dict['tot_pack_cost']
        print('Pay U is {}'.format(total_dict['pay_u']))
        print('Total_shopify\t: {}\nTotal_shipping\t: {}\nPay_U\t:{}\nShopify Commision\t:{}\ntotal packing cost\t:{}\nSKUs Total = '
              'Shopify - shipping = {}'.format(total_dict['shoppify_total'], total_dict['shipping_cost'],
                                               total_dict['pay_u'], total_dict['shopify_commision'], total_dict['tot_pack_cost'], skus_total))

        print('Pay U count is : {}'.format(pay_cnt))


