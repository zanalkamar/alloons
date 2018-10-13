from flask import Blueprint, render_template, request, send_file, redirect, url_for, session, make_response
from src.models.users.users import User
from src.models.order.order import Order


order_blueprint = Blueprint('order', __name__)


@order_blueprint.route('/', methods={'GET', 'POST'})
def order():
    print('program reached here')
    user = None
    error_msg = None

    if request.method == 'POST':
        ord_date = request.form['ord_date']
        pid = request.form['pid']
        prod_descr = request.form['prod_descr']
        size = request.form['size']
        vendor = request.form['vendor']
        qty = request.form['qty']
        u_price = request.form['u_price']
        gst = request.form['gst']
        ship = request.form['ship']
        total = request.form['total']
        rcv_date = request.form['rcv_date']
        ord_obj = Order(ord_date=ord_date, pid=pid, prod_descr=prod_descr, size=size, vendor=vendor, qty=qty,
                        u_price=u_price, gst=gst, ship=ship, total=total, rcv_date=rcv_date)
        ord_obj.save_to_mongo()

    orders = Order.get_all_order()

    # return render_template('order/order.html')
    return render_template('order/order.html', orders=orders, error_msg=None, user=user)


#
# @expense_blueprint.route('/edit/<string:_id>', methods={'GET', 'POST'})
# def expense_edit(_id):
#     # user = User.find_by_email(session.get('email'))
#     if request.method == 'GET':
#         expense = Expense.get_exp_by_id(_id)
#         return render_template('expense/edit.html', expense=expense)
#     else:
#
#         date = request.form['date']
#         category = request.form['category']
#         item = request.form['item']
#         remarks = request.form['remarks']
#         cost = request.form['amount']
#         exp = Expense.get_exp_by_id(_id)
#         exp.date = date
#         exp.category = category
#         exp.item = item
#         exp.remarks = remarks
#         exp.cost = cost
#         exp.save_to_mongo()
#     return redirect(url_for('expense.expense'))
#
#
# @expense_blueprint.route('/del/<string:_id>', methods={'GET', 'POST'})
# def del_expense(_id):
#     Expense.del_expense_by_id(_id)
#     return redirect(url_for('expense.expense'))

