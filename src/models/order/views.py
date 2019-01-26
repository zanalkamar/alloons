from flask import Blueprint, render_template, request, send_file, redirect, url_for, session, make_response
from src.models.users.users import User
from src.models.order.order import Order
import uuid


order_blueprint = Blueprint('order', __name__)


@order_blueprint.route('/', methods={'GET', 'POST'})
def order():
    if not Order.check_user_access(session.get('email'), 'admin'):
        # this is for the access level testing. move it to decorator
        return render_template('users/login.html')
    error_msg = None

    if request.method == 'POST':
        ord_date = request.form['ord_date']
        name = request.form['name']
        descr = request.form['descr']
        # size = request.form['size']
        vendor = request.form['vendor']
        # qty = request.form['qty']
        # u_price = request.form['u_price']
        gst = request.form['gst']
        ship = request.form['ship']
        total = request.form['total']
        rcv_date = request.form['rcv_date']
        ord_obj = Order(ord_date=ord_date, name=name, descr=descr, vendor=vendor, gst=gst, ship=ship, total=total,
                        rcv_date=rcv_date)
        ord_obj.save_to_mongo()

    orders = Order.get_all_order()
    user = User.find_by_email(session.get('email'))

    return render_template('order/order.html', orders=orders, error_msg=None, user=user)


@order_blueprint.route('/edit/<string:_id>', methods={'GET', 'POST'})
def order_edit(_id):
    user = User.find_by_email(session.get('email'))
    if request.method == 'GET':
        order = Order.get_ord_by_id(_id)
        return render_template('order/edit.html', order=order, user=user, items=order.items)
    else:
        ord_obj = Order.get_ord_by_id(_id)
        ord_date = request.form['ord_date']
        name = request.form['name']
        descr = request.form['descr']
        vendor = request.form['vendor']
        gst = request.form['gst']
        ship = request.form['ship']
        total = request.form['total']
        rcv_date = request.form['rcv_date']
        ord_obj.ord_date = ord_date
        ord_obj.name = name
        ord_obj.descr = descr
        ord_obj.vendor = vendor
        ord_obj.gst = gst
        ord_obj.ship = ship
        ord_obj.total = total
        ord_obj.rcv_date = rcv_date
        ord_obj.save_to_mongo()
    return redirect(url_for('order.order'))


@order_blueprint.route('/del/<string:_id>', methods={'GET', 'POST'})
def del_order(_id):
    Order.del_ord_by_id(_id)
    return redirect(url_for('order.order'))


@order_blueprint.route('/add_item/<string:_id>', methods={'GET', 'POST'})
def add_item(_id):
    if request.method == 'GET':
        return render_template('order/add_item.html', _id=_id)
    else:
        pid = request.form['pid']
        item_descr = request.form['item_descr']
        size = request.form['size']
        qty = request.form['qty']
        u_price = request.form['u_price']
        gst = request.form['gst']
        ship = request.form['ship']
        sku = request.form['sku']  # want this to be user generated or machine generated?
        # item_total = request.form['item_total'] # calculate this from the unit price, the qty and gst
        item_total = None
        rcv_date = request.form['rcv_date']
        item_id = uuid.uuid4().hex
        item_dict = dict(pid=pid, item_descr=item_descr, size=size, qty=qty, u_price=u_price, gst=gst, ship=ship,
                         item_total=item_total, rcv_date=rcv_date, item_id=item_id, sku=sku)
        order_obj = Order.get_ord_by_id(_id)
        order_obj.items.append(item_dict)
        order_obj.save_to_mongo()
        return redirect(url_for('order.order'))


@order_blueprint.route('/item_edit/<string:_id>/<string:item_id>', methods={'GET', 'POST'})
def edit_item(_id, item_id):
    if request.method == 'GET':
        item = Order.get_item_for_order(_id, item_id)
        return render_template('order/edit_item.html', item=item, _id=_id)

    else:
        pid = request.form['pid']
        item_descr = request.form['item_descr']
        size = request.form['size']
        qty = request.form['qty']
        u_price = request.form['u_price']
        gst = request.form['gst']
        ship = request.form['ship']
        sku = request.form['sku']  # want this to be user generated or machine generated?
        # item_total = request.form['item_total'] # calculate this from the unit price, the qty and gst
        item_total = None
        rcv_date = request.form['rcv_date']
        item_id = item_id
        item_dict = dict(pid=pid, item_descr=item_descr, size=size, qty=qty, u_price=u_price, gst=gst, ship=ship,
                         item_total=item_total, rcv_date=rcv_date, item_id=item_id, sku=sku)
        # order_obj = Order.get_ord_by_id(_id)
        # order_obj.items.append(item_dict)
        # item = Order.get_item_for_order(_id, item_id)
        # order_obj = Order.get_ord_by_id(_id)
        # order_obj.items.remove(item)
        Order.update_item(_id, item_id, item_dict)
        return redirect(url_for('order.order_edit', _id=_id))


