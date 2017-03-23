import utils
from Post import Post
from User import User

from google.appengine.ext import db


class Comment(db.Model):
    post = db.ReferenceProperty(Post, collection_name="comments")
    content = db.TextProperty(required=True)
    author = db.ReferenceProperty(User, collection_name="comments")
    created = db.DateTimeProperty(auto_now_add=True)

    def render(self, username):
        self._isAuthor = False
        if username == self.author.name:
            self._isAuthor = True

        self._render_text = self.content.replace('\n', '<br>')
        self._key = self.key().id()
        return utils.render_str("comment.html", c=self)
