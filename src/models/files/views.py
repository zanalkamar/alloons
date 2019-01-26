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
        # print(f'the length is {len(csv_input)}')
        # cnt = 0
        for row in csv_input:
            # print(row.keys())
            # cnt += 1
            shop_order = Shopifyorder(row['Name'], row['Email'], row['Financial Status'], row['Paid at'], row['Fulfillment Status'],
                    row['Fulfilled at'], row['Accepts Marketing'], row['Currency'], row['Subtotal'], row['Shipping'],
                    row['Taxes'], row['Total'], row['Discount Code'], row['Discount Amount'], row['Shipping Method'],
                    row['Created at'], row['Lineitem quantity'], row['Lineitem name'], row['Lineitem price'],
                    row['Lineitem compare at price'], row['Lineitem sku'], row['Lineitem requires shipping'],
                    row['Lineitem taxable'], row['Lineitem fulfillment status'], row['Billing Name'],
                    row['Billing Street'], row['Billing Address1'], row['Billing Address2'], row['Billing Company'],
                    row['Billing City'], row['Billing Zip'], row['Billing Province'], row['Billing Country'],
                    row['Billing Phone'], row['Shipping Name'], row['Shipping Street'], row['Shipping Address1'],
                    row['Shipping Address2'], row['Shipping Company'], row['Shipping City'], row['Shipping Zip'],
                    row['Shipping Province'], row['Shipping Country'], row['Shipping Phone'], row['Notes'],
                    row['Note Attributes'], row['Cancelled at'], row['Payment Method'], row['Payment Reference'],
                    row['Refunded Amount'], row['Vendor'], row['Id'], row['Tags'], row['Risk Level'], row['Source'],
                    row['Lineitem discount'], row['Tax 1 Name'], row['Tax 1 Value'], row['Tax 2 Name'], row['Tax 2 Value'],
                    row['Tax 3 Name'], row['Tax 3 Value'], row['Tax 4 Name'], row['Tax 4 Value'], row['Tax 5 Name'],
                    row['Tax 5 Value'], row['Phone'])
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
        # print(f'the length is {len(csv_input)}')
        # cnt = 0
        for row in csv_input:
            # print(row.keys())
            # cnt += 1
            # shop_order = Shopifyorder(row['Name'], row['Email'], row['Financial Status'], row['Paid at'], row['Fulfillment Status'],
            #         row['Fulfilled at'], row['Accepts Marketing'], row['Currency'], row['Subtotal'], row['Shipping'],
            #         row['Taxes'], row['Total'], row['Discount Code'], row['Discount Amount'], row['Shipping Method'],
            #         row['Created at'], row['Lineitem quantity'], row['Lineitem name'], row['Lineitem price'],
            #         row['Lineitem compare at price'], row['Lineitem sku'], row['Lineitem requires shipping'],
            #         row['Lineitem taxable'], row['Lineitem fulfillment status'], row['Billing Name'],
            #         row['Billing Street'], row['Billing Address1'], row['Billing Address2'], row['Billing Company'],
            #         row['Billing City'], row['Billing Zip'], row['Billing Province'], row['Billing Country'],
            #         row['Billing Phone'], row['Shipping Name'], row['Shipping Street'], row['Shipping Address1'],
            #         row['Shipping Address2'], row['Shipping Company'], row['Shipping City'], row['Shipping Zip'],
            #         row['Shipping Province'], row['Shipping Country'], row['Shipping Phone'], row['Notes'],
            #         row['Note Attributes'], row['Cancelled at'], row['Payment Method'], row['Payment Reference'],
            #         row['Refunded Amount'], row['Vendor'], row['Id'], row['Tags'], row['Risk Level'], row['Source'],
            #         row['Lineitem discount'], row['Tax 1 Name'], row['Tax 1 Value'], row['Tax 2 Name'], row['Tax 2 Value'],
            #         row['Tax 3 Name'], row['Tax 3 Value'], row['Tax 4 Name'], row['Tax 4 Value'], row['Tax 5 Name'],
            #         row['Tax 5 Value'], row['Phone'])
            # shop_order.save_to_mongo()
    # Shopifyorder.fill_missing_info()

            shopify = Shopifyorder.get_by_name('{}{}'.format('#', row['order_number']))
            if shopify:
                shopify.shipping_company = 'ecom'
                shopify.save_to_mongo()
            # print('shopify for the order {} is {}'.format(row['order_number'], type(shopify)))

    return render_template('files/files_index.html', user=user)


@files_blueprint.route('/download', methods=['GET', 'POST'])
def download():
    pass






