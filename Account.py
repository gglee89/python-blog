from Blog import BlogHandler
from model.User import User

import utils


class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/login')


class Login(BlogHandler):
    def get(self):
        if self.user:
            self.redirect('/welcome')
        else:
            self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/welcome')
        else:
            msg = "Invalid login"
            self.render('/login-form.html',
                        username=username,
                        error=msg)


class Signup(BlogHandler):
    def get(self):
        if self.user:
            self.redirect('/welcome')
        else:
            self.render('/signup-form.html')

    def post(self):
        have_error = False
        self.username = self.request.get("username")
        self.password = self.request.get("password")
        self.verify = self.request.get("verify")
        self.email = self.request.get("email")

        params = dict(username=self.username,
                      email=self.email)

        if not utils.valid_username(self.username):
            have_error = True
            params['error_username'] = "That's not a valid username"

        if not utils.valid_password(self.password):
            params['error_password'] = "That wasn't a valid password"
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your password didn't match"
            have_error = True

        if have_error:
            self.render('/signup-form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError


class Register(Signup):
    def done(self):
        u = User.by_name(self.username)
        if u:
            msg = "This user already exists"
            self.render("/signup-form.html",
                        username=self.username,
                        error_username=msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect("/welcome")


class Users(BlogHandler):
    def get(self):
        if self.user:
            users = User.getAll()
            self.render('/users.html', users=users, username=self.user.name)
        else:
            self.redirect('/login')


class Welcome(BlogHandler):
    def get(self):
        if self.user:
            self.render('welcome.html', username=self.user.name)
        else:
            self.redirect('/signup')
