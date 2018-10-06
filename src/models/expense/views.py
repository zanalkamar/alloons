from flask import Blueprint, render_template, request, send_file, redirect, url_for, session, make_response
from src.models.user.user import User
from src.models.expense.expense import Expense


expense_blueprint = Blueprint('expense', __name__)


@expense_blueprint.route('/', methods={'GET', 'POST'})
def expense():
    user = None
    error_msg = None

    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        item = request.form['item']
        remarks = request.form['remarks']
        cost = request.form['amount']
        exp_obj = Expense(date, category, item, remarks, cost)
        exp_obj.save_to_mongo()

    expenses = Expense.get_all_expense()#

    return render_template('expense/expense.html', expenses=expenses, error_msg=error_msg, user=user )
