import utils
from User import User

from google.appengine.ext import db


class Post(db.Model):
    """ Post class """
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    author = db.ReferenceProperty(User, collection_name="posts")
    liked_by = db.ListProperty(int)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    @property
    def likes(self):
        """ like property """
        return len(self.liked_by)

    def render(self, username):
        """ Post class render method """
        self._render_text = self.content.replace('\n', '<br>')
        self._key = self.key().id()
        self._can_edit = False

        key = db.Key.from_path('Post', int(self._key), parent=utils.blog_key())

        if self.author.name == username:
            self._can_edit = True

        return utils.render_str("post.html",
                                p=self)

    def showPermalink(self, username):
        """ Post class render permalink """
        self._render_text = self.content.replace('\n', '<br>')
        self._key = self.key().id()
        self._can_edit = False
        self._is_permalink = True

        if self.author.name == username:
            self._can_edit = True
            return utils.render_str("editpost.html",
                                    title="Edit post",
                                    username=username,
                                    author=self.author.name,
                                    subject=self.subject,
                                    content=self._render_text,
                                    key=self._key,
                                    error="")
        else:
            return utils.render_str("post.html", p=self)
