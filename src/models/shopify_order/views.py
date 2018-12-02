# from flask import Blueprint, render_template, request, send_file, redirect, url_for, session, make_response
from src.models.users.users import User
from src.models.shopify_order.shopify_order import Shopifyorder
from flask import Blueprint, render_template, request, session, redirect, url_for

shopify_blueprint = Blueprint('shopify', __name__)


@shopify_blueprint.route('/', methods={'GET', 'POST'})
def shopify():
    error_msg = None
    if not Shopifyorder.check_user_access(session.get('email'), 'admin'):
        # this is for the access level testing. move it to decorator
        return render_template('users/login.html')

    # if request.method == 'POST':
    #     date = request.form['date']
    #     category = request.form['category']
    #     item = request.form['item']
    #     remarks = request.form['remarks']
    #     cost = request.form['amount']
    #     exp_obj = Shopifyorder(date, category, item, remarks, cost)
    #     exp_obj.save_to_mongo()

    shopify_orders = Shopifyorder.get_all_shopify() #
    user = User.find_by_email(session.get('email'))

    return render_template('shopify/shopify.html', shopify=shopify_orders, error_msg=error_msg, user=user)


# @shopify_blueprint.route('/edit/<string:_id>', methods={'GET', 'POST'})
# def shopify_edit(_id):
#     user = User.find_by_email(session.get('email'))
#     if request.method == 'GET':
#         shopify_order = Shopifyorder.get_exp_by_id(_id)
#         return render_template('shopify_order/edit.html', shopify_order=shopify_order, user=user)
#     else:
#         date = request.form['date']
#         # category = request.form['category']
#         item = request.form['item']
#         remarks = request.form['remarks']
#         # cost = request.form['amount']
#         amount = request.form['amount']
#         exp = Shopifyorder.get_exp_by_id(_id)
#         exp.date = date
#         # exp.category = category
#         exp.item = item
#         exp.remarks = remarks
#         exp.amount = amount
#         exp.save_to_mongo()
#     return redirect(url_for('shopify_order.shopify_order'))


# @shopify_blueprint.route('/del/<string:_id>', methods={'GET', 'POST'})
# def del_shopify(_id):
#     Shopifyorder.del_shopify_order_by_id(_id)
#     return redirect(url_for('shopify.shopify'))

