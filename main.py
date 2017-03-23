import webapp2

from Blog import BlogFront, PostPage, NewPost, EditPost, DeletePost
from Blog import UnlikePost, LikePost, NewComment, BlogHandler
from Blog import EditComment, DeleteComment
from Account import Login, Logout, Signup, Register, Users, Welcome

app = webapp2.WSGIApplication([('/', BlogFront),
                               ('/blog', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/like/([0-9]+)', LikePost),
                               ('/blog/unlike/([0-9]+)', UnlikePost),
                               ('/blog/newpost', NewPost),
                               ('/blog/newcomment', NewComment),
                               ('/blog/editpost', EditPost),
                               ('/editcomment/([0-9]+)', EditComment),
                               ('/deletepost/([0-9]+)', DeletePost),
                               ('/deletecomment/([0-9]+)', DeleteComment),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/users', Users),
                               ('/welcome', Welcome)
                               ], debug=True)
