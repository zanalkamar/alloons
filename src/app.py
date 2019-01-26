from flask import Flask, render_template, redirect, url_for

from src.common.database import Database
from src.models.admin.views import admin_blueprint
from src.models.expense.views import expense_blueprint
from src.models.users.views import user_blueprint
from src.models.settings.views import settings_blueprint
from src.models.order.views import order_blueprint
from src.models.investor.views import investor_blueprint
from src.models.files.views import files_blueprint
from src.models.shopify_order.views import shopify_blueprint


app = Flask(__name__)
app.config.DEBUG = True
# keep app.config.DEBUG = True # for trouble shooting
app.secret_key = "#h@kshUsr#vn$"


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    # return redirect(url_for('users.user_home'))
    # return render_template('home.html')
    return redirect(url_for('users.user_home'))


app.register_blueprint(admin_blueprint, url_prefix="/admin")
app.register_blueprint(expense_blueprint, url_prefix="/expense")
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(settings_blueprint, url_prefix="/settings")
app.register_blueprint(order_blueprint, url_prefix="/order")
app.register_blueprint(investor_blueprint, url_prefix="/investor")
app.register_blueprint(files_blueprint, url_prefix="/files")
app.register_blueprint(shopify_blueprint, url_prefix="/shopify")



