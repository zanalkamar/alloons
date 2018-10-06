from flask import Blueprint, render_template, request, session, redirect, url_for

from src.models.users.users import User


user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_users():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if User.login_user(email, password):
                session['email'] = email
                # return redirect(url_for("device.device"))
                user = User.find_by_email(email)
                return render_template('home.html', user=user)
            else:
                return render_template('users/login.html')
        except Exception as e:
            # change this to proper Error management
            print(e)
            return render_template('users/login.html')
    return render_template('users/login.html')


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return render_template('home.html')


@user_blueprint.route('/home')
def user_home():
    email = session.get('email')
    if email:
        return render_template('home.html', user=User.find_by_email(email))
    else:
        return render_template('home.html', user=None)


@user_blueprint.route('/users', methods={'GET', 'POST'})
def users():
    # if not User.check_access_email(session.get('email'), 'super_user'):
    #     return render_template('users/login.html')
    # user = User.find_by_email(session.get('email'))
    user = None
    all_user_obj = User.get_all_users()
    # print('User is {}'.format(user.name))
    return render_template('users/users.html', user_objs=all_user_obj, error_msg=None, user=user)


@user_blueprint.route('/add', methods={'GET', 'POST'})
def add_user():
    # if not User.check_access_email(session.get('email'), 'super_user'):
    #     return render_template('users/login.html')
    error_msg = None
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        access = request.form['access']
        try:
            User.register_user(email, password, name, access)
        except Exception as e:
            # print(e)
            error_msg = e

    all_users = User.get_all_users()
    return render_template('users/users.html', users=all_users, error_msg = error_msg)


@user_blueprint.route('/edit/<string:_id>', methods={'GET', 'POST'})
def edit_user(_id):
    # if not User.check_access_email(session.get('email'), 'super_user'):
    #     return render_template('users/login.html')
    user = User.find_by_email(session.get('email'))
    if request.method == 'GET':
        user_obj = User.find_by_id(_id)
        return render_template('users/edit.html', user_obj=user_obj, user=user)
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        access = request.form['access']
        user_obj=User.find_by_id(_id)
        user_obj.name = name
        user_obj.email = email
        user_obj.password = password if password else user_obj.password
        user_obj.access = access
        user_obj.save_to_mongo()
        return redirect(url_for('users.users'))


@user_blueprint.route('/delete/<string:_id>', methods={'GET'})
def del_user(_id):
    # if not User.check_access_email(session.get('email'), 'super_user'):
    #     return render_template('users/login.html')
    User.del_user_by_id(_id)
    return redirect(url_for('users.users'))
