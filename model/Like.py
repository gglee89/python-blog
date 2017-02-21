import utils

from google.appengine.ext import db
from model.Post import Post


class Like(db.Model):
    user = db.ReferenceProperty(Post)
    liked = db.BooleanProperty()
