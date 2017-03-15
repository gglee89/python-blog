from model.User import User

import utils
import webapp2


class BlogHandler(webapp2.RequestHandler):
    """ Blog handler """
    def write(self, *a, **kw):
        """ Use it as the writer """
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        """
        A function to render the template string
        """
        t = utils.jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        """
        Render the template
        """
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        """
        Sets a secure cookie in the headers
        """
        cookie_val = utils.make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val)
        )

    def read_secure_cookie(self, name):
        """
        Read a cookie based on a name
        """
        cookie_val = self.request.cookies.get(name)
        return cookie_val and utils.check_secure_val(cookie_val)

    def login(self, user):
        """
        Sets a secure cookie
        """
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        """
        Deletes the cookie in the header
        """
        self.response.headers.add_header(
            'Set-Cookie',
            'user_id=; Path=/'
        )

    def initialize(self, *a, **kw):
        """
        Initializes the secure cookie
        """
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))
