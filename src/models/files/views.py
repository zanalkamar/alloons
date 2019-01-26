from flask import Blueprint, render_template, request, session, redirect, url_for

from src.models.users.users import User
from src.models.files.files import Files
import io
from src.models.shopify_order.shopify_order import Shopifyorder
import csv

files_blueprint = Blueprint('files', __name__)


@files_blueprint.route('/', methods=['GET', 'POST'])
def files_index():
    user = User.find_by_email(session.get('email'))
    files = Files.get_all_files()
    return render_template('files/files_index.html', files=files, user=user)


@files_blueprint.route('/upload', methods=['GET', 'POST'])
def upload_file():
    user = User.find_by_email(session.get('email'))
    if request.method == 'POST':
        file = request.files['file']
        Files.create_and_save_gridfs(file)
    return render_template('files/files_index.html', user=user)


def transform(text_file_contents):
    return text_file_contents.replace("=", ",")


@files_blueprint.route('/upload_shopify', methods=['GET', 'POST'])
def upload_shopify():
    user = User.find_by_email(session.get('email'))
    if request.method == 'POST':
        file = request.files['file']
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
        for row in csv_input:
            shop_order = Shopifyorder(row['Name'], row['Email'], row['Financial Status'], row['Paid at'], row['Fulfillment Status'],
                    row['Fulfilled at'], row['Accepts Marketing'], row['Currency'], row['Subtotal'], row['Shipping'],
                    row['Taxes'], row['Total'], row['Discount Code'], row['Discount Amount'], row['Shipping Method'],
                    row['Created at'], row['Lineitem quantity'], row['Lineitem name'], row['Lineitem price'],
                    row['Lineitem compare at price'], row['Lineitem sku'], row['Lineitem requires shipping'],
                    row['Lineitem taxable'], row['Lineitem fulfillment status'], row['Shipping Company'], row['Notes'],
                    row['Note Attributes'], row['Cancelled at'], row['Payment Method'], row['Payment Reference'],
                    row['Refunded Amount'], row['Vendor'], row['Id'], row['Tags'],
                    row['Lineitem discount'])
            shop_order.save_to_mongo()
    Shopifyorder.fill_missing_info()

    return render_template('files/files_index.html', user=user)


@files_blueprint.route('/upload_ecom', methods=['GET', 'POST'])
def upload_ecom():
    user = User.find_by_email(session.get('email'))
    if request.method == 'POST':
        file = request.files['file']
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
        for row in csv_input:
            shopify = Shopifyorder.get_by_name('{}{}'.format('#', row['order_number']))
            if shopify:
                shopify.shipping_company = 'ecom'
                shopify.shipping_cost = float(row['Total'])
                # shopify.payment_method = row['product_type']
                shopify.save_to_mongo()

    return render_template('files/files_index.html', user=user)


@files_blueprint.route('/upload_fedex', methods=['GET', 'POST'])
def upload_fedex():
    user = User.find_by_email(session.get('email'))
    if request.method == 'POST':
        file = request.files['file']
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
        # for i in csv_input:
        #     print(i)

        for row in csv_input:
            # print(row['Shipper Reference 1'])
            shopify = Shopifyorder.get_by_name('{}{}'.format('#', row['Shipper Reference 1']))
            # print(shopify.name)
            if shopify:
                # for i in row.keys():
                #     print(i)
                # print('\n\n\n\n\n')
                shopify.shipping_company = 'fedex'
                shopify.shipping_cost = float(row['Air Waybill Total Amount'])
                print(row['Air Waybill Charge Label'])
                # shopify.payment_method = row['product_type']
                # print(shopify.payment_method)
                shopify.save_to_mongo()

    return render_template('files/files_index.html', user=user)


@files_blueprint.route('/download', methods=['GET', 'POST'])
def download():
    pass






