from flask import Blueprint, render_template, request, send_file, redirect, url_for, session, make_response
from src.models.users.users import User
from src.models.investor.investor import Investor

investor_blueprint = Blueprint('investor', __name__)


@investor_blueprint.route('/', methods={'GET', 'POST'})
def investor():
    error_msg = None
    if not Investor.check_user_access(session.get('email'), 'admin'):
        # this is for the access level testing. move it to decorator
        return render_template('users/login.html')

    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        join_date = request.form['date']
        # name, join_date = None, contacts = None, sku_dict = None, _id = None
        inv_obj = Investor(name=name, join_date=join_date, contacts={'mobile': mobile, 'email': email})
        inv_obj.save_to_mongo()

    investors = Investor.get_all()
    user = User.find_by_email(session.get('email'))
    return render_template('investor/investor.html', investors=investors, error_msg=error_msg, user=user)


@investor_blueprint.route('/edit/<string:_id>', methods={'GET', 'POST'})
def investor_edit(_id):
    user = User.find_by_email(session.get('email'))
    if request.method == 'GET':
        investor = Investor.get_investor_by_id(_id)
        return render_template('investor/edit.html', investor=investor, user=user)
    else:
        sku_amount = request.form['sku_amount']
        sku = request.form['sku']
        sku_descr = request.form['sku_descr']
        # sku description should be auto populated for him
        sku_amount = request.form['sku_amount']
        sku_num = request.form['sku_num']
        # this num should be changed to quantity
        sku_date = request.form['inv_date']
        inv = Investor.get_investor_by_id(_id)
        inv.sku_dict[sku] = dict(amount=int(sku_amount), number=int(sku_num))
        inv.save_to_mongo()
    return redirect(url_for('investor.investor'))


@investor_blueprint.route('/del/<string:_id>', methods={'GET', 'POST'})
def del_investor(_id):
    Investor.del_investor_by_id(_id)
    return redirect(url_for('investor.investor'))


# @investor_blueprint.route('/del/<string:_id>', methods={'GET', 'POST'})
# def del_investor(_id):
#     Investor.del_investor_by_id(_id)
#     return redirect(url_for('investor.investor'))


