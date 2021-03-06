import os
import re
import random
import hmac
import hashlib

from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

def render_str(template, **params):
    """
    A function to render the HTML template
    """
    t = jinja_env.get_template(template)
    return t.render(params)


def make_secure_val(val):
    """
    A function to generate the secure cookie value
    """
    secret = "dhao$)DAH@(!#)"
    return "%s|%s" % (val, hmac.new(secret, val).hexdigest())


def check_secure_val(secure_val):
    """
    A function to check the generated secure cookie value
    """
    val = secure_val.split("|")[0]
    if secure_val == make_secure_val(val):
        return val


# user stuff
def make_salt(length=5):
    """
    A function to generate salt key
    """
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(name, pw, salt=None):
    """
    A function to generate a password hash
    """
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pw(name, password, h):
    """
    A function to check if password hash match
    """
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)


def users_key(group='default'):
    """
    A function to return the entity User key
    """
    return db.Key.from_path('users', group)


# blog stuff
def blog_key(name='default'):
    """
    A function to return the entity Blog key
    """
    return db.Key.from_path('blogs', name)


def valid_username(username):
    """
    A function to vlidate the username has at least 3 characters and
    maximum of 20 characters
    """
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(username)


def valid_password(password):
    """
    A function to validate the password has at least 3 characters and
    maximum of 20 characters
    """
    PASSWORD_RE = re.compile(r"^.{3,20}$")
    return PASSWORD_RE.match(password)


def valid_email(email):
    """
    A function to validate the email address using regex
    """
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return EMAIL_RE.match(email)
