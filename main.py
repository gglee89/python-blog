import webapp2

from Blog import BlogFront, PostPage, NewPost, EditPost, DeletePost, LikePost, NewComment, BlogHandler
from Account import Login, Logout, Signup, Register, Users, Welcome

app = webapp2.WSGIApplication([('/', BlogFront),
                               ('/blog', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/like/([0-9]+)', LikePost),
                               ('/blog/newpost', NewPost),
                               ('/blog/newcomment', NewComment),
                               ('/blog/editpost', EditPost),
                               ('/blog/delete/([0-9]+)', DeletePost),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/users', Users),
                               ('/welcome', Welcome)
                               ],
                                debug=True)