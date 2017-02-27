from model.Post import Post
from model.User import User
from model.Like import Like
from model.Comment import Comment
import webapp2
import os
import time

from BlogHandler import BlogHandler
import utils

from google.appengine.ext import db


class BlogFront(BlogHandler):
    """ Render blog's front page """
    def get(self):
        """ Front page's GET render """
        posts = db.GqlQuery("""Select * from Post order
                            by created desc limit 10""")
        username = self.user and self.user.name

        self.render("front.html", username=username, posts=posts)


class PostPage(BlogHandler):
    """ Render blog's post """
    def get(self, post_id):
        """ Render blog's post - get method """
        key = db.Key.from_path('Post', int(post_id), parent=utils.blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        username = self.user and self.user.name

        self.render("permalink.html",
                    username=username,
                    post_id=post_id,
                    post=post)


class DeletePost(BlogHandler):
    """ Delete post """
    def get(self, post_id):
        """ Delete post - get method """
        key = db.Key.from_path('Post', int(post_id), parent=utils.blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        if post.author:
            post.delete()
            self.render('delete.html',
                        message="Post succesfully deleted")
        else:
            self.render('delete.html',
                        message="Error attempting to delete post")


class LikePost(BlogHandler):
    """ Like post class """
    def get(self, post_id):
        """ Like post - get method """
        if self.user:
            key = db.Key.from_path('Post',
                                   int(post_id),
                                   parent=utils.blog_key())
            post = db.get(key)
            author = User.by_name(self.user.name)
            like = True

            if not post:
                self.error(404)
                return

            post_like = Like(author=author, post=post, like=like)
            post_like.put()

            self.redirect('/blog/%s' % str(post.key().id()))
        else:
            self.redirect('/login')


class EditPost(BlogHandler):
    """ Edit post class """
    def get(self):
        """ Like post class - get method """
        post_id = self.request.get("key")
        key = db.Key.from_path('Post',
                               int(post_id),
                               parent=utils.blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        if post.key().id():
            self.redirect('/blog/%s' % str(post.key().id()))
        else:
            self.redirect('/blog')

    def post(self):
        """ Like post class - post method """
        post_id = self.request.get("key")
        key = db.Key.from_path('Post',
                               int(post_id),
                               parent=utils.blog_key())
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
                        title="Edit Post",
                        username=self.user.name,
                        subject=post.subject,
                        content=post.content,
                        author=post.author,
                        error=error)


class NewPost(BlogHandler):
    """ New post class """
    def get(self):
        """ New post class - get method """
        if self.user:
            self.render("newpost.html",
                        title="New Post",
                        username=self.user.name)
        else:
            self.redirect('/login')

    def post(self):
        """ New post class - post method """
        if self.user:
            subject = self.request.get("subject")
            content = self.request.get("content")
            author = User.by_name(self.user.name)

            error = ""

            if subject and content:
                to_post = Post(parent=utils.blog_key(),
                               subject=subject,
                               content=content,
                               author=author)
                to_post.put()
                self.redirect('/blog/%s' % str(to_post.key().id()))
            else:
                error = "subject and content, please!"
                self.render("newpost.html",
                            title="New Post",
                            username=self.user.name,
                            subject=subject,
                            content=content,
                            error=error)
        else:
            self.redirect('/login')


# Comment section
class NewComment(BlogHandler):
    """ New comment class """
    def get(self):
        """ New comment class - get method """
        if self.user:
            post_id = self.request.get("key")
            key = db.Key.from_path('Post',
                                   int(post_id),
                                   parent=utils.blog_key())
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
        """ New comment class """
        if self.user:
            post_id = self.request.get("key")
            key = db.Key.from_path('Post',
                                   int(post_id),
                                   parent=utils.blog_key())
            post = db.get(key)

            if not post:
                self.error(404)
                return

            content = self.request.get("content")
            author = User.by_name(self.user.name)

            if content:
                comm = Comment(post=post, content=content, author=author)
                comm.put()

            self.redirect('/blog/%s' % str(post.key().id()))
        else:
            self.redirect('/login')
