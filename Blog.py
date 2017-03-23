from model.Post import Post
from model.User import User
from model.Comment import Comment
import webapp2
import os
import time

from BlogHandler import BlogHandler
import utils

from google.appengine.ext import db

def login_required(func):
    """
    A decorator to confirm a user is logged in or redirect as needed
    """
    def login(self, *args, **kwargs):
        """ Redirect to login if user is not logged in, else execute func """
        if not self.user:
            self.redirect('/login')
        else:
            func(self, *args, **kwargs)
    return login

class BlogFront(BlogHandler):
    """ Render blog's front page """
    @login_required
    def get(self):
        """ Front page's GET render """
        posts = db.GqlQuery("""Select * from Post order
                            by created desc limit 10""")
        username = self.user and self.user.name

        self.render("front.html", username=username, posts=posts)


class PostPage(BlogHandler):
    """ Render blog's post """
    @login_required
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
    @login_required
    def get(self, post_id):
        """ Delete post - get method """
        key = db.Key.from_path('Post', int(post_id), parent=utils.blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        if post.author.key().id() == self.user.key().id():
            post.delete()
            self.render('delete.html',
                        message="Post succesfully deleted")
        else:
            self.render('delete.html',
                        message="Error attempting to delete post")


class DeleteComment(BlogHandler):
    """ Delete comment """
    @login_required
    def get(self, comment_id):
        """ Delete comment - get method """
        key = db.Key.from_path('Comment', int(comment_id))
        comment = db.get(key)

        if not comment:
            self.error(404)
            return

        if comment.author.key().id() == self.user.key().id():
            comment.delete()
            self.render('delete.html',
                        message="Comment succesfully deleted")
        else:
            self.render('delete.html',
                        message="You can't delete this comment.")


class LikePost(BlogHandler):
    """ Like post class """
    @login_required
    def get(self, post_id):
        """ Like post - get method """
        key = db.Key.from_path('Post',
                               int(post_id),
                               parent=utils.blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        if post.author.key().id() == self.user.key().id():
            message = "Authors can't like their own post"
            self.render('front.html', message=message)
        else:
            post.likes = int(post.likes) + 1
            post.authorLiked = True
            post.save()

            self.redirect('/blog/%s' % str(post.key().id()))


class UnlikePost(BlogHandler):
    """ Like post class """
    @login_required
    def get(self, post_id):
        """ Like post - get method """
        key = db.Key.from_path('Post',
                               int(post_id),
                               parent=utils.blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        if post.author.key().id() == self.user.key().id():
            message = "Authors can't like their post"
            self.render('front.html', message=message)
        else:
            post.likes = int(post.likes) - 1
            post.authorLiked = False
            post.save()

            self.redirect('/blog/%s' % str(post.key().id()))


class EditPost(BlogHandler):
    """ Edit post class """
    @login_required
    def get(self):
        """ Edit post class - get method """
        self.redirect('/blog')

    @login_required
    def post(self):
        """ Edit post class - post method """
        post_id = self.request.get("key")
        key = db.Key.from_path('Post',
                               int(post_id),
                               parent=utils.blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        if post.author.key().id() == self.user.key().id():
            post.subject = self.request.get("subject")
            post.content = self.request.get("content")
            post.author = self.user
            error = ""

            if post.subject and post.content:
                post.save()

                # Setting timer to give time for the Server to SAVE
                time.sleep(2)

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
        else:
            self.redirect("/login")


class NewPost(BlogHandler):
    """ New post class """
    @login_required
    def get(self):
        """ New post class - get method """
        self.render("newpost.html",
                    title="New Post",
                    username=self.user.name)

    @login_required
    def post(self):
        """ New post class - post method """
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


# Comment section
class NewComment(BlogHandler):
    """ New comment class """
    @login_required
    def get(self):
        """ New comment class - get method """
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

    @login_required
    def post(self):
        """ New comment class """
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

        # Setting timer to give time for the Server to SAVE
        time.sleep(2)
        self.redirect('/blog/%s' % str(post.key().id()))


class EditComment(BlogHandler):
    """ Edit comment class """
    @login_required
    def get(self, comment_id):
        """ Edit comment class """
        key = db.Key.from_path('Comment',
                               int(comment_id))
        comment = db.get(key)

        if not comment:
            self.error(404)
            return

        if self.user.key().id() == comment.author.key().id():
            self.render("editcomment.html",
                        title="Edit Comment",
                        key=comment_id,
                        author=comment.author.name,
                        content=comment.content)
        else:
            self.redirect('/login')

    @login_required
    def post(self, comment_id):
        """ Edit comment class - POST """
        key = db.Key.from_path('Comment',
                               int(comment_id))

        comment = db.get(key)

        if not comment:
            self.error(404)
            return

        if self.user.key().id() == comment.author.key().id():
            comment.content = self.request.get("content")
            error = ""

            if comment.content:
                comment.save()

                #Setting timer to give time for the Server to SAVE
                time.sleep(2)

                self.redirect('/blog')
            else:
                error = "Fill in the content, please!"
                self.render("editcomment.html",
                            title="Edit Comment",
                            username=self.user.name,
                            content=comment.content,
                            author=comment.author,
                            error=error)
        else:
            self.redirect('/login')