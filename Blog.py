from model.Post import Post
from model.User import User
from model.Comment import Comment
import webapp2
import os
import time

import utils

from google.appengine.ext import db

class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = utils.jinja_env.get_template(template)
        return t.render(params)
        
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = utils.make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val)
        )

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and utils.check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header(
            'Set-Cookie',
            'user_id=; Path=/'
        )

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

class BlogFront(BlogHandler):
    def get(self):
        # posts = Post.all().order("~created")
        posts = db.GqlQuery("Select * from Post order by created desc limit 10")
        username = self.user and self.user.name
        self.render("front.html", username = username, posts = posts)

class PostPage(BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=utils.blog_key())
        post = db.get(key)
        
        comments = post.comments

        if not post:
            self.error(404)
            return

        username = self.user and self.user.name

        self.render("permalink.html", 
                    username = username,
                    post_id = post_id,
                    comments = comments,
                    post = post)

class DeletePost(BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=utils.blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        post.delete()

        self.redirect("/blog")

class LikePost(BlogHandler):
    def get(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id), parent=utils.blog_key())
            post = db.get(key)

            if not post:
                self.error(404)
                return

            post.likes = 0 if post.likes is None else int(post.likes)
            post.likes += 1

            post.save()

            self.redirect('/blog/%s' % str(post.key().id()))
        else:
            self.redirect('/login')

class EditPost(BlogHandler):
    def get(self):
        post_id = self.request.get("key")
        key = db.Key.from_path('Post', int(post_id), parent=utils.blog_key())
        post = db.get(key)
        
        if not post:
            self.error(404)
            return
        
        if post.key().id():
            self.redirect('/blog/%s' % str(post.key().id()))
        else:
            self.redirect('/blog')

    def post(self):
        post_id = self.request.get("key")
        key = db.Key.from_path('Post', int(post_id), parent=utils.blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return
        
        post.subject = self.request.get("subject")
        post.content = self.request.get("content")
        post.author = self.user.name
        error = ""

        if post.subject and post.content:
            post.save()

            time.sleep(0.1)
            self.redirect('/blog')
        else:
            error = "subject and content, please!"
            self.render("editpost.html",
                        title = "Edit Post",
                        username = self.user.name,
                        subject = post.subject,
                        content = post.content,
                        author = post.author,
                        error = error)

class NewPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html",
                        title = "New Post",
                        username = self.user.name)
        else:
            self.redirect('/login')

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        author = self.user.name
        error = ""

        if subject and content:
            p = Post(parent = utils.blog_key(), subject = subject, content = content, author = author)
            p.put()

            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html",
                        title = "New Post",
                        username = self.user.name,
                        subject = subject,
                        content = content,
                        error = error)

## Comment section
class NewComment(BlogHandler):
    def get(self):
        if self.user:
            post_id = self.request.get("key")
            key = db.Key.from_path('Post', int(post_id), parent=utils.blog_key())
            post = db.get(key)
            
            if not post:
                self.error(404)
                return
            
            if post.key().id():
                self.redirect('/blog/%s' % str(post.key().id()))
            else:
                self.redirect('/blog')
        else:
            self.redirect('/login')
        
    def post(self):
        if self.user:
            post_id = self.request.get("key")
            key = db.Key.from_path('Post', int(post_id), parent=utils.blog_key())
            post = db.get(key)

            if not post:
                self.error(404)
                return

            if post.key().id():
                content = self.request.get("content")
                author = self.user.name
                error = ""

                if content:
                    c = Comment(post = post, content = content, author = author)
                    c.put()

                self.redirect('/blog/%s' % str(post.key().id()))
            else:
                self.redirect('/blog')
        else:
            self.redirect('/login')