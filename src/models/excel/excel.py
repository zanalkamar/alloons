
# print('Your total sale as of today is : {}'.format(total_sale))

import csv
from src.models.sales.sales import Sales
from src.common.database import Database
Database.initialize()


def convert_str_float(string):
    try:
        return float(string)
    except ValueError:
        return None


with open('/Users/zameer/PycharmProjects/alloons/src/files/order.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print('Going for row: {}'.format(row))
        subtotal, ship_cost, tax, ship_method, line_item, line_item_price, pay_method, refund_amount, \
        finance_stat, order_num, sku, sale_id = row['Subtotal'], row['Shipping'], row['Taxes'], row['Shipping Method'], \
                                  row['Lineitem name'], row['Lineitem price'], row['Payment Method'], \
                                  row['Refunded Amount'], row['Financial Status'], row['Name'].strip('#'), row['Lineitem sku'], row['Id']
        subtotal, line_item_price, refund_amount, ship_cost, tax = convert_str_float(subtotal), convert_str_float(line_item_price), convert_str_float(refund_amount), convert_str_float(ship_cost), convert_str_float(tax)
        sale_dict = dict(subtotal=subtotal, ship_cost=ship_cost, tax=tax, ship_method=ship_method, line_item=line_item,
                         line_item_price=line_item_price, pay_method=pay_method, refund_amount=refund_amount,
                         finance_stat=finance_stat, order_num=order_num, sku=sku)
        sale_line = Sales(subtotal, ship_cost, tax, ship_method, line_item, line_item_price, pay_method, refund_amount,
                          finance_stat, order_num, sku)
        print('Object is {}'.format(sale_line))
        sale_line.save_to_mongo()


