import utils
from Post import Post

from google.appengine.ext import db

class Comment(db.Model):
    post = db.ReferenceProperty(Post, collection_name="comments")
    content = db.TextProperty(required = True)
    author = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return utils.render_str("comment.html", c = self)