# from passlib.hash import pbkdf2_sha512
import re
from passlib.hash import pbkdf2_sha512

class Utils(object):
    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^([\w-])+@([\w-]+\.)+[\w]+$')
        return True if email_address_matcher.match(email) else False
        #no need for this method as flask can handle this directly

    @staticmethod
    def hash_password(password):
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        return pbkdf2_sha512.verify(password, hashed_password)
