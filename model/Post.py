import utils
from User import User

from google.appengine.ext import db


class Post(db.Model):
    """ Post class """
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    author = db.ReferenceProperty(User, collection_name="posts")
    authorLiked = db.BooleanProperty(required=False, default=False)
    likes = db.IntegerProperty(required=False, default=0)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    @property
    def like(self):
        """ like property """
        print 'Getting like value'
        return self.likes

    @like.setter
    def like(self, value):
        print 'Setting like value'
        self.likes = value

    def render(self, username):
        """ Post class render method """
        self._render_text = self.content.replace('\n', '<br>')
        self._key = self.key().id()
        self._can_edit = False

        key = db.Key.from_path('Post', int(self._key), parent=utils.blog_key())

        if self.author == username:
            self._can_edit = True

        return utils.render_str("post.html",
                                p=self)

    def showPermalink(self, username):
        """ Post class render permalink """
        self._render_text = self.content.replace('\n', '<br>')
        self._key = self.key().id()
        self._can_edit = False
        self._is_permalink = True

        if self.author == username:
            self._can_edit = True

        if self.author == username:
            return utils.render_str("editpost.html",
                                    title="Edit post",
                                    username=username,
                                    author=self.author,
                                    subject=self.subject,
                                    content=self._render_text,
                                    key=self._key,
                                    error="")
        else:
            return utils.render_str("post.html", p=self)
