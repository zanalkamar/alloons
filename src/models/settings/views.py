from flask import Blueprint, render_template, request, send_file, redirect, url_for, session, make_response
from src.models.users.users import User


settings_blueprint = Blueprint('settings', __name__)


@settings_blueprint.route('/home', methods={'GET'})
def settings():
    user = User.find_by_email(session.get('email'))
    return render_template('settings/settings.html', user=user)






