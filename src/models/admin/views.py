from flask import Blueprint, render_template, request, send_file, redirect, url_for, session, make_response
# from src.models.device.device import Device
# from src.models.users.users import User

# test with the below and move to proper location
from src.common.database import Database

admin_blueprint = Blueprint('admin', __name__)
