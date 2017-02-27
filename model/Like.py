import utils
import sys

from model.User import User

from google.appengine.ext import db


class Like(db.Model):
    author = db.ReferenceProperty(User)
    like = db.BooleanProperty()

    @classmethod
    def countLikesByPost(cls, post):
        post_likes = Like.all().filter('post=', post).count()
        return post_likes
