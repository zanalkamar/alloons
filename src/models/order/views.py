from flask import Blueprint, render_template, request, send_file, redirect, url_for, session, make_response
from src.models.users.users import User
from src.models.order.order import Order


order_blueprint = Blueprint('order', __name__)


@order_blueprint.route('/', methods={'GET', 'POST'})
def order():
    if not Order.check_user_access(session.get('email'), 'admin'):
        # this is for the access level testing. move it to decorator
        return render_template('users/login.html')
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
        sku = request.form['sku']
        ord_obj = Order(ord_date=ord_date, pid=pid, prod_descr=prod_descr, size=size, vendor=vendor, qty=qty,
                        u_price=u_price, gst=gst, ship=ship, total=total, rcv_date=rcv_date, sku=sku)
        ord_obj.save_to_mongo()

    orders = Order.get_all_order()
    user = User.find_by_email(session.get('email'))

    # return render_template('order/order.html')
    return render_template('order/order.html', orders=orders, error_msg=None, user=user)


@order_blueprint.route('/edit/<string:_id>', methods={'GET', 'POST'})
def order_edit(_id):
    user = User.find_by_email(session.get('email'))
    if request.method == 'GET':
        order = Order.get_ord_by_id(_id)
        return render_template('order/edit.html', order=order, user=user)
    else:
        ord_obj = Order.get_ord_by_id(_id)
        ord_date = request.form['ord_date']
        pid = request.form['pid']
        prod_descr = request.form['prod_descr']
        # size = request.form['size']
        vendor = request.form['vendor']
        qty = request.form['qty']
        u_price = request.form['u_price']
        gst = request.form['gst']
        ship = request.form['ship']
        total = request.form['total']
        rcv_date = request.form['rcv_date']
        sku = request.form['sku']
        # ord_obj = Order(ord_date=ord_date, pid=pid, prod_descr=prod_descr, size=size, vendor=vendor, qty=qty,
        #                 u_price=u_price, gst=gst, ship=ship, total=total, rcv_date=rcv_date, sku=sku)
        ord_obj.ord_date = ord_date
        ord_obj.pid = pid
        ord_obj.prod_descr = prod_descr
        ord_obj.vendor = vendor
        ord_obj.qty = qty
        ord_obj.u_price = u_price
        ord_obj.gst = gst
        ord_obj.ship = ship
        ord_obj.total = total
        ord_obj.rcv_date = rcv_date
        ord_obj.sku = sku
        ord_obj.save_to_mongo()
    return redirect(url_for('order.order'))


@order_blueprint.route('/del/<string:_id>', methods={'GET', 'POST'})
def del_order(_id):
    Order.del_ord_by_id(_id)
    return redirect(url_for('order.order'))
