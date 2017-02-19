import utils

from google.appengine.ext import db

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    author = db.StringProperty()
    likes = db.IntegerProperty()
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render(self, username):
        self._render_text = self.content.replace('\n', '<br>')
        self._key = self.key().id()
        self._can_edit = False

        if self._key:
            key = db.Key.from_path('Post', int(self._key), parent=utils.blog_key())
            post = db.get(key)
            comments_length = 10
        else:
            comments_length = 5
        
        if self.likes is None:
            self.likes = 0

        if self.author == username:
            self._can_edit = True

        return utils.render_str("post.html", p = self, comments_length = comments_length)

    def showPermalink(self, username):
        self._render_text = self.content.replace('\n', '<br>')
        self._key = self.key().id()
        self._can_edit = False
        self._is_permalink = True
        
        if self.likes is None:
            self.likes = 0

        if self.author == username:
            self._can_edit = True

        if self.author == username:
            return utils.render_str("editpost.html",
                                    title = "Edit post",
                                    username = username,
                                    author = self.author,
                                    subject = self.subject,
                                    content = self._render_text,
                                    likes = self.likes,
                                    key = self._key,
                                    error = "")
        else:
            return utils.render_str("post.html", p = self)