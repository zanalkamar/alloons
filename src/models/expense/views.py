from flask import Blueprint, render_template, request, send_file, redirect, url_for, session, make_response
from src.models.users.users import User
from src.models.expense.expense import Expense
from datetime import datetime


expense_blueprint = Blueprint('expense', __name__)


@expense_blueprint.route('/', methods={'GET', 'POST'})
def expense():
    error_msg = None
    if not Expense.check_user_access(session.get('email'), 'admin'):
        # this is for the access level testing. move it to decorator
        return render_template('users/login.html')

    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        category = request.form['category']
        item = request.form['item']
        remarks = request.form['remarks']
        cost = request.form['amount']
        exp_obj = Expense(date, category, item, remarks, cost)
        exp_obj.save_to_mongo()

    expenses = Expense.get_all_expense()  #
    sum_dict = Expense.get_sum_dict()

    user = User.find_by_email(session.get('email'))

    return render_template('expense/expense.html', expenses=expenses, error_msg=error_msg, user=user, sum_dict=sum_dict)


@expense_blueprint.route('/edit/<string:_id>', methods={'GET', 'POST'})
def expense_edit(_id):
    user = User.find_by_email(session.get('email'))
    if request.method == 'GET':
        expense = Expense.get_exp_by_id(_id)
        return render_template('expense/edit.html', expense=expense, user=user)
    else:
        # date = request.form['date']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        # category = request.form['category']
        item = request.form['item']
        remarks = request.form['remarks']
        # cost = request.form['amount']
        amount = request.form['amount']
        exp = Expense.get_exp_by_id(_id)
        exp.date = date
        # exp.category = category
        exp.item = item
        exp.remarks = remarks
        exp.amount = amount
        exp.save_to_mongo()
    return redirect(url_for('expense.expense'))


@expense_blueprint.route('/del/<string:_id>', methods={'GET', 'POST'})
def del_expense(_id):
    Expense.del_expense_by_id(_id)
    return redirect(url_for('expense.expense'))

